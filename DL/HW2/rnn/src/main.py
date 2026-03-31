import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

import data
import model

import argparse
import time
import os
from genericpath import exists

from tensorboardX import SummaryWriter
train_writer = SummaryWriter('./logs/train')
valid_writer = SummaryWriter('./logs/val')


# feel free to add some other arguments
parser = argparse.ArgumentParser(description='PyTorch Language Model')
parser.add_argument('--num_epochs', type=int, default=40, help='upper epoch limit')
parser.add_argument('--train_batch_size', type=int, default=20, metavar='N', help='train batch size')
parser.add_argument('--eval_batch_size', type=int, default=10, metavar='N', help='eval batch size')
parser.add_argument('--max_sql', type=int, default=35, help='sequence length') # you can increase the seqence length to see how well the model works when capturing long-term dependencies
parser.add_argument('--structure', type=str, default='GRU', help='structure of RNN')
parser.add_argument('--num_layers', type=int, default=2, help='layers number')
parser.add_argument('--input_size', type=int, default=256, help='input_size')
parser.add_argument('--hidden_size', type=int, default=256, help='hidden_size')
parser.add_argument('--lr', type=float, default=1e-3, help='learning rate')
parser.add_argument('--seed', type=int, default=42, help='set random seed')
parser.add_argument('--cuda', action='store_true', default=True, help='use CUDA device')
parser.add_argument('--gpu_id', type=int, default=0, help='GPU device id used')
parser.add_argument('--save_dir', type=str, default='./checkpoints/', help='model save path')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
torch.manual_seed(args.seed)

# Use gpu or cpu to train
use_gpu = args.cuda
if use_gpu:
    torch.cuda.set_device(args.gpu_id)
    device = torch.device(args.gpu_id)
else:
    device = torch.device("cpu")

# load data
train_batch_size = args.train_batch_size
eval_batch_size = args.eval_batch_size
batch_size = {'train': train_batch_size, 'valid': eval_batch_size}
data_loader = data.Corpus("../data/wikitext2", batch_size, args.max_sql)

# WRITE CODE HERE within two '#' bar                                                           #
# Build model, optimizer and so on                                                             #
################################################################################################
model_RNN = model.RNN(len(data_loader.vocabulary), args.input_size, args.hidden_size, nlayers=args.num_layers, structure=args.structure)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_RNN.parameters(), lr=args.lr)
model_RNN.to(device)
################################################################################################


# WRITE CODE HERE within two '#' bar                                                           #
# Evaluation Function                                                                          #
# Calculate the average cross-entropy loss between the prediction and the ground truth word    #
# And then exp(average cross-entropy loss) is perplexity                                       #
################################################################################################
def evaluate():
    model_RNN.eval()
    data_loader.set_valid()

    loss_total = 0.0
    accT1_total = 0.0
    accT5_total = 0.0
    end_flag = False
    with torch.no_grad():
        while not end_flag:
            input, target, end_flag = data_loader.get_batch(device)
            output, _ = model_RNN(input)
            output = output.reshape(-1, len(data_loader.vocabulary))
            loss = criterion(output, target)

            loss_total += loss.item() * output.size(0)
            _, predT1 = torch.topk(output, 1, dim=1)
            _, predT5 = torch.topk(output, 5, dim=1)
            accT1_total += torch.sum(torch.eq(predT1, target.reshape(-1, 1)).any(dim=1)).float().item()
            accT5_total += torch.sum(torch.eq(predT5, target.reshape(-1, 1)).any(dim=1)).float().item()

    valid_loss = loss_total / (data_loader.valid.size(0) * data_loader.valid.size(1))
    valid_PP = np.exp(valid_loss)
    valid_accT1 = accT1_total / (data_loader.valid.size(0) * data_loader.valid.size(1))
    valid_accT5 = accT5_total / (data_loader.valid.size(0) * data_loader.valid.size(1))

    valid_writer.add_scalar('Loss/valid', valid_loss, epoch)
    valid_writer.add_scalar('Perplexity/valid', valid_PP, epoch)
    valid_writer.add_scalar('Acc_Top1/valid', valid_accT1, epoch)
    valid_writer.add_scalar('Acc_Top5/valid', valid_accT5, epoch)

    return valid_loss, valid_PP, valid_accT1, valid_accT5
################################################################################################


# WRITE CODE HERE within two '#' bar                                                           #
# Training Function                                                                            #
# Calculate the average cross-entropy loss between the prediction and the ground truth word    #
# And then exp(average cross-entropy loss) is perplexity                                       #
################################################################################################
def train():
    model_RNN.train(True)
    data_loader.set_train()

    loss_total = 0.0
    accT1_total = 0.0
    accT5_total = 0.0
    end_flag = False
    while not end_flag:
        input, target, end_flag = data_loader.get_batch(device)
        optimizer.zero_grad()
        output, _ = model_RNN(input)
        output = output.reshape(-1, len(data_loader.vocabulary))
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        loss_total += loss.item() * output.size(0)
        _, predT1 = torch.topk(output, 1, dim=1)
        _, predT5 = torch.topk(output, 5, dim=1)
        accT1_total += torch.sum(torch.eq(predT1, target.reshape(-1, 1)).any(dim=1)).float().item()
        accT5_total += torch.sum(torch.eq(predT5, target.reshape(-1, 1)).any(dim=1)).float().item()

    train_loss = loss_total / (data_loader.train.size(0) * data_loader.train.size(1))
    train_PP = np.exp(train_loss)
    train_accT1 = accT1_total / (data_loader.train.size(0) * data_loader.train.size(1))
    train_accT5 = accT5_total / (data_loader.train.size(0) * data_loader.train.size(1))

    train_writer.add_scalar('Loss/train', train_loss, epoch)
    train_writer.add_scalar('Perplexity/train', train_PP, epoch)
    train_writer.add_scalar('Acc_Top1/train', train_accT1, epoch)
    train_writer.add_scalar('Acc_Top5/train', train_accT5, epoch)

    return train_loss, train_PP, train_accT1, train_accT5
################################################################################################


# WRITE CODE HERE within two '#' bar                                                           #
# Showcase your model with multi-step ahead prediction                                         #
################################################################################################
def predict(prompt, pred_length, size_beam):
    model_RNN = torch.load('.\checkpoints\GRU\GRU_40.pt').to(device)
    model_RNN.eval()
    vocabulary = data_loader.vocabulary
    word_id = data_loader.word_id

    words = prompt.split()
    tokens = torch.LongTensor(len(words))
    token_id = 0
    for word in words:
        tokens[token_id] = word_id[word]
        token_id += 1

    with torch.no_grad():
        last_preds = [tokens.to(device)] * size_beam
        last_probabilitys = [1.0] * size_beam
        for epoch in range(pred_length):
            beam_temp = {}
            input = torch.stack(last_preds, dim=1).to(device)
            output, _ = model_RNN(input)
            output = output.reshape(-1, len(vocabulary))
            probability, pred = torch.topk(output, size_beam, dim=1)
            probability, pred = probability.reshape(-1, size_beam, size_beam)[-1, :, :], pred.reshape(-1, size_beam, size_beam)[-1, :, :]
            for beam_id in range(size_beam):
                for top_id in range(size_beam):
                    beam_temp[torch.cat((last_preds[beam_id], pred[beam_id, top_id: top_id + 1]))] = last_probabilitys[beam_id] * probability[beam_id, top_id].item()
                if epoch == 0:
                    break
            d = sorted(beam_temp.items(), key=lambda x: x[1], reverse=True)
            last_preds = [d[i][0] for i in range(size_beam)]
            last_probabilitys = [d[i][1] for i in range(size_beam)]
            # 防止溢出
            if max(last_probabilitys) > 100:
                for i, _ in enumerate(last_probabilitys):
                    last_probabilitys[i] = last_probabilitys[i] / 100

    return last_preds, last_probabilitys
################################################################################################


# WRITE CODE HERE within two '#' bar                                                           #
# Loop over epochs                                                                             #
################################################################################################
if __name__ == "__main__":
    if not exists(args.save_dir):
        os.makedirs(args.save_dir)
    print(args)
    for epoch in range(1, args.num_epochs + 1):
        print("*" * 64)
        print("== epoch: %d" % epoch)
        start = time.time()
        train_loss, train_PP, train_accT1, train_accT5 = train()
        valid_loss, valid_PP, valid_accT1, valid_accT5 = evaluate()
        print("Time Cost  : %f" % (time.time() - start))
        print("Loss       : %f, %f" % (train_loss, valid_loss))
        print("Perplexity : %f, %f" % (train_PP, valid_PP))
        print("Top1 Acc   : %f, %f" % (train_accT1, valid_accT1))
        print("Top5 Acc   : %f, %f" % (train_accT5, valid_accT5))
        print(">> saving...")
        torch.save(model_RNN, os.path.join(args.save_dir, "%s_%d.pt" % (args.structure, epoch)))
        print("<< done.")
################################################################################################
