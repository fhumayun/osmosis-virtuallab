#!/usr/bin/env python3

import os
import logging

# TODO: Add help, error handling in case there is no docker compose running
logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info("Stoping virtual lab")

os.system("docker-compose -f dockerfiles/docker-compose.yml down")
