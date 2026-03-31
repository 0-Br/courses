from genericpath import exists
import torch
import torch.nn as nn
import torch.optim as optim
import data
import models
import utils
import os
from pickle import dump
import argparse
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
import cv2
from torch.optim.lr_scheduler import LinearLR, ExponentialLR, CosineAnnealingLR


from tensorboardX import SummaryWriter
train_writer = SummaryWriter('./logs/train')
valid_writer = SummaryWriter('./logs/val')


# Note that: here we provide a basic solution for training and validation.
# You can directly change it if you find something wrong or not good enough.


def train_model(model, train_set, valid_set, criterion, optimizer, save_dir, num_epochs=20):

    def train(model, train_loader, optimizer, criterion):
        model.train(True)
        total_loss = 0.0
        all_labels = []
        all_probs = []

        # ----------------- 此部分为学习率调整策略 -----------------
        # scheduler = LinearLR(optimizer, 1, 0.2, 10)
        # scheduler = ExponentialLR(optimizer, 0.9)
        # scheduler = CosineAnnealingLR(optimizer, T_max=5, eta_min=2e-5)
        scheduler = CosineAnnealingLR(optimizer, T_max=15, eta_min=2e-5)
        # ----------------- 此部分为学习率调整策略 -----------------

        bar = tqdm(train_loader, desc='train')
        for inputs, labels in bar:
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * inputs.size(0)
            bar.set_postfix(loss=loss.item())
            all_labels.append(labels.cpu().numpy())
            all_probs.append(torch.sigmoid(outputs).cpu().detach().numpy())
        scheduler.step()

        epoch_loss = total_loss / len(train_loader.dataset)
        all_labels = np.concatenate(all_labels)
        all_probs = np.concatenate(all_probs)
        roc_auc = utils.get_roc_auc_score(all_labels, all_probs)

        train_writer.add_scalar('Loss/train', epoch_loss, epoch)
        train_writer.add_scalar('AUC/train', roc_auc, epoch)

        return epoch_loss, roc_auc

    def valid(model, valid_loader, criterion):
        model.train(False)
        total_loss = 0.0
        all_labels = []
        all_probs = []
        for inputs, labels in tqdm(valid_loader, desc='val'):
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * inputs.size(0)
            all_labels.append(labels.cpu().numpy())
            all_probs.append(torch.sigmoid(outputs).cpu().numpy())

        epoch_loss = total_loss / len(valid_loader.dataset)
        all_labels = np.concatenate(all_labels)
        all_probs = np.concatenate(all_probs)
        roc_auc = utils.get_roc_auc_score(all_labels, all_probs)

        valid_writer.add_scalar('Loss/valid', epoch_loss, epoch)
        valid_writer.add_scalar('AUC/valid', roc_auc, epoch)

        return epoch_loss, roc_auc

    best_roc_auc = 0.0
    best_epoch = 0
    train_loss_alltime = []
    train_auc_alltime = []
    valid_loss_alltime = []
    valid_auc_alltime = []

    if not exists(save_dir):
        os.makedirs(save_dir)
    for epoch in range(num_epochs):
        print('epoch:{:d}/{:d}'.format(epoch, num_epochs))
        print('*' * 100)
        train_set.resample()

        # train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=10)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=4)
        train_loss, train_roc_auc = train(model, train_loader, optimizer, criterion)
        print("training: {:.4f}, {:.4f}".format(train_loss, train_roc_auc))

        # valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size, shuffle=False, num_workers=10)
        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=batch_size, shuffle=False, num_workers=4)
        with torch.no_grad():
            valid_loss, valid_roc_auc = valid(model, valid_loader, criterion)
        print("validation: {:.4f}, {:.4f}".format(valid_loss, valid_roc_auc))
        print()
        torch.save(model, os.path.join(save_dir, "model_%d.pt" % epoch))
        if valid_roc_auc > best_roc_auc:
            best_roc_auc = valid_roc_auc
            best_model = model
            best_epoch = epoch
            torch.save(best_model, os.path.join(save_dir, 'best_model.pt'))

        train_loss_alltime.append(train_loss)
        train_auc_alltime.append(train_roc_auc)
        valid_loss_alltime.append(valid_loss)
        valid_auc_alltime.append(valid_roc_auc)

    with open('./checkpoints/main.pkl', 'wb') as f:
        dump({'train_loss': train_loss_alltime, 'train_auc': train_auc_alltime, 'valid_loss': valid_loss_alltime, 'valid_auc': valid_auc_alltime}, f)
    print("best score: %f" % best_roc_auc)
    print("best model: model_%d" % best_epoch)


def test_model(model, test_loader, criterion):
    with torch.no_grad():
        model.train(False)
        total_loss = 0.0
        all_labels = []
        all_probs = []
        for inputs, labels in tqdm(test_loader, desc='test'):
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            total_loss += loss.item() * inputs.size(0)
            all_labels.append(labels.cpu().numpy())
            all_probs.append(torch.sigmoid(outputs).cpu().numpy())

    epoch_loss = total_loss / len(test_loader.dataset)
    all_labels = np.concatenate(all_labels)
    all_probs = np.concatenate(all_probs)
    roc_auc = utils.get_roc_auc_score(all_labels, all_probs)
    print(epoch_loss, roc_auc)


if __name__ == '__main__':

    seed = 42
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)

    # os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    parser = argparse.ArgumentParser(description='hw1')
    parser.add_argument('--data_dir', type=str, default='H:/NIH-Chest-X-ray-dataset/', help='dataset path')
    parser.add_argument('--save_dir', type=str, default='./checkpoints/', help='model save path')
    parser.add_argument('--pretrained', default=False, action='store_true', help='whether to use pretrained model')
    args = parser.parse_args()

    # about model
    num_classes = 15

    # about data
    data_dir = args.data_dir  # You need to specify the data_dir first
    input_size = 224

    # about batch_size
    batch_size = 256 # for resnet18
    # batch_size = 64 # for MyConvNeXt_v1
    # batch_size = 64 # for MyConvNeXt_v2
    # batch_size = 128 # for MyConvNeXt_v3
    # batch_size = 64 # for MyDenseNet

    # about training
    num_epochs = 20
    lr = 0.0001

    # model initialization
    model = models.model_A(num_classes=num_classes, pretrained=args.pretrained) # resnet18
    # model = models.model_B(num_classes)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    print(device)

    # data preparation
    train_set = data.XRaysTrainDataset(data_dir=data_dir, data_list='train_val_list.txt',
                                       transform=data.data_transforms['train'])
    valid_set = data.XRaysTrainDataset(data_dir=data_dir, data_list='test_list.txt',
                                       transform=data.data_transforms['test'])

    # optimizer
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # loss function
    criterion = nn.BCEWithLogitsLoss()
    train_model(model, train_set, valid_set, criterion, optimizer, args.save_dir, num_epochs=num_epochs)
