import os.path as osp

import torch
import torch.nn.functional as F

import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import MLP, GINConv

dataset = 'Cora'
path = osp.join(osp.dirname(osp.realpath(__file__)), 'data', dataset)
dataset = Planetoid(path, dataset, transform=T.NormalizeFeatures())
data = dataset[0]


class GIN(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = GINConv(MLP([in_channels, 64, 64]))
        self.conv2 = GINConv(MLP([64, 128, 64]))
        self.conv3 = GINConv(MLP([64, out_channels, out_channels]))

    def forward(self, x, edge_index, edge_weight):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv1(x, edge_index, edge_weight)
        x = F.relu(x)
        x = self.conv2(x, edge_index, edge_weight)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv3(x, edge_index, edge_weight)
        return x


device = torch.device('cuda')
model = GIN(dataset.num_features, dataset.num_classes).to(device)
data = data.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.05, weight_decay=5e-4)


def train(data):
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index, data.edge_attr)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()


@torch.no_grad()
def test(data):
    model.eval()
    out, accs = model(data.x, data.edge_index, data.edge_attr), []
    for _, mask in data('train_mask', 'val_mask', 'test_mask'):
        pred = out[mask].max(1)[1]
        acc = pred.eq(data.y[mask]).sum().item() / mask.sum().item()
        accs.append(acc)
    return accs


loss_hist = []
acc_train_hist = []
acc_valid_hist = []
acc_test_hist = []
for epoch in range(1, 201):
    loss_hist.append(train(data))
    train_acc, val_acc, test_acc = test(data)
    print(f'Epoch: {epoch:03d}, Train: {train_acc:.4f}, Val: {val_acc:.4f}, '
          f'Test: {test_acc:.4f}')
    acc_train_hist.append(train_acc)
    acc_valid_hist.append(val_acc)
    acc_test_hist.append(test_acc)


import pickle
with open('./logs/gin/loss_hist.pkl', 'wb') as f:
    pickle.dump(loss_hist, f)
with open('./logs/gin/acc_train_hist.pkl', 'wb') as f:
    pickle.dump(acc_train_hist, f)
with open('./logs/gin/acc_valid_hist.pkl', 'wb') as f:
    pickle.dump(acc_valid_hist, f)
with open('./logs/gin/acc_test_hist.pkl', 'wb') as f:
    pickle.dump(acc_test_hist, f)
