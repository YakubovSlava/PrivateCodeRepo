### Импорт необходимых библиотек

import torch
import torch.nn as nn
from PIL import Image
import numpy as np
import os
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader
from tqdm import tqdm
from torchvision.utils import save_image
import torch.optim as optim

### Код для сохранения датасета
for path in tqdm(os.listdir('test_set/test_set/')):
    image = Image.open('test_set/test_set/'+path).resize((256, 256))
    image.save('temp.jpeg', 'JPEG', quality=5)
    temp = Image.open('temp.jpeg')
    res = Image.fromarray(np.append(np.array(temp), np.array(image), axis=1))
    res.save('maps/val/'+path)

for path in tqdm(os.listdir('training_set/training_set/')):
    image = Image.open('training_set/training_set/'+path).resize((256, 256))
    image.save('temp.jpeg', 'JPEG', quality=5)
    temp = Image.open('temp.jpeg')
    res = Image.fromarray(np.append(np.array(temp), np.array(image), axis=1))
    res.save('maps/train/'+path)

### Код для чтения данных в датасет

class MyDataset(Dataset):
    def __init__(self, home_dir, val=False):
        super().__init__()
        self.dir = home_dir
        self.all_files = os.listdir(home_dir)
        self.left_right_transform = A.Compose(
            [
                A.Resize(width=256, height=256),
                A.HorizontalFlip(p=0.5 if not val else 0)
            ],
            additional_targets={
                'image0': 'image'
            }
        )
        self.left_transform = A.Compose(
            transforms=[A.ColorJitter(p=0.2 if not val else 0),
                        A.Normalize(mean=[0.5, 0.5, 0.5],
                                    std=[0.5, 0.5, 0.5]),
                        ToTensorV2()]
        )
        self.right_transform = A.Compose(
            transforms=[
                 A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
                 ToTensorV2()
            ]
        )

    def __len__(self):
        return len(self.all_files)

    def __getitem__(self, idx):
        path = os.path.join(self.dir, self.all_files[idx])
        image_array = np.array(Image.open(path))
        left_image = image_array[:, :256, :]
        right_image = image_array[:, 256:, :]
        augumented = self.left_right_transform(image=left_image, image0=right_image)
        left_image, right_image = augumented['image'], augumented['image0']
        left_image = self.left_transform(image=left_image)['image']
        right_image = self.right_transform(image=right_image)['image']
        return left_image, right_image


### Сохранение чекпоинта
def save_model(model, optimizer, filename):
    print('Saving model')
    torch.save({
                'state_dict': model.state_dict(),
                'optimizer': optimizer.state_dict()
                }, filename)

### Загрузка чекпоинта
def load_model(model, optimizer, lr, file):
    print('load model')
    checkpoint = torch.load(file, map_location=device)
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr