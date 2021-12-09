#!/usr/bin/env python3
import os
import sys
import logging

# TODO: Add help
container = input("Which container do you want to stop? (A,B,C,D,E,F): ")
container = container.upper()

valid_containers = ('A', 'B', 'C', 'D', 'E', 'F')

if container not in valid_containers:
    logging.error(f"container-{container} doesn't exist")
    sys.exit()

if container == "A":
    logging.info(f"""container-{container} is the cloud container, if you stop it you won't be
    able to access manager in the browser""")
    continue_flag = input("Are you sure you want to stop it? Y/N: ").upper()

    if continue_flag != "Y":
        logging.info("Exiting")
        sys.exit()

logging.info(f"Stopping container-{container}")
os.system(f"docker container stop container-{container}")
