import os
from matplotlib import transforms
import pandas as pd # type: ignore
import torch
from torch.utils.data import Dataset, random_split
from torchvision.transforms import ToTensor, Lambda, transforms
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from PIL import Image
from torch import nn
import torchvision
import numpy as np

# Custom dataset class
class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path)
        label = self.img_labels.iloc[idx, 1]
        # maybe add the class
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


# Custom NN class
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.cnn_layers = nn.Sequential(
            # Defining a 2D convolution layer
            nn.Conv2d(1, 4, kernel_size=3),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
            # Defining another 2D convolution layer
            nn.Conv2d(4, 4, kernel_size=3),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
        )

        self.linear_layers = nn.Sequential(
            # 4 channels out with size of 54 by 98 (corresponding to an image of 224*398)
            nn.Linear(54 * 98 * 4, 2)
        )


    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        logits = self.linear_layers(x)
        return logits

# Optimizing model parameters (train)
def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 10 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


# Optimizing model parameters (test)
def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


def launch_train_model(image_size = 224, learning_rate = 1e-3, batch_size = 100, epochs = 1):

    transformation = transforms.Compose([transforms.Resize(image_size),
                                    transforms.Grayscale(1),
                                    ToTensor()])
    transformation_target = Lambda(lambda y: torch.zeros(
        2, dtype=torch.float).scatter_(dim=0, index=torch.tensor(y), value=1))
    annotations = r'images/annotations.txt'
    image_location = r'images'
    data = CustomImageDataset(annotations, image_location, transformation, transformation_target)
    train_size = int(0.8 * len(data))
    test_size = len(data) - train_size
    train_dataset, test_dataset = random_split(data, [train_size, test_size])
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset)
    train_features, train_labels = next(iter(train_dataloader))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    # Building the model with a loss function and an optimizer
    model = NeuralNetwork().to(device)
    print(f"Model structure: {model}\n\n")
    for name, param in model.named_parameters():
        print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")
    loss_fn = nn.CrossEntropyLoss()
    # optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Optimizing model parameters
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer)
        test_loop(test_dataloader, model, loss_fn)
    print("Done!")

    # Saving the model weights
    torch.save(model, 'model.pth')


if __name__ == "__main__":

    launch_train_model()