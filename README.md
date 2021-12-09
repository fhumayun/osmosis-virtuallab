# VirtualLab

Virtual Lab created testing Osmosis, Cloud and Manager.


## Initial Setup
In order to run the scripts, is required to have docker, python 3 and the packages listed on the `requirements.txt` file.

- Download docker from https://www.docker.com/products/docker-desktop and install it.
- To install python 3: `brew install python3`.
- To install additional packages: `pip3 install -r requirements.txt` from the root folder of the project.

Additional to this, is required to place the license.json and Java KeyStore files inside the `appfiles` folder.
## Usage
Run the `build.py` to create the docker images with the osmosis, cloud and manager builds from S3. Then run `start.py` to start the virtual lab and `stop.py` to stop it.

In the scripts folder:
- `stopcontainer.py` stop the desired container.
- `startcontainer.py` start the container again.
- `executetest.py` open a shell inside the root container where you can execute the tests located on `dockerfiles/test-scripts`.

## Folders

### appfiles
Store the files required for the docker images to work. This includes the build downloaded from the S3 buckets and the scripts to execute the application inside the containers.

NOTE: The license.json and Java KeyStore file needs to be located on this folder.

### dockerfiles

Includes the dockerfiles to build the images that will be used on the docker-compose. Additionally it has the `test.script` folder that is used as a volume for the `root-container`, this works for storing the scripts for the automated tests that needs to be executed.

### lib

Python files with methods and constants are required on different scripts.

### scripts
Store scripts for quick actions on the virtual lab. It includes the following files:
- `executetest.py`
- `startcontainer.py`
- `stopcontainer.py`
