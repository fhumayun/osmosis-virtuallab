#!/usr/bin/env python3

import argparse
import os
import sys
import docker
import logging
from lib import helpers

parser = argparse.ArgumentParser(description="""Build docker images for running
                                osmosis and cloud and updating the
                                docker-compose file to work with them. It is
                                required to have the star_local.jks file
                                located on docker/osmosis folder""")

parser.add_argument("-o", "--osmosis", action="store", dest="osmosis_version",
                    help="Osmosis version")
parser.add_argument("-c", "--cloud", action="store", dest="cloud_version",
                    help="Cloud version")
parser.add_argument("-m", "--manager", action="store", dest="manager_version",
                    help="Manager version")

# TODO: Set logging configuration on a separate file
logging.basicConfig(format='%(message)s', level=logging.INFO)
# Parse incoming parameters
args = parser.parse_args()

osmosis = helpers.product("osmosis", args.osmosis_version)
cloud = helpers.product("cloud", args.cloud_version)
manager = helpers.product("manager", args.manager_version)

products = [osmosis, cloud, manager]

# Verify if the docker engine is running
try:
    client = docker.from_env()
except docker.errors.DockerException:
    logging.error("Docker Engine not running, please open the docker application and run the script again")
    sys.exit()

# Verify that versions exist and get aws path
for p in products:
    p.file_name, p.version = helpers.getFileName(p)

# Copy tar files
for p in products:
    helpers.getFile(p)

helpers.buildCloudTar(cloud, manager)


# Build images
image_tag_osmosis = "osmosis" + f":{osmosis.version}"
image_tag_cloud = "cloud" + f":cloud_{cloud.version}_manager_{manager.version}"
image_tag_main = "main/container:latest"

# TODO: Change to docker package
logging.info("Building docker images")

if len(client.images.list(image_tag_osmosis)) == 0:
    os.system("docker build --tag %s -f %s/dockerfiles/Dockerfile.centos.odevapp ." % (image_tag_osmosis, os.getcwd()))
else:
    logging.info(f"{image_tag_osmosis} image already exist")

if len(client.images.list(image_tag_cloud)) == 0:
    os.system("docker build --tag %s -f %s/dockerfiles/Dockerfile.centos.cloud ." % (image_tag_cloud, os.getcwd()))
else:
    logging.info(f"{image_tag_cloud} image already exist")

if len(client.images.list(image_tag_main)) == 0:
    os.system("docker build --tag %s -f %s/dockerfiles/Dockerfile.main ." % (image_tag_main, os.getcwd()))
else:
    logging.info(f"{image_tag_main} image already exist")

logging.info("Updating docker-compose file")
helpers.updateDockerCompose(image_tag_cloud, image_tag_osmosis, image_tag_main)
