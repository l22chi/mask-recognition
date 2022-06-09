import os

def create_neg(path=os.path.dirname(os.path.realpath(__file__)), data_dir='images', classnumber = 0):

    for img in os.listdir(str(path)+'/'+str(data_dir)):
        if not img.startswith('.'):
            if not img.endswith('.webp'):
                if not img.endswith('.crdownload'):
                    line = str(data_dir)+ '/' + str(img) + f', {classnumber}\n'
                    print(line)
                    with open('images/annotations.txt','a') as f:
                        f.write(line)

dataDirs = ['images/mask', 'images/not_mask']

for labels in dataDirs:
    if labels == str(dataDirs[0]):
        create_neg(data_dir=labels)
    else:
        create_neg(data_dir=labels, classnumber=1)