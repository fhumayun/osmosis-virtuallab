#!/usr/bin/env python3
import os
import sys

# TODO: Add help
container = input("Which container do you want to start? (A,B,C,D,E,F): ")
container = container.upper()

valid_containers = ('A', 'B', 'C', 'D', 'E', 'F')

if container not in valid_containers:
    print(f"container-{container} doesn't exist")
    sys.exit()

os.system(f"docker container start container-{container}")
