#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[0;33m'  
GREEN='\033[0;32m'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "${YELLOW}[INFO] Moving to the project folder : $SCRIPT_DIR ...${NC}"
cd $SCRIPT_DIR

echo -e "${YELLOW}[INFO] executing script ...${NC}"

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

#python detect_haarcascade.py
python video_recognition.py

echo -e "${YELLOW}[INFO] end of script.${NC}"