[![](https://img.shields.io/badge/python-3.8.5-blue.svg?&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-385/) [![](https://img.shields.io/badge/OpenCV-3.4.0-blue?&logo=opencv&logoColor=red)](https://docs.opencv.org/3.4.0/index.html) [![](https://img.shields.io/badge/Docker-20.10.14-blue?&logo=Docker&logoColor=blue)](https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu)


The models built in this project use haarcascade features trained with OpenCV.

Positive images were annotated with OpenCV (version 4.5.5, but works on 3.4.0 which is the version required on this project) and the opencv_annotation tool (using a GUI).

Concerning the training of the haarcascade and the creation of several positive samples, they were respectively carried out with the tools opencv_createsamples and opencv_traincascade of OpenCV. These two applications cannot be called with a classic installation of OpenCV (versions greater than 3.4.x) a docker image based on Ubuntu (latest) with a pre-download of the OpenCV version 3.4 archive is necessary (if you don't want to build the OpenCV library on your local environment).
To use these tools it is necessary to build this image and use it via the CLI window of this one. For this you can refer to the documentation of the image on the Docker Hub (https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu) or let yourself be guided by the automatic installation with initialize .sh (local installation)

# Automatic installation with initialize.sh


Please look carefully at the contents of initialize.sh as it is a script that performs the following steps:

- [OPTIONAL] Install brew package utility for Mac
- [REQUIRED] Install python 3.x.x
- [REQUIRED] Install the virtual environment manager virtualenv
- [OPTIONAL] Install git
- [OPTIONAL] Install cmake & gcc
- [OPTIONAL] Install wget & unzip
- [OPTIONAL] Download and build OpenCV from version 3.4.0 (cmake & gcc installation)
- [OPTIONAL] Propose to build the docker image containing a stable version of OpenCV 3.4.0
- [REQUIRED] Create a python virtual environment with the necessary libraries

The optional steps allow you to obtain an environment allowing you to use OpenCV as you wish to adapt the programs to your projects / needs.
The required steps are minimal steps necessary in order to run the programs from the provided example data (or from pre-trained models).

This operation is possible for POSIX systems (Unix / Linux based systems). This script also launches another script named 'env.sh' which allows you to activate the virtual environment with the following command:

> <code>activate</code>

Si vous n'utilisez pas le script 'initialize.sh', il est tout de même possible d'utiliser le script 'env.sh' pour faciliter l'utilisation de l'environnement virtuel.
Pour cela, veuillez lancer le script en mode 'source' :

> <code>source env.sh</code>

Please note that you can also make this script executable through the following command:

> <code>chmod +x /env.sh</code>

To deactivate the virtual environment, use the following command:

> <code>deactivate</code>

Please note that you must be in the same session in which 'env.sh' was launched if you want to use these commands (if you close and reopen a console, or change console, you will have to rerun 'env.sh').

# How to run the stable 3.4.0 version of OpenCV building a docker image


At the root of this project you will find a folder named 'docker' containing a dockerfile from which you can manually mount the image containing the stable version of OpenCV 3.4.0. Once mounted, you can launch the container with the following command:

> <code>docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]</code>

You can use the -it parameter and bash to launch the container in interactive mode through a CLI window to access OpenCV commands (c.f. official Docker documentation: https://docs.docker.com/engine/reference/run/).

You also have the possibility to mount the image containing the stable version of OpenCV 3.4.0 directly from Docker Hub (https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu).
Note that if you are using a version of OpenCV from an image, you will need to create a gateway between your host system and the Docker container in order to access your data (images, .info files etc.) when using OpenCV commands (e.g. opencv_createsamples, opencv_traincascade). You can also copy your data folder as soon as the image is mounted by configuring the COPY line of the dockerfile (by default it is configured to copy data from the classifiers-constructor folder). The structure is as follows:

> <code>COPY [RELATIVE PATH OF FILES / DIRS TO COPY ON THE HOST SYSTEM] [ABSOLUTEE PATH ON THE IMAGE]</code>

# OpenCV folder


This folder contains a .zip archive of OpenCV version 3.4.0 if you want to install OpenCV on your own.