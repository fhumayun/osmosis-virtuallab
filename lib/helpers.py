#!/usr/bin/env python3

import subprocess as sp
import sys
import os
import glob
from lib import constants


class product:
    """This class represents a wti product"""
    file_name = ""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version


def getFileName(product: product):
    if product.version is not None:
        version = "-" + product.version
    else:
        version = ""

    if product.name == "cloud" or product.name == "osmosis":
        folder = "build"
    else:
        folder = product.name

    build_path = sp.getoutput(f"aws s3 ls s3://{constants.S3_BUCKET}/{folder}/dev/").split("\n")
    build_path = [x for x in build_path if x.endswith(".gz")
                  and f"{product.name}" in x and f"{version}" in x]

    if len(build_path) == 0:
        print(f"{product.name} {version[1:]} version doesn´t exist")
        sys.exit()

    build_path = sorted(build_path)[-1]

    # get the version
    build_path = build_path.split(" ")[-1]
    build_version = sp.getoutput("echo %s | cut -d '-' -f 4" % build_path)

    if "tar" in build_version:
        build_version = ".".join(build_version.split(".")[:3])
    return build_path, build_version


def getFile(product: product):
    # Remove previous files if exist
    if glob.glob(f"appfiles/{product.name}*.tar.gz"):
        os.system(f"rm appfiles/{product.name}*.tar.gz")

    if product.name == "cloud" or product.name == "osmosis":
        folder = "build"
    else:
        folder = product.name

    tar_file = f"{product.name}{product.version}.tar.gz"

    os.system(f"aws s3 cp s3://{constants.S3_BUCKET}/{folder}/dev/{product.file_name} ./{tar_file}")

    os.system(f"mv {tar_file} appfiles/")


def buildCloudTar(cloud: product, manager: product):
    os.system("mkdir -p appfiles/cloud/manager")
    os.system(f"tar -xvf appfiles/{manager.name}{manager.version}.tar.gz -C appfiles/cloud/manager")
    os.system(f"tar -xvf appfiles/{cloud.name}{cloud.version}.tar.gz -C appfiles/cloud/")
    os.system("cp appfiles/license.json appfiles/cloud/cloud/config/")
    os.system("cp appfiles/star_local*.jks appfiles/cloud/star_local.jks")
    os.system("tar -czf appfiles/osmosis-cloud.tar.gz appfiles/cloud")
    os.system("rm -rf appfiles/cloud")
