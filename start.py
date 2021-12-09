#!/usr/bin/env python3

import os
import logging

# TODO: Add help, error handling

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info("Starting virtual lab")

os.system("docker-compose -f dockerfiles/docker-compose.yml up -d")
