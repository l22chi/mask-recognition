[![](https://img.shields.io/badge/python-3.8.5-blue.svg?&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-385/) [![](https://img.shields.io/badge/OpenCV-3.4.0-blue?&logo=opencv&logoColor=red)](https://docs.opencv.org/3.4.0/index.html) [![](https://img.shields.io/badge/Docker-20.10.14-blue?&logo=Docker&logoColor=blue)](https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu)

# How to build a haarcascade trained file

These scripts allow you to do several things:
- Create the info file for the negatives (bg.txt) indicating the relative path of the negative images of the model, using the script 'makeNeg.py'
- Create the info file for the positive lees (info.txt) indicating the relative path of the positive images of the model, the number of positive objects on the image and their positions on the latter, using the script 'roi_maker .py'
- Create a positive set of images using the user's webcam, with the script 'take_photos.py'

The different steps and different processes described below are simplified. That is to say that all the command parameters are not used, and that the specified parameters are chosen arbitrarily by way of example and minimum configuration. For more information I refer you to [the official OpenCV documentation](https://docs.opencv.org/4.x/dc/d88/tutorial_traincascade.html).

## Global use information

### Structure

```bash
├── classifiers-constructor
│   ├── dataset
│   │   ├── annotations
│   │   └──  images
│   │        ├── masked
│   │        ├── neg
│   │        ├── samples
│   │        ├── bg.txt
│   │        └── info.txt
│   ├── README.md
│   ├── autorun.sh
│   ├── makeNeg.py
│   ├── roi_maker.py
│   └── take_photos.py
```

### About the structure

In this sub-directory, there is an image folder containing 3 sub-folders as well as the two information files.

Regarding the 3 subfolders, the 'masked' folder is intended to accommodate the positive images of the model, the 'neg' folder the negative images, and the 'samples' folder the positive images created from the distortion of a positive image on several negative images.
It is important to respect the locations and destinations of each image, file and folder because when creating the haarcascade with OpenCV, relative paths are important.

Please note that information files are by default in '.txt' format but '.dat' and '.info' formats are also accepted.

### take_photos.py

When this script is launched, it accesses the user's webam (noted that permission will be requested) and takes care of taking by default:
- 200 tagged photos of the 'masked' class every 3 seconds (default configuration)
You can change the parameters of the script in order to adapt the model to your needs:
- ***number_imgs***: number of images taken per class (200 by default)
- ***labels***: list comprising the titles of the desired classes (by default 'masked' only)

By default the waiting time between taking two photos is 3 seconds but you can change it. The waiting time for class change is 10 seconds (you can also change it).

Please note that the OpenCV library (import cv2) allows python to access your webcam. Depending on the user's configuration, it is likely that line 23 needs to be changed:

> cap = cv2.VideoCapture(0)

By default the webcams are configured on port '0' but this may be different (especially if you are using a camera or a webcam other than the one natively existing on your device.

### roi_maker.py

This script allows the user to create two types of files in parallel:

- the positive images info file (.txt, .dat, .info)
- positive images info files (.xml)

This project uses different templates, and some templates use different info files than the default ones (e.g. .txt). This is notably the case of the model used by Tensorflow and Keras which use the .xml format to obtain the path of the positive images as well as the position of the region of interest on the latter. Regarding this format, an .xml file is created for each positive image in the 'masked' folder.
This script therefore makes it possible to prepare the info files for the two types of models in parallel.

### The different possibilities for creating info files

When I started getting interested in creating these info files, I didn't know about the different tools that existed. That's why I had created this script 'roi_maker.py'.
It was only later that I became aware of different tools allowing me to obtain the same files:

The first is the 'label image' python library which allows you to obtain info files in .xml format

The second is a tool provided by OpenCV named:

> opencv_annotations

The latter allows you to create the default info file (.txt, .dat, .info) allowing you to build the haarcascade file. It is available even in the most recent versions of OpenCV and allows, using a graphic interface, to indicate where the regions of interest of each image are.

Finally, the last one I had the opportunity to work with is 'SuperAnnotate', which is a very powerful image / video annotation tool via graphical interface (it was introduced by OpenCV in this article: [OpenCV - SuperAnnotate](https://opencv.org/superannotate-desktop/), and you can have a free version as a professional or a student).

## How to use opencv_annotations (opencv annotation tool)

Regarding the OpenCV annotation tool, you will find its usage tutorial [here](https://docs.opencv.org/4.x/dc/d88/tutorial_traincascade.html), it is written for OpenCV 4.X versions but still valid and functional for earlier versions. However, we will see here how to use it:

At first you need to have a version of OpenCV (if you don't know how to do it, I refer you to the previous explanations of this project or to the official documentation of OpenCV).

You then need to have several positive images (in the 'masked' folder)

**Note**: if you want to build a robust model based on haar features, you need several hundreds / thousands of positive images, and annotate them for example using this tool. on the other hand, if you want to build your model from a single image, to which you will apply distortions, a single and a single image containing only the object you wish to detect is necessary, in this precise case, the dimensions of the image, corresponding only to the unique dimensions of the region of interest, you can skip this annotation step, and proceed to the step of creating positive samples (with the opencv_createsamples tool) below. Otherwise, please follow this step.

If you have a properly built version of OpenCV then you can use the following command:

```bash
opencv_annotation --annotations dataset/images/info.txt --images dataset/images/masked
```

If you do not have a properly built version (especially if you have an error indicating that the command 'opencv_annotation' does not exist') please use the following command (you indicate in fact the path of the OpenCV executable):

```bash
opencv/build/bin/opencv_annotation --annotations=/path/to/annotations/file.txt --images=/path/to/image/folder/
```

Please note that for the latter you must have OpenCV mounted on your local machine, if you are using the stable image of OpenCV 3.4.0 via Docker, you will first need to have transferred your poitive images into the Docker container (see the part on Docker, and the COPY command in the docker file). You will also need to adapt the paths to your configuration.

## How to create positive samples from one image (opencv_createamples)

Note: to use the opencv_createsamples tool, you must have a stable version of OpenCV 3.4.X (versions beyond which, these tools written in C have not been translated into C++ and are therefore not compiled and usable directly). To have such a stable and functional version of OpenCV, I refer you to the previous part of this directory concerning the installation of OpenCV 3.4.0 on a local machine or via a Docker container. If you have good skills in C or C++, then .... it's up to you, go for it!

If you choose to create multiple positive samples via this tool and from a single positive image, you will need to have negative images beforehand (any negative image is good, the only conditions to respect are the number of negative images: equal to at least the number of positive images if you have several positive images yourself, or at least equal to the number of positive images that you want created from the distortion; the size of the negative images: in general, a size is taken which corresponds on average to the size of the region of interest of the positive images, or else a size at least equal to the size of the only positive image in the case of createsamples).

opencv_annotations provide you the information .txt file required the create the vec file. Concerning the negative images info file, you will have to create it in any case (see sccript 'makeNeg.py'). The vec file is required to train thee haarcascade file. The opencv_createsamples command provide you the vec file.

Before continuing to explain how to use this OpenCV tool, you must understand a fact about the size of the ROIs (Regions Of interests) that will be created during the multiple distortions of the base image in order to create positive samples at the opencv_createsamples command help:

If you decide to use the tool: opencv_createsamples, then you will create positive samples (positive images) from a single image, applying distortions to it and overlaying it on negative images. During this process, you have the possibility to choose in parameter the size of the samples in output (h: height and w: width). By default, these parameters are both set to 24 pixels. Since all these samples will therefore be 24x24 pixels in size, the detection size when using the haarcascade file will be 24 by 24 pixels in size (because all training sizes are 24 by 24). It is important to understand that if the size of the samples created is h=24 by w=24, the haarcascade training will take as input the parameters h=24 and w=24 (h and w of createsamples and traincascade are different, then traincascaade will fail) and the debtction when using the haarcascade will be h=24 and w=24.
If you want to increase the detection size of the haarcascade, you must increase the size of the input parameters h and w during its training and therefore increase the output size h and w of the samples created. However, the more these parameters are increased, the longer the duration of haarcascade training will take (it is already a time-consuming operation, to train you, or test the model, recommended average sizes are for example h= 20 and w=20 pixels). 

Knowing all this, you can run the following command to create positive samples and create the vec file corresponding:

```bash
opencv_createsamples -vec pos.vec -img dataset/images/masked/masked.jpg -bg dataset/images/bg.txt -w 24 -h 24 -num 1950
```

Note: you can choose the number of positive images to create with the parameter: -num. In this configuration the number of positive images to be output is 1950 (which means that the number of negative images must be at least equal to 1950, 2000 would be a good number guaranteeing the security of the procedure).


If you already have your positive images and you want to create the vector file to train the haacascade file, then use the following command:

```bash
opencv_createsamples -vec pos.vec --info dataset/images/info.txt -num 100
```
Remarks :
- The indication of ***w*** and ***h*** undergoes the same remarks as stated previously
- ***num*** corresponds to the number of positive images to use to create the .vec file (it must be at most equal to the number of positive images you have)
- If your OpenCV is misconfigured (e.g. "error witth opencv_createsamples, command not found" you may need to indicate the path to the executable and change the other parameter paths accordingly, for example:
```bash
opencv/build/bin/opencv_createsamples -vec pos.vec --info dataset/images/info.txt
```
If you happen to have OpenCV built on your local machine.

## How to create haarcascade trained file (opencv_traincascade)

You should now have the following:
- a pos.vec file (containing the positive samples)
- a bg.txt file (file containing the negative samples)

The process now consists of training the model and saving it in .xml format (haarcascade.xml). This is the simplest step but also the longest and the most resource-intensive. It is strongly advised to perform this step with small parameter values ​​in order to see and understand how this step behaves before going to the next level.

To use the opencv_traincascade tool, you must enter these different parameters:
- ***data***: the location where you want this file to be saved
- ***vec***: the location of the file containing the positive samples
- ***bg***: the location of the file containing the negative samples
- ***numPos***: the number of positive images to use (concerning this parameter, it will inform you of a number of positive images to use **LOWER** than the number of positive images you have, because if the training of a haarcascade step runs out of images, training stops, no longer having positive images)
- ***numNeg***: the number of negative images to use (must be equal to half the number of positive samples to be used)
- numStages: the number of stages to train (the equivalent of epochs, the larger it is, the more time-consuming the operation will be)
- ***w*** & ***h***: size of the training samples (they must be exactly the same size as during the sample creation process (opencv_createsamples, the larger they were during the sample creation process, the more this operation will be time consuming

In case you used opencv_createsamples:

```bash
opencv_traincascade -data  ../object-detection-(video)/classifiers -vec pos.vec -bg dataset/images/bg.txt -numPos 1800 -numNeg 900 -numStages 10 -w 24 -h 24
```

In case you didn't use opencv_createsamples:

```bash
opencv_traincascade -data  ../object-detection-(video)/classifiers -vec pos.vec -bg dataset/images/bg.txt -numPos 100 -numNeg 50 -numStages 10
```

In case OpenCV is misconfigured:

```bash
opencv/build/bin/opencv_traincascade -data  ../object-detection-(video)/classifiers -vec pos.vec -bg dataset/images/bg.txt -numPos 100 -numNeg 50 -numStages 10
```

### Gain-train the model

This step consists of making training gains. You can start from the haarcascade.xml file trained by the opencv_traincasscade command and train the model on more stages. for example, you have specified -numStages 10, you can start from numStages 10 and go to numStages 20. To do this, you just need to relaunch the command, this time specifying: numStages 20, which gives:

```bash
opencv_traincascade -data  ../object-detection-(video)/classifiers -vec pos.vec -bg dataset/images/bg.txt -numPos 1800 -numNeg 900 -numStages 20 -w 24 -h 24
```
But **beware** , in order for this to work, you must invoke the command in the same way as the previous time (i.e. without changing any parameters). Otherwise it will lead to a different haarcascade.
You will also have to be careful not to over-fit your model.

### Optimize the execution time

In order to optimize the execution time of the haarcascade training command (opencv_train cascace) you can perform two processes.

- Make a swap (by default this option is disabled in 'autorun.sh'
- Set buffer sizes in the arguments of the opencv_traincascade command)

#### To make a swap:

```bash
#OTHER SESSION at root
apt-get install htop
#command to see processuss running RAMs etc
htop

crontab -e
2

#at the end of the file 

* * * * * sudo echo 1 > /proc/sys/vm/dop_caches
* * * * * sudo echo 2 > /proc/sys/vm/dop_caches
* * * * * sudo echo 3 > /proc/sys/vm/dop_caches

#ctrl + x, yes to save

service cron restart
htop
```

Note: you are not obliged to use the htop command, the latter just allows you to have an overview of the behavior. You can also use top instead of htop (top being now natively present).

#### To set the buffers size


In order to specify the size of the buffers and to speed up / optimize the execution time, you can specify the following parameters:

- precalcValBufSize ***precalculated_vals_buffer_size_in_Mb*** : Size of buffer for precalculated feature values (in Mb). The more memory you assign the faster the training process, however keep in mind that -precalcValBufSize and -precalcIdxBufSize combined should not exceed you available system memory.
- precalcIdxBufSize ***precalculated_idxs_buffer_size_in_M*** : Size of buffer for precalculated feature indices (in Mb). The more memory you assign the faster the training process, however keep in mind that -precalcValBufSize and -precalcIdxBufSize combined should not exceed you available system memory.
- numThreads ***max_number_of_threads*** : Maximum number of threads to use during training. Notice that the actual number of used threads may be lower, depending on your machine and compilation options. By default, the maximum available threads are selected if you built OpenCV with TBB support, which is needed for this optimization.

## Or, let yourself be guided by the automatic training of the haarcascade file (autorun.sh)

If you want to perform these steps automatically, you can run 'autorun.sh' and let yourself be guided. Please, however, check the content of this script to be sure that it corresponds to your needs / configurations.
The default values ​​of 'autorun.sh' are those required for a minimum training configuration of a haarcascade file.