import torch
import torch.nn as nn


class Memory(nn.Module):
    def __init__(self, ninput, nhid):
        super(Memory, self).__init__()
        self.ninput = ninput
        self.nhid = nhid
        self.fc = nn.Linear(ninput + nhid, 4 * nhid)

    def forward(self, x):
        '''
        x: (seq_len, batch_size, ninput)
        '''
        c = torch.zeros([x.size(1), self.nhid]).to(x.device)
        h = torch.zeros([x.size(1), self.nhid]).to(x.device)
        output = torch.zeros([x.size(0), x.size(1), self.nhid]).to(x.device)
        for seq_id in range(x.size(0)):
            a = self.fc(torch.cat((x[seq_id], h), dim=1)) # a: (batch_size, 4 * nhid)
            i = torch.sigmoid(a[:, : 1 * self.nhid]) # input_gate
            f = torch.sigmoid(a[:, 1 * self.nhid: 2 * self.nhid]) # forget_gate
            o = torch.sigmoid(a[:, 2 * self.nhid: 3 * self.nhid]) # output_gate
            g = torch.tanh(a[:, 3 * self.nhid:]) # gate_gate

            c = c * f + i * g # update c
            h = o * torch.tanh(c) # update h
            output[seq_id] = h
        return output, h


class MyLSTM(nn.Module):
    def __init__(self, ninput, nhid, nlayers):
        super(MyLSTM, self).__init__()
        self.ninput = ninput
        self.nhid = nhid
        self.nlayers = nlayers
        self.mems = nn.ModuleList([Memory(ninput, nhid)])
        for _ in range(1, nlayers):
            self.mems.append(Memory(nhid, nhid))

    def forward(self, input):
        output, hidden = self.mems[0](input)
        for i in range(1, self.nlayers):
            output, hidden = self.mems[i](output)
        return output, hidden


class RNN(nn.Module):
    # RNN model is composed of three parts: a word embedding layer, a rnn network and a output layer
    # The word embedding layer have input as a sequence of word index (in the vocabulary) and output a sequence of vector where each one is a word embedding
    # The network has input of each word embedding and output a hidden feature corresponding to each word embedding
    # The output layer has input as the hidden feature and output the probability of each word in the vocabulary
    # feel free to change the init arguments if necessary
    def __init__(self, nvoc, ninput, nhid, nlayers, structure):

        super(RNN, self).__init__()
        self.drop = nn.Dropout(0.5)

        # self.embed change input size BxL into BxLxE
        self.embed = nn.Embedding(nvoc, ninput)

        # WRITE CODE HERE within two '#' bar                                              #
        # Construct you RNN model here. You can add additional parameters to the function #
        ###################################################################################
        assert structure in ('GRU', 'LSTM')
        if structure == 'GRU':
            self.rnn = nn.GRU(ninput, nhid, nlayers)
        if structure == 'LSTM':
            self.rnn = MyLSTM(ninput, nhid, nlayers)
        ###################################################################################

        self.decoder = nn.Linear(nhid, nvoc)
        self.init_weights()
        self.nhid = nhid
        self.nlayers = nlayers

    def init_weights(self):
        init_uniform = 0.1
        self.embed.weight.data.uniform_(-init_uniform, init_uniform)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-init_uniform, init_uniform)

    # feel free to change the forward arguments if necessary
    def forward(self, input):
        embeddings = self.drop(self.embed(input))

        # WRITE CODE HERE within two '#' bar                                             #
        # With embeddings, you can get your output here.                                 #
        # Output has the dimension of sequence_length * batch_size * number of classes   #
        ##################################################################################
        output, hidden = self.rnn(embeddings)
        ##################################################################################

        output = self.drop(output)
        decoded = self.decoder(output.reshape(output.size(0)*output.size(1), output.size(2)))
        return decoded.reshape(output.size(0), output.size(1), decoded.size(1)), hidden
