import cv2
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import data
import models

# from tensorboardX import SummaryWriter
# writer = SummaryWriter('./structure')


dict_labels = {}
lines = open('./NIH-Chest-X-ray-dataset/Data_Entry_2017_v2020.csv', 'r').readlines()
for line in lines[1:]:
    filename, labels = line.split(',')[:2]
    labels = labels.split('|')
    dict_labels[filename] = labels

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.load('./checkpoints/best_model.pt')
model.eval()
model.eval()
model.to(device)
criterion = nn.BCEWithLogitsLoss()

'''
model = torch.load('./cache/FINAL/checkpoints/best_model.pt')
input = torch.randn((1, 3, 224, 224)).to(device)
model.train()
writer.add_graph(model, input)
pred = model(input)
'''

def load_image(img):
    img_tensor = data.data_transforms['test'](img)
    img_tensor.requires_grad_()
    img_tensor = img_tensor.unsqueeze(0)

    target = torch.zeros(1, len(data.all_classes))
    for lab in labels:
        lab_idx = data.all_classes.index(lab)
        target[0][lab_idx] = 1

    return img_tensor.to(device), target.to(device)


def visualize_conv_features(img, save_path):
    conv_layers = []
    conv_weights = []
    img, target = load_image(img)

    for child in model.children():
        if type(child) == nn.Conv2d:
            conv_weights.append(child.weight)
            conv_layers.append(child)
        elif type(child) == nn.Sequential:
            for j in range(len(child)):
                for grand_child in child[j].children():
                    if type(grand_child) == nn.Conv2d:
                        conv_weights.append(grand_child.weight)
                        conv_layers.append(grand_child)

    outputs = [img]
    features = []

    for layer in conv_layers:
        img = layer(img)
        outputs.append(img)
    for feature_map in outputs:
        gray_scale = torch.sum(feature_map.squeeze(0), 0) / feature_map.shape[0]
        features.append(gray_scale.data.cpu().numpy())

    fig = plt.figure(figsize=(50, 30), dpi = 300)
    for i, feature in enumerate(features):
        ax = fig.add_subplot(3, 6, i + 1)
        plt.imshow(feature)
        ax.axis("off")
        if i == 0:
            ax.set_title('[input]', fontsize=30)
        else:
            ax.set_title('[conv2d] %d' % i, fontsize=30)

    plt.savefig(save_path, bbox_inches='tight')


def visualize_saliency(img, layer, alpha, save_path):

    img_tensor, target = load_image(img)
    out = model(img_tensor)
    loss = criterion(out, target)
    grad_list = []
    def print_grad(grad):
        grad_list.append(grad)
    img_tensor.register_hook(print_grad)
    loss.backward()

    saliency_map = (abs(grad_list[layer])).squeeze(0).detach().cpu().numpy()
    saliency_map = np.mean(saliency_map, axis=0)

    maximum, minimum = np.max(saliency_map), np.min(saliency_map)
    saliency_map = (saliency_map - minimum) / (maximum - minimum)
    saliency_map = np.uint8(255 * saliency_map)
    saliency_map = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)

    cv2.imwrite(save_path, saliency_map * alpha + img)


if __name__ == '__main__':

    '''
    img = cv2.imread('./NIH-Chest-X-ray-dataset/images_224/00000001_000.png')
    visualize_conv_features(img, 'conv_features.png')

    for i in range(1, 10):
        img = cv2.imread('./NIH-Chest-X-ray-dataset/images_224/0000000%d_000.png' % i)
        visualize_saliency(img, 0, 0.4, 'saliency_map_%d.png' % i)
    '''
    pass
