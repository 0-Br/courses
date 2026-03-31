import os.path as osp

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from sklearn.manifold import TSNE

from torch_geometric.datasets import Planetoid
from torch_geometric.nn import Node2Vec

dataset = 'Cora'
path = osp.join(osp.dirname(osp.realpath(__file__)), 'data', dataset)
dataset = Planetoid(path, dataset)
data = dataset[0]

device = torch.device('cuda')
model = Node2Vec(data.edge_index, embedding_dim=128, walk_length=20,
                 context_size=10, walks_per_node=10,
                 num_negative_samples=1, p=1, q=1, sparse=True).to(device)

loader = model.loader(batch_size=128, shuffle=True, num_workers=0)
optimizer = torch.optim.SparseAdam(list(model.parameters()), lr=0.01)


def train():
    model.train()
    total_loss = 0
    for pos_rw, neg_rw in loader:
        optimizer.zero_grad()
        loss = model.loss(pos_rw.to(device), neg_rw.to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def test():
    model.eval()
    z = model()
    acc = model.test(z[data.train_mask], data.y[data.train_mask],
                     z[data.test_mask], data.y[data.test_mask],
                     max_iter=150)
    return acc


loss_hist = []
acc_hist = []
for epoch in range(1, 201):
    loss = train()
    acc = test()
    print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Acc: {acc:.4f}')
    loss_hist.append(loss)
    acc_hist.append(acc)

import pickle
with open('./logs/node2vec/loss_hist.pkl', 'wb') as f:
    pickle.dump(loss_hist, f)
with open('./logs/node2vec/acc_hist.pkl', 'wb') as f:
    pickle.dump(acc_hist, f)


@torch.no_grad()
def visualize(color_list):
    model.eval()
    z = model(torch.arange(data.num_nodes, device=device))
    z = TSNE(n_components=2).fit_transform(z.cpu().numpy())
    y = data.y.cpu().numpy()

    plt.figure(figsize=(8, 8))
    for i in range(dataset.num_classes):
        plt.scatter(z[y == i, 0], z[y == i, 1], s=20, color=color_list[i])
    plt.axis('off')
    plt.savefig('visualization.png')


color_list = [
    '#ffc0cb', '#bada55', '#008080', '#420420', '#7fe5f0', '#065535',
    '#ffd700'
]
visualize(color_list)
