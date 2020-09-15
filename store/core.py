"""
The highest level functions are stored in this file
"""
import json
import datetime
import boto3
from mypy_boto3_s3 import Client
from itertools import chain
import time
import multiprocessing
import string

s3_safe_char = [
    *list(string.ascii_lowercase),
    *list(string.ascii_uppercase),
    *list(string.digits),
    "/",
    "!",
    "-",
    "_",
    ".",
    "*",
    "'",
    "(",
    ")",
]


class S3:
    def __init__(self, profile="default", region="us-east-1"):
        self._session = boto3.session.Session(profile_name=profile, region_name=region)
        self._client: Client = self._session.client("s3")

    @staticmethod
    def check_status_code(response):
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def list_buckets(self):
        response = self._client.list_buckets()
        self.check_status_code(response)
        return response["Buckets"]

    def bucket_names(self):
        return [d["Name"] for d in self.list_buckets()]

    def list_objects_parallel(self, bucket):
        data = []
        for prefix in s3_safe_char:
            data.append(
                (self._session.profile_name, self._session.region_name, bucket, prefix)
            )

        num_pool = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num_pool)
        with pool as p:
            results = p.map(list_objects_async, data)
        return list(chain.from_iterable(results))

    def list_objects(self, bucket, prefix=None):
        kwargs = {"Bucket": bucket}
        if prefix is not None:
            kwargs["Prefix"] = prefix

        objects = extract_from_paginator(
            paginator=self._client.get_paginator("list_objects_v2").paginate,
            kwargs=kwargs,
            key_to_extract="Contents",
        )
        return objects

    def summary(self, buckets: list = None, units=None, parallel=False):
        # limit to
        if buckets:
            buckets = [b for b in self.list_buckets() if b["Name"] in buckets]
        else:
            buckets = self.list_buckets()

        stats = []
        for b in buckets:
            name = b["Name"]

            # get objects while measuring speed
            if parallel:
                f = self.list_objects_parallel
            else:
                f = self.list_objects
            objects, duration = timeit(f, [name], {})
            number_of_objects = len(objects)
            size = 0
            last_modified = None
            if number_of_objects != 0:
                size = sum([o["Size"] for o in objects])
                last_modified = list(
                    sorted(objects, key=lambda x: x["LastModified"], reverse=True)
                )[0]["LastModified"]

            stats.append(
                {
                    "Name": name,
                    "CreationDate": b["CreationDate"],
                    "NumberOfFiles": number_of_objects,
                    "LastModified": last_modified,
                    "Size": format_bytes(size, prefix=units),
                    "ReadTime": duration,
                }
            )
        return stats


def list_objects_async(args):
    profile, region, bucket, prefix = args
    _client: Client = boto3.session.Session(
        profile_name=profile, region_name=region
    ).client("s3")
    objects = extract_from_paginator(
        paginator=_client.get_paginator("list_objects_v2").paginate,
        kwargs={"Bucket": bucket, "Prefix": prefix},
        key_to_extract="Contents",
    )
    return objects


def test_format_bytes():
    bytes = 11234235253
    assert format_bytes(bytes) == "10.46 GB"
    assert format_bytes(bytes, "GB") == "10.46 GB"
    assert format_bytes(bytes, "MB") == "10713.80 MB"


def format_bytes(size, prefix=None):
    power = 2 ** 10  # 2**10 = 1024
    power_labels = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    if prefix is None:
        n = 0
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}"
    else:
        assert prefix in power_labels.values()
        size = size / (power ** ({v: k for k, v in power_labels.items()}[prefix]))
        return f"{size:.2f} {prefix}"


def test_extract_from_paginator():
    def paginator(**kwargs):
        for i in [1, 2, 3]:
            yield {"Contents": [i], **kwargs}

    assert extract_from_paginator(
        paginator, kwargs={"Stuff": "foo"}, key_to_extract="Contents"
    ) == [1, 2, 3]


def extract_from_paginator(paginator, kwargs, key_to_extract):
    responses = []
    for response in paginator(**kwargs):
        if key_to_extract in response:
            responses.append(response[key_to_extract])
    return list(chain.from_iterable(responses))


def test_timeit():
    response, duration = timeit(lambda *args, **kwargs: time.sleep(1.1), [], {})
    assert duration > 1


def timeit(f, args, kwargs):
    then = time.time()
    response = f(*args, **kwargs)
    delta = time.time() - then
    return response, delta


def jprint(data):
    print(json.dumps(data, indent=4, default=str))


def main():
    jprint(S3().summary())


if __name__ == "__main__":
    main()
