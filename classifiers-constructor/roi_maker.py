# importing the module
import cv2 # type: ignore
import xml.etree.cElementTree as ET
import os
from imutils import paths


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    global mouseX_l, mouseY_l, mouseX_r, mouseY_r
	# checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
        print(x, ' ', y)
        mouseX_l, mouseY_l = x,y

		# displaying the coordinates
		# on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
					str(y), (x,y), font,
				2, (20, 20, 184), 3)
        cv2.imshow('Defining ROI', img)

	# checking for right mouse clicks	
    if event==cv2.EVENT_RBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
        print(x, ' ', y)
        mouseX_r, mouseY_r = x, y

		# displaying the coordinates
		# on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
					str(y), (x,y), font,2,
					(184, 149, 22), 3)
        cv2.imshow('Defining ROI', img)


# Iteration over images
BASE_PATH = "dataset"
ORIG_IMAGES = os.path.sep.join([BASE_PATH, "images"])
ORIG_ANNOTS = os.path.sep.join([BASE_PATH, "annotations"])

positives_text_file = open("pos.txt","w+")

imagePaths = list(paths.list_images(ORIG_IMAGES))

# loop over the image paths
for (i, img_path) in enumerate(imagePaths):
    print("[INFO] processing image {}/{}...".format(i + 1,
		len(imagePaths)))

    k=0
    # Close the window when key q is pressed
    while k!=113:

        # reading the image
        img = cv2.imread(img_path, 1)
        # Make a temporary image, will be useful to clear the drawing
        temp = img.copy()
        # Create a named window
        cv2.namedWindow("Defining ROI")
        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Defining ROI', click_event)
        dimensions = img.shape

        # Display the image
        cv2.imshow('Defining ROI', img)
        k = cv2.waitKey(0)
        # If c is pressed, clear the window, using the dummy image
        if k == ord('c'):
            print('Copying image ...')
            img= temp.copy()
            cv2.imshow('Defining ROI', img)
            print('...Image cleared')
        elif k == ord('p'):
            print(f"Printing coords : {mouseX_l}, {mouseY_l}, {mouseX_r}, {mouseY_r}")
        elif k == ord('d'):
            print('Starting drawing the ROI ...')
            copy_image = temp.copy()
            start_point = (mouseX_l, mouseY_l)
            end_point = (mouseX_r, mouseY_r)
            color = (89, 196, 47)
            thickness = 15
            image_with_rectangle = cv2.rectangle(
                img = img,
                pt1 = start_point,
                pt2 = end_point, 
                color = color, 
                thickness = thickness
            )
            cv2.imshow('ROI Defined', image_with_rectangle)
            print('... ROI drawn')

    filename = img_path.split(os.path.sep)[-1]   
    filename = filename[:filename.rfind(".")]
    annotPath = os.path.sep.join([ORIG_ANNOTS,
		"{}.xml".format(filename)])

    print(f'{filename},\n{annotPath}')

    # building the coorresponding xml file
    annotation = ET.Element("annotation", verified="yes")
    folder = ET.SubElement(annotation, "folder").text = "dataset/images"
    filename = ET.SubElement(annotation, "filename").text = f"{filename}.jpg"
    path = ET.SubElement(annotation, "path").text = f"/Users/val/Desktop/ds-project/interactive_coordinates_image/dataset/images/{filename}"
    source = ET.SubElement(annotation, "source")
    size = ET.SubElement(annotation, "size")
    segmented = ET.SubElement(annotation, "segmented").text = "0"
    object = ET.SubElement(annotation, "object")

    ET.SubElement(source, "database").text = "Unknown"
    ET.SubElement(size, "width").text = f"{img.shape[1]}"
    ET.SubElement(size, "height").text = f"{img.shape[0]}"
    ET.SubElement(size, "depth").text = f"{img.shape[2]}"

    ET.SubElement(object, "name").text = "black surgey mask"
    ET.SubElement(object, "pose").text = "Unspecified"
    ET.SubElement(object, "truncated").text = "0"
    ET.SubElement(object, "difficult").text = "0"

    bndbox = ET.SubElement(object, "bndbox")

    ET.SubElement(bndbox, "xmin").text = f"{mouseX_l}"
    ET.SubElement(bndbox, "ymin").text = f"{mouseY_l}"
    ET.SubElement(bndbox, "xmax").text = f"{mouseX_r}"
    ET.SubElement(bndbox, "ymax").text = f"{mouseY_r}"

    tree = ET.ElementTree(annotation)

    tree.write(annotPath)

    print(f"Image {filename} processed (.xml)")

    # Change the path of the positive images the correspondig one where we create vec file
    positives_text_file.write(f"dataset/imagess/{filename} 1 {mouseX_l} {mouseY_l} {mouseX_r} {mouseY_r}\n")

    print(f"Image {filename} processed (pos.txt)")

positives_text_file.close()

print('All images processed.')