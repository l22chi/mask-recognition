[![](https://img.shields.io/badge/python-3.8.5-blue.svg?&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-385/) [![](https://img.shields.io/badge/OpenCV-3.4.0-blue?&logo=opencv&logoColor=red)](https://docs.opencv.org/3.4.0/index.html) [![](https://img.shields.io/badge/Docker-20.10.14-blue?&logo=Docker&logoColor=blue)](https://hub.docker.com/repository/docker/l22chi/opencv-ubuntu)

# How to build a haarcascade trained file


## Structure

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
│   ├── makeNeg.py
│   ├── roi_maker.py
│   └── take_photos.py
```