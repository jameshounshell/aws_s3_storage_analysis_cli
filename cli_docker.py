#!/usr/bin/env python3

import hashlib
import subprocess
import sys
import os

args = sys.argv[1:]
image_name = "store"
sha_source = "poetry.lock"
sha_dest = "/tmp/cli_sha"


def main():
    if os.path.exists(sha_dest) is False or sha_sum(sha_source) != read(sha_dest):
        sp_run(f"docker build -t {image_name} .")
        write(sha_dest, sha_sum("poetry.lock"))

    print("running container")
    sp_run(f"docker run --rm -v {os.getcwd()}:/app {image_name} {' '.join(args)}")


def sp_run(command):
    print(command)
    subprocess.run(command, shell=True)


def write(filename, content):
    with open(filename, "w") as f:
        f.write(content)


def read(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def sha_sum(filename):
    with open(filename, "rb") as f:
        sum = hashlib.sha3_256(f.read()).hexdigest()
    return sum


if __name__ == "__main__":
    main()
