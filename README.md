[![](https://img.shields.io/badge/python-3.8.5-blue.svg?&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-385/) [![](https://img.shields.io/badge/OpenCV-3.4.0-blue?&logo=opencv&logoColor=red)](https://opencv.org/) [![](https://img.shields.io/badge/Docker-20.10.14-blue?&logo=Docker&logoColor=blue)](https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu)


The models built in this project use haarcascade features trained with OpenCV.

Positive images were annotated with OpenCV (version 4.5.5, but works on 3.4.0 which is the version required on this project) and the opencv_annotation tool (using a GUI).

Concerning the training of the haarcascade and the creation of several positive samples, they were respectively carried out with the tools createsamples and trainhaarcascade of OpenCV. These two applications cannot be called with a classic installation of OpenCV (versions greater than 3.4.x) a docker image based on Ubuntu (latest) with a pre-download of the OpenCV version 3.4 archive is necessary (if you don't want to build the OpenCV library on your local environment).
To use these tools it is necessary to build this image and use it via the CLI window of this one. For this you can refer to the documentation of the image on the Docker Hub (https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu) or let yourself be guided by the automatic installation with initialize .sh

# Automatic installation with initialize.sh



