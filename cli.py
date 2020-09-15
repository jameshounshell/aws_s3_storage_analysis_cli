#!/usr/bin/env python3
import subprocess
import sys

args = sys.argv[1:]
command = f"poetry run python store/cli.py {' '.join(args)}"
subprocess.run(command, shell=True)
