from cProfile import label
import os

def create_neg(data_dir, label_image, path=os.path.dirname(os.path.realpath(__file__))):

    for img in os.listdir(str(path)+'/'+str(data_dir)):
        if not img.startswith('.'):
            if not img.endswith('.webp'):
                if not img.endswith('.crdownload'):
                    line = str(label_image)+ '/' + str(img) + f', {label_image}\n'
                    print(line)
                    with open('images/annotations.txt','a') as f:
                        f.write(line)


dataDirs = ['mask', 'not_mask']

for dir in dataDirs:
    create_neg(data_dir=f'images/{dir}', label_image=str(dir))
        