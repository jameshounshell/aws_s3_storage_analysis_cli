"""
The integration tests require the AWS cli to be configured with a default profile and us-east-1 region
Also requires at least one bucket with some files
"""
import store
import datetime
import math


def avg(args: list):
    return sum(args) / len(args)


def test_summary():
    stats = store.core.S3().summary()
    assert len(stats) > 0
    first = stats[0]
    assert all(
        [
            key in first.keys()
            for key in ["Name", "CreationDate", "NumberOfFiles", "LastModified", "Size"]
        ]
    )
    assert type(first["CreationDate"]) == datetime.datetime

    # verify speed requirement
    time_per_million_files = []
    for bucket in stats:
        if bucket["NumberOfFiles"] > 100:
            time_per_file = bucket["ReadTime"] / bucket["NumberOfFiles"]
            time_per_million_files.append(time_per_file * 1e6)

    average = avg(time_per_million_files) / 60
    print(f"{average:.2f} minutes")
    assert average < 1
    raise Exception
