#!/usr/bin/env python3
import os

container = input("Which container do you want to stop? (A,B,C,D,E,F)")
os.system(f"docker container stop container-{container}")
