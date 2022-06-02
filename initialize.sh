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

    echo -e "${YELLOW}[INFO] Installing opencv and all its dependencies${NC}"
    brew install opencv
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

    echo -e "${YELLOW}[INFO] Installing git and all its dependencies${NC}"
    brew install git
    echo -e "${GREEN}[SUCCESS] Succefully installed${NC}"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then

    sudo apt-get update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update

    if ! python3 -c 'import sys; assert sys.version_info <= (3,7)' > /dev/null; then
        sudo apt install python3.8
    fi

    sudo apt-get install python3-pip
    sudo apt-get install libopencv-dev
    sudo apt-get install git

fi

cd $SCRIPT_DIR

echo -e "${RED}[WARNING] You need to have Docker installed to continue !${NC}"

echo -e "${YELLOW}[INFO] Building Docker image FROM dockerfile : $CURRENT${NC}"

sudo docker build -t opencv-image docker

echo -e "${GREEN}[SUCCESS] Docker image has been built.${NC}"

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