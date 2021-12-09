#!/usr/bin/env python3
import os
import logging

# TODO: Add help, error handling
logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.info("Entering into main container shell")
os.system("docker exec -it container-root /bin/sh")
