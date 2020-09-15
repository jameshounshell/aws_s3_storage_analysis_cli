aws_s3_storage_analysis_cli
===========================
A Click based CLI called `store` that shows summary statistics for your AWS S3 Buckets

After install execute `store summary`

Example:
```text
>>> store summary --help
Usage: store summary [OPTIONS]

  Print Summary statistics for all buckets for a given AWS Profile and
  Region

Options:
  -p, --profile TEXT         AWS Profile (default: 'default')
  -r, --region TEXT          AWS Region (default: 'us-east-1')
  -b, --buckets TEXT         Specify a subset buckets with '-b foo,bar,baz'
                             (default: all buckets)

  -u, --units [KB|MB|GB|TB]  Specify a bytes unit prefix  (default: optimal
                             unit)

  -p, --parallel             Use rudimentary parallelization (default: False)
  --help                     Show this message and exit.

>>> store summary
[
    {
        "Name": "foo",
        "CreationDate": "2017-06-05 03:12:31+00:00",
        "NumberOfFiles": 204,
        "LastModified": "2018-02-01 15:55:06+00:00",
        "Size": "206.39 MB",
        "ReadTime": 0.13700652122497559
    },
    {
        "Name": "bar",
        "CreationDate": "2018-03-06 20:39:15+00:00",
        "NumberOfFiles": 1647,
        "LastModified": "2018-03-06 21:29:52+00:00",
        "Size": "178.73 MB",
        "ReadTime": 0.5921769142150879
    },
    {
        "Name": "baz",
        "CreationDate": "2016-11-18 20:40:35+00:00",
        "NumberOfFiles": 1,
        "LastModified": "2016-11-18 21:01:02+00:00",
        "Size": "30.00 B",
        "ReadTime": 0.0730142593383789
    }
]

```

How to Contribute
=================
- Clone this repo
- Run `make dev`
    - This will:
        - Ensure python-poetry is installed
        - Install dependencies using poetry
        - Run `poetry shell` to activate the virtual environment
- Run `make unit_test` to run any unit tests
- Run `make integration_test` to run integration tests
- Run `make test` to run all tests
- Run `make speed_test` to summarize all buckets for the default

How to Install/Run
==================
- with python:
    - requires `poetry`
    - `poetry run python store/cli.py summary`
    - or the wrapper `./cli.py summary`
- with docker:
    - requires `docker`
    - this will build a docker container then run the command specified
    - rebuilds container if `poetry.lock` changes
    - `./cli_docker.py summary`
- as a pyinstaller binary file:
    - `make pyinstaller`
    - move the binary at `dist/store` to a location on your PATH
    - `store summary`