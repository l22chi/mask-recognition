#!/usr/bin/env bash

RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[0;33m'
GREEN='\033[0;32m'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "${YELLOW}[INFO] Moving to the project folder : $SCRIPT_DIR ...${NC}"
cd $SCRIPT_DIR

if [[ "$OSTYPE" == "darwin"* ]]; then

    echo -e "${RED}[WARNING] You need the folloging package manager : brew${NC}"
    echo -e "${YELLOW}[INFO] Installing the package manager for macOS Brew${NC}"

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    echo -e "${YELLOW}[INFO] Installing python3 and all its dependencies${NC}"
    brew install python3
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing virtualenv and all its dependencies${NC}"
    brew install virtualenv
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing git and all its dependencies${NC}"
    brew install git
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing cmake and all its dependencies${NC}"
    brew install cmake
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing wget and all its dependencies${NC}"
    brew install wget
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing unzip and all its dependencies${NC}"
    brew install unzip
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing g++ and all its dependencies${NC}"
    brew install gcc
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Building and installing OpenCV${NC}"
    mkdir opencv && cd opencv
    wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.zip
    unzip opencv.zip
    mkdir -p build && cd build
    cmake  ../opencv-3.4
    echo -e "${RED}[WARNING] Following make command is running with -j4 param (switch control to use 4 processes), please check your number of cores.${NC}"
    make -j4
    make install
    echo -e "${GREEN}[SUCCESS] OpenCV core modules succefully compiled and installed${NC}"


elif [[ "$OSTYPE" == "linux-gnu"* ]]; then

    sudo apt-get update

    if ! python3 -c 'import sys; assert sys.version_info <= (3,7)' > /dev/null; then
        sudo apt-get install python3.8
    fi

    sudo apt-get install python3-pip
    sudo mkdir opencv && cd opencv
    sudo apt-get -y install git cmake g++ wget unzip
    wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.zip
    unzip opencv.zip
    mkdir -p build && cd build
    cmake  ../opencv-3.4
    make -j4make install

fi

cd $SCRIPT_DIR

echo -e "${RED}[WARNING] You need to have Docker installed to continue !${NC}"

echo -e "${YELLOW}[WARNING] If your OpenCV version is above 3.4.x you won't be able to use createsamples and trainhaarcascade commands. To do so, build the docker image with OpenCV 3.4${NC}"
echo -e "${YELLOW}[WARNING] The annotation tool provided by OpenCV need a graphical interface and work on latest versions of OpenCV (above 3.4.x) but won't run on the docker image${NC}"
echo "Do you want to build the corresponding docker image ? [y/n]"
read YES_OR_NO

if [ "$YES_OR_NO" = "yes" ] || [ "$YES_OR_NO" = "y" ]; then
    echo -e "${YELLOW}[INFO] Building Docker image FROM dockerfile : $CURRENT${NC}"
    sudo docker build -t opencv-image docker
    echo -e "${GREEN}[SUCCESS] Image succefully built. Please now use cmake to build OpenCV-3.4 archives. If get any troubles building it, please refers to the image doc on : ${NC}https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu"
fi

echo -e "${RED}[WARNING] Executing this script will create a virtual environment venv in the current working directory !${NC}"

cd $SCRIPT_DIR

CURRENT=$( pwd )
echo -e "${YELLOW}[INFO] The current directory is now : $CURRENT${NC}"

echo -e "${YELLOW}[INFO] Creating a virtual environment folder ...${NC}"
mkdir venv
cd venv 
echo "Please, enter the name of the virtual environment you want :"
read VIRTUAL_ENV
echo -e "${YELLOW}[INFO] Creating a virtual environment named $VIRTUAL_ENV${NC}"
python3 -m venv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate
echo -e "${YELLOW}[INFO] Installing all the necessary packages listed on requirements.txt ...${NC}"
pip3 install -r $SCRIPT_DIR/requirements.txt

deactivate

echo -e "${GREEN}[SUCCESS] Virtual environment $VIRTUAL_ENV has been created at $SCRIPT_DIR.${NC}"

cd $SCRIPT_DIR

echo -e "${YELLOW}[INFO] end of installation.${NC}"

chmod +x /env.sh

source env.sh