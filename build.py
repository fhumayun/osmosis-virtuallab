#!/usr/bin/env python3

import argparse
from lib import helpers
import os
import sys
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

# Parse incoming parameters
args = parser.parse_args()

osmosis = helpers.product("osmosis", args.osmosis_version)
cloud = helpers.product("cloud", args.cloud_version)
manager = helpers.product("manager", args.manager_version)

products = [osmosis, cloud, manager]

# Verify that versions exist and get aws path
for p in products:
    p.file_name, p.version = helpers.getFileName(p)

# Copy tar files
for p in products:
    helpers.getFile(p)

helpers.buildCloudTar(cloud, manager)

image_tag_osmosis = "osmosis" + f":{osmosis.version}"
image_tag_cloud = "cloud" + f":cloud_{cloud.version}_manager_{manager.version}"

# Build images
os.system("docker build --tag %s -f %s/dockerfiles/Dockerfile.centos.odevapp ." % (image_tag_osmosis, os.getcwd()))
os.system("docker build --tag %s -f %s/dockerfiles/Dockerfile.centos.cloud ." % (image_tag_cloud, os.getcwd()))
