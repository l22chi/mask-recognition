import cv2 # type: ignore
import uuid
import time
import os

labels = ['masked']
number_imgs = 200

IMAGES_PATH = os.path.join('dataset','images')

if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.system(f'mkdir -p {IMAGES_PATH}')
    elif os.name == 'nt':
        os.system(f'mkdir {IMAGES_PATH}')
for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.system(f'mkdir {path}')


for label in labels:
    cap = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label))
    time.sleep(10)
    for imgnum in range(number_imgs):
        print('Collecting image {}'.format(imgnum))
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()