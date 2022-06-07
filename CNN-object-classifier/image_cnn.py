import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn, optim
from torch.autograd import Variable
# import torch.nn.functional as F
# import torchvision
from torchvision import datasets, transforms, models
from PIL import Image

data_dir = str("images")

# Function that split beween train and test
def load_split_train_test(datadir, valid_size = .2):
 
    train_transforms = transforms.Compose([
                                       #transforms.RandomResizedCrop(224),
                                       transforms.Resize(224),
                                       transforms.ToTensor(),
                                       ])

    test_transforms = transforms.Compose([#transforms.RandomResizedCrop(224),
                                          transforms.Resize(224),
                                          transforms.ToTensor(),
                                      ])

    train_data = datasets.ImageFolder(datadir, transform=train_transforms)
    test_data = datasets.ImageFolder(datadir, transform=test_transforms)

    num_train = len(train_data)
    indices = list(range(num_train))
    split = int(np.floor(valid_size * num_train))
    np.random.shuffle(indices)
    from torch.utils.data.sampler import SubsetRandomSampler
    train_idx, test_idx = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_idx)
    test_sampler = SubsetRandomSampler(test_idx)
    trainloader = torch.utils.data.DataLoader(train_data, sampler=train_sampler, batch_size=16)
    testloader = torch.utils.data.DataLoader(test_data, sampler=test_sampler, batch_size=16)
    return trainloader, testloader

# Split the set betwen train and test
trainloader, testloader = load_split_train_test(data_dir, .2)
print("Different classes : ", trainloader.dataset.classes)

test_transforms = transforms.Compose([transforms.Resize(224),
                                    #transforms.RandomResizedCrop(224),
                                    transforms.ToTensor(),
                                    ])

# Get n random images to display
def get_random_images(num):
    data = datasets.ImageFolder(data_dir, transform=test_transforms)
    classes = data.classes
    indices = list(range(len(data)))
    np.random.shuffle(indices)
    idx = indices[:num]
    from torch.utils.data.sampler import SubsetRandomSampler
    sampler = SubsetRandomSampler(idx)
    loader = torch.utils.data.DataLoader(data, sampler=sampler, batch_size=num)
    dataiter = iter(loader)
    images, labels = dataiter.next()
    return images, labels 

# display n images 
'''images, labels = get_random_images(2)
to_pil = transforms.ToPILImage()
fig=plt.figure(figsize=(5,5))
classes=trainloader.dataset.classes
for ii in range(len(images)):
    image = to_pil(images[ii])
    sub = fig.add_subplot(1, len(images), ii+1)
    plt.axis('off')
    plt.imshow(image)
plt.show()'''


# Determine whether you're using a CPU or a GPU to build the deep learning network.
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if torch.cuda.is_available():               # When using a single GPU (specific case with OSX I guess ...)
    device = "cuda:0"
else:
    device = "cpu"

device = torch.device(device)
model = models.resnet50(pretrained=True)


# Builds all the neurons.
for param in model.parameters():
    param.requires_grad = False

# The parameters of our deep learning model.
model.fc = nn.Sequential(nn.Linear(2048, 512),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),
                                 nn.Linear(512, 2),
                                 nn.LogSoftmax(dim=1))
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.003)
model.to(device)
print('done')

# lmearning params of the model
epochs = 5
steps = 0
running_loss = 0
print_every = 5
train_losses, test_losses = [], []

for epoch in range(epochs):

    epoch += 1

    for inputs, labels in trainloader:

        steps += 1
        print('Training step ', steps)
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        logps = model.forward(inputs)
        loss = criterion(logps, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if steps % print_every == 0:
            test_loss = 0
            accuracy = 0
            model.eval()
            with torch.no_grad():
                for inputs, labels in testloader:
                    inputs, labels = inputs.to(device), labels.to(device)
                    logps = model.forward(inputs)
                    batch_loss = criterion(logps, labels)
                    test_loss += batch_loss.item()
                    
                    ps = torch.exp(logps)
                    top_p, top_class = ps.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

            train_losses.append(running_loss/len(trainloader))
            test_losses.append(test_loss/len(testloader))                    
            print(f"Epoch {epoch}/{epochs}.. "
                  f"Train loss: {running_loss/print_every:.3f}.. "
                  f"Test loss: {test_loss/len(testloader):.3f}.. "
                  f"Test accuracy: {accuracy/len(testloader):.3f}")
            running_loss = 0
            model.train()

# Probabilité de succès / précision du réseau de neuronnes 
precision_accuracy = accuracy/len((testloader))
print("Actual precision of the model is:", round(precision_accuracy*100, 2), "%.")

torch.save(model, 'maskRecognitionModel.pth')
#torch.save({'state_dict': model.state_dict()}, 'checkpoint.pth.tar')
print("Model has been saved.")

# Loading the model 
#model = describe_model()
#checkpoint = torch.load('checkpoint.pth.tar')
#model.load_state_dict(checkpoint['state_dict'])

# Loading model
if torch.cuda.is_available():               # When using a single GPU
    device = "cuda:0"
else:
    device = "cpu"

device = torch.device(device)
model=torch.load('maskRecognitionModel.pth')

# Function that preedict the class of a given image
def predict_image(image):
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = Variable(image_tensor)
    input = input.to(device)
    output = model(input)
    index = output.data.cpu().numpy().argmax()
    return index

# Get random image and their label 
images, labels = get_random_images(5)
# Trasnform them
to_pil = transforms.ToPILImage()
images, labels = get_random_images(5)
fig=plt.figure(figsize=(20,10))

# Predict their class and display image + prediction
classes=trainloader.dataset.classes
for ii in range(len(images)):
    image = to_pil(images[ii])
    index = predict_image(image)
    sub = fig.add_subplot(1, len(images), ii+1)
    res = int(labels[ii]) == index
    sub.set_title(str(classes[index]) + ":" + str(res))
    plt.axis('off')
    plt.imshow(image)
plt.show()