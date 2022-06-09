import os
from matplotlib import transforms
import pandas as pd # type: ignore
import torch
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor, Lambda, transforms
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from PIL import Image


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

transformation = transforms.Compose([transforms.Resize(224),
                                    transforms.Grayscale(3),
                                    ToTensor()])
transformation_target = Lambda(lambda y: torch.zeros(
    2, dtype=torch.float).scatter_(dim=0, index=torch.tensor(y), value=1))
annotations = r'images/annotations.txt'
image_location = r'images'
data = CustomImageDataset(annotations, image_location, transformation, transformation_target)
train_dataloader = DataLoader(data, batch_size=64, shuffle=True)

train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")

img = train_features[0].squeeze()
label = train_labels[0]
fig=plt.figure(figsize=(5,5))
to_pil = transforms.ToPILImage()
plt.axis('off')
plt.imshow(to_pil(img))
plt.show()
print(f"Label: {label}")