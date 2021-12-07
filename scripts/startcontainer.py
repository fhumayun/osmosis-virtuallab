#!/usr/bin/env python3
import os

container = input("Which container do you want to start? (A,B,C,D,E,F)")
os.system(f"docker container start container-{container}")
