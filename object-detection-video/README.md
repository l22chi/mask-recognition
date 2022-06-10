[![](https://img.shields.io/badge/python-3.8.5-blue.svg?&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-385/) [![](https://img.shields.io/badge/OpenCV-3.4.0-blue?&logo=opencv&logoColor=red)](https://docs.opencv.org/3.4.0/index.html) [![](https://img.shields.io/badge/Docker-20.10.14-blue?&logo=Docker&logoColor=blue)](https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu)


# The live object (mask) detection model


This part aims to use the haarcascade classifiers in order to detect what they were trained on during a live video stream (webcam).

## Structure

```bash
├── object-detection-video
│   ├── classifiers
│   │   ├── haarcascade_frontalface_default.xml
│   │   └── Mouth.xml
│   ├── autorun.sh
│   ├── detect_haarcascade.py
│   └── video_recognition.py
```

## The haarcascade classsifier

The haarcascade classifiers used to detect objects are present in the 'classifiers' subfolder. There are several of them.
By default there is:
- haarcascade_frontalface_default.xml
- Mouth.xml

The first haarcascade classifier is a pre-trained classifier directly available in the OpenCV library which is used to detect the presence of a human face from the front.
The second is also a pre-trained classifier from the OpenCV library but this time used to detect the presence of a human mouth.

Basically, a good idea seemed to combine these two classifiers in a program. Indeed, the goal was initially to detect a human face, then to detect a mouth. If a face was detected but not the presence of a mouth, then it meant that the detected face was wearing a mask, conversely, if the face was detected but the mouth was too, then it indicated that we were not wearing of mask. It was a good idea to detect mask wearing in general.
However, in our project, we wanted to bring an additional dimension which is "the **GOOD** wearing of the mask. This classifier then no longer seemed relevant. Moreover, the classifier being very dependent on the way in which it was trained (the images), the latter did not allow us to obtain the expected results and precision. We therefore decided to train our own haarcascade classifier. By default in the 'classifiers' sub-folder there is a 3rd classifier named 'haarcascade .xml' which is actually the result of the classifier we trained ourselves.
Also, if you carry out yourself the training process of a haarcascade classifier (in the section classifiers-constructor) then yours will be directly saved in this same sub-folder.

## How to use it
It is possible to use these detectors in two ways:
- The first is to let yourself be guided by the autorun.sh which will automatically execute the detection script:

```bash
object-detection-video/autorun.sh
```
- The second is to run the python scripts yourself:

The 'video_recognition.py' script is the script that uses the haarcascade classifiers haarcascade_frontalface_default.xml and Mouth.xml

The 'detect_haarcascade.py' script is the script that uses the classifier we trained or the one you trained in the classifirers-constructor section.

In case you launch the second, you will have to pay attention to the name of the classifier used in the script. It must match the name of the classifier you trained: l.3:

```python
haarcacade_frontface_path = str("classifiers/haarcascade.xml")
```

And in any case, you will also have to pay attention to the following lines:

detect_haarcascade.py l.7 and video_reecognition.py l.21:

```python
cap = cv2.VideoCapture(0)
```
Indeed, the harcoded parameter 'cv2.VideoCapture(0)' is set to 0, which indicates a computer's default webcam. If you use other devices for the video stream then you will have to fumble on the latter.