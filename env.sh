#!/usr/bin/env bash

RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[0;33m'  
GREEN='\033[0;32m'

echo -e "${RED}[WARNING] This script needs to be lauched with 'source' (e.g. source env.sh or . env.sh if execution permission has been granted) !${NC}"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "${YELLOW}[INFO] Moving to the project folder : $SCRIPT_DIR ...${NC}"
cd $SCRIPT_DIR

VIRTUAL_ENV=$(find $SCRIPT_DIR -name "activate")
echo -e "${YELLOW}[INFO] Your virtual environment has been found at : $VIRTUAL_ENV${NC}"
echo -e "${YELLOW}[INFO] Activating the virtual environment ...${NC}"
chmod u+rx,go-w $VIRTUAL_ENV

# 1. Create ProgressBar function
# 1.1 Input is currentState($1) and totalState($2)
function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:                           
# 1.2.1.1 Progress : [########################################] 100%
printf "\rProgress : [${GREEN}${_fill// /█}${_empty// /-}${NC}] ${_progress}%%"

}

# Variables
_start=1

# This accounts as the "totalState" variable for the ProgressBar function
_end=100

# Proof of concept
for number in $(seq ${_start} ${_end})
do
    sleep 0.1
    ProgressBar ${number} ${_end}
done
printf "\n"

activate () {
    VIRTUAL_ENV=$(find $SCRIPT_DIR -name "activate")
    source $VIRTUAL_ENV
}

export -f activate

echo -e "${YELLOW}[INFO] Virtual environment ready to be activated. Type 'activate' in the current shell.${NC}"
