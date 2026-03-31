from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
import os
import cv2
import torch
from tqdm import tqdm
from collections import defaultdict
import numpy as np

# Note that: here we provide a basic solution for loading data and transforming data.
# You can directly change it if you find something wrong or not good enough.

# the mean and standard variance of imagenet dataset
# mean_vals = [0.485, 0.456, 0.406]
# std_vals = [0.229, 0.224, 0.225]

data_transforms = {
    'train': transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        transforms.RandomHorizontalFlip(0.5),
        # transforms.RandomErasing(0.5),
        transforms.GaussianBlur(3),
    ]),
    'test': transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]),
}

all_classes = [
    'No Finding',
    'Infiltration',
    'Effusion',
    'Atelectasis',
    'Nodule',
    'Mass',
    'Pneumothorax',
    'Consolidation',
    'Pleural_Thickening',
    'Cardiomegaly',
    'Emphysema',
    'Edema',
    'Fibrosis',
    'Pneumonia',
    'Hernia',
]


class XRaysTrainDataset(Dataset):
    def __init__(self, data_dir, data_list='train_val_list.txt', transform=data_transforms['train']):
        self.data_dir = data_dir
        self.transform = transform

        self.get_labels(data_dir)
        self.get_data_list(data_dir, data_list)
        self.resample_data_list = None

    def get_labels(self, data_dir):
        self.labels = {}
        lines = open(os.path.join(data_dir, 'Data_Entry_2017_v2020.csv'), 'r').readlines()
        for line in tqdm(lines[1:], desc="Loading labels"):
            filename, labels = line.split(',')[:2]
            labels = labels.split('|')
            self.labels[filename] = labels

    def get_data_list(self, data_dir, data_list):
        self.data_list = []
        lines = open(os.path.join(data_dir, data_list), 'r').readlines()
        for line in tqdm(lines, desc="Loading data list"):
            filename = line.strip()
            self.data_list.append(filename)

    def resample(self):
        max_examples_per_class = 10000  # its the maximum number of examples that would be sampled in the training set for any class
        self.resample_data_list = []
        class_count = defaultdict(int)
        total_len = len(self.data_list)

        for i in tqdm(list(np.random.choice(range(total_len), total_len, replace=False)), desc='resample'):
            labels = self.labels[self.data_list[i]]
            # ultra minority Hernia as special case
            if 'Hernia' in labels or sum([class_count[l] < max_examples_per_class for l in labels]) == len(labels):
                self.resample_data_list.append(self.data_list[i])
                for l in labels:
                    class_count[l] += 1

        print('resample class_count: ', class_count)
        print('len of resample_data_list: ', len(self.resample_data_list))

    def __len__(self):
        if self.resample_data_list is not None:
            return len(self.resample_data_list)
        else:
            return len(self.data_list)

    def __getitem__(self, index):
        if self.resample_data_list is not None:
            filename = self.resample_data_list[index]
        else:
            filename = self.data_list[index]

        img = cv2.imread(os.path.join(self.data_dir, 'images_224', filename))
        labels = self.labels[filename]

        target = torch.zeros(len(all_classes))
        for lab in labels:
            lab_idx = all_classes.index(lab)
            target[lab_idx] = 1

        if self.transform is not None:
            img = self.transform(img)

        return img, target
