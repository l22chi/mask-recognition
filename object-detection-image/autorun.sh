#!/bin/bash

NC='\033[0m' # No Color
YELLOW='\033[0;33m'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "${YELLOW}[INFO] Moving to the project folder : $SCRIPT_DIR ...${NC}"
cd $SCRIPT_DIR

echo -e "${YELLOW}[INFO] Running selective_search.py ...${NC}"
echo "Please enter the name of the image you want to detect an object on (e.g. :image.jpg)"
read IMAGE_NAME

echo "Do you want to choose params ? (y/n)"
read ANSWER
if [[ "$ANSWER" == "y" ]]; then

    echo "Choose your minimum probability to consider a classification/detection (0 to 1, e.g. : 0.9)"
    read MIN_PROB
    echo -e "${YELLOW}[INFO] The minimum probability you chose is : $MIN_PROB${NC}"

    echo "Choose the ROI size in pixeel, e.g. : (200, 150)"
    read ROI_SIZ
    echo -e "${YELLOW}[INFO] The ROI size you chose is : $ROI_SIZ${NC}"

    echo "Whether or not to show extra visualizations for debugging (y/n) ?"
    read EXTRA_VIZU

    if [[ "$EXTRA_VIZU" == "y" ]]; then

        echo "How much bounding box you want to see ? (to activate, must be at least >0)"
        read BOUNDING_BOXES
        echo -e "${YELLOW}[INFO] The exra visualizations you chose is : $BOUNDING_BOXES${NC}"
        echo -e "${YELLOW}[INFO] executing script ...${NC}"
        python detect_with_classifier.py --image $IMAGE_NAME --size $ROI_SIZ --min-conf $MIN_PROB --visualize $BOUNDING_BOXES

    elif [[ "$EXTRA_VIZU" == "n" ]]; then

        echo -e "${YELLOW}[INFO] executing script ...${NC}"
        python detect_with_classifier.py --image $IMAGE_NAME --size $ROI_SIZ --min-conf $MIN_PROB
    fi

elif [[ "$ANSWER" == "n" ]]; then

    echo -e "${YELLOW}[INFO] executing script ...${NC}"
    python detect_with_classifier.py --image $IMAGE_NAME
fi

echo -e "${YELLOW}[INFO] end of script.${NC}"