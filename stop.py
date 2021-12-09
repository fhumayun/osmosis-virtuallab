#!/usr/bin/env python3

import os

# TODO: Add help, error handling in case there is no docker compose running
os.system("docker-compose -f dockerfiles/docker-compose.yml down")
