#!/usr/bin/env python3

import subprocess as sp
import sys
import os
import glob
import yaml
import logging
from lib import constants


class product:
    """Represents a wti product/application"""
    file_name = ""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version


def getFileName(product: product) -> tuple[str, str]:
    """
    Verify that the product version exists.

    Return the file name and version.
    """
    if product.version is not None:
        logging.info(f"Checking if {product.version} exist for {product.name}")
        version = "-" + product.version
    else:
        logging.info(f"No version provided for {product.name}, getting last one")
        version = ""

    if product.name == "cloud" or product.name == "osmosis":
        folder = "build"
    else:
        folder = product.name

    build_path = sp.getoutput(f"aws s3 ls s3://{constants.S3_BUCKET}/{folder}/dev/").split("\n")
    build_path = [x for x in build_path if x.endswith(".gz")
                  and f"{product.name}" in x and f"{version}" in x]

    if len(build_path) == 0:
        logging.error(f"{product.name} {version[1:]} version doesn´t exist")
        sys.exit()

    build_path = sorted(build_path)[-1]

    # get the application version number
    build_path = build_path.split(" ")[-1]
    build_version = sp.getoutput("echo %s | cut -d '-' -f 4" % build_path)

    if "tar" in build_version:
        build_version = ".".join(build_version.split(".")[:3])

    return build_path, build_version


def getFile(product: product) -> None:
    """
    Download the product file if not exist
    """

    if not os.path.isfile(f"appfiles/{product.name}{product.version}.tar.gz"):
        logging.info(f"Downloading files for {product.name}-{product.version}")
        # Remove previous files if exists
        if glob.glob(f"appfiles/{product.name}*.tar.gz"):
            os.system(f"rm appfiles/{product.name}*.tar.gz")

        if product.name == "cloud" or product.name == "osmosis":
            folder = "build"
        else:
            folder = product.name

        tar_file = f"{product.name}{product.version}.tar.gz"

        os.system(f"aws s3 cp s3://{constants.S3_BUCKET}/{folder}/dev/{product.file_name} ./{tar_file}")
        os.system(f"mv {tar_file} appfiles/")
    else:
        logging.info(f"{product.name}{product.version}.tar.gz file already exist on local")


def buildCloudTar(cloud: product, manager: product) -> None:
    """
    Build the tar file with manager and cloud
    """
    if not os.path.isfile(f"appfiles/cloud-manager-{cloud.version}-{manager.version}.tar.gz"):
        logging.info(f"Building cloud-manager-{cloud.version}-{manager.version} tar file")
        os.system("mkdir -p appfiles/cloud/manager")
        os.system(f"tar -xf appfiles/{manager.name}{manager.version}.tar.gz -C appfiles/cloud/manager")
        os.system(f"tar -xf appfiles/{cloud.name}{cloud.version}.tar.gz -C appfiles/cloud/")
        os.system("cp appfiles/license.json appfiles/cloud/cloud/config/")
        os.system("cp appfiles/star_local*.jks appfiles/cloud/star_local.jks")
        os.system(f"tar -czf appfiles/cloud-manager-{cloud.version}-{manager.version}.tar.gz -C appfiles/cloud .")
        os.system("rm -rf appfiles/cloud")
    else:
        logging.info(f"cloud-manager-{cloud.version}-{manager.version} tar file already exist")


def updateDockerCompose(cloud_image, osmosis_image, main_image) -> None:
    """
    Update the docker-compose file with the new images
    """
    logging.info("Updating docker-compose file with new images")
    compose_file = yaml.safe_load(open("dockerfiles/docker-compose.yml", "r"))
    for k, v in compose_file["services"].items():
        if v["hostname"] == "A":
            v["image"] = cloud_image
        elif v["hostname"] == "root":
            v["image"] = main_image
        else:
            v["image"] = osmosis_image
    # to write the docker-compose
    yaml.safe_dump(compose_file, open("dockerfiles/docker-compose.yml", "w+"))
