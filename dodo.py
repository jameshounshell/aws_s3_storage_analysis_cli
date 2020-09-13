"""

https://pydoit.org/contents.html
"""

DOIT_CONFIG = {"backend": "sqlite3", "verbosity": 2, "default_tasks": ["fmt"]}


def task_fmt():
    return {"actions": ["black ."]}


def task_cli():
    return {"actions": ["python store/cli.py --help"]}


def task_test_unit():
    return {"actions": ["pytest"]}


# test_end_to_end:
#
# docker_build:
# docker build -t store .
#
# docker_run: build
# docker run --rm store
#
