import os

def create_neg(path=os.path.dirname(os.path.realpath(__file__))):

    data_dir = 'dataset/images/neg'

    for img in os.listdir(str(path)+'/'+str(data_dir)):
        if not img.startswith('.'):
            if not img.endswith('.webp'):
                if not img.endswith('.crdownload'):
                    line = 'neg/' + str(img) + '\n'
                    print(line)
                    with open('dataset/images/bg.txt','a') as f:
                        f.write(line)

create_neg()