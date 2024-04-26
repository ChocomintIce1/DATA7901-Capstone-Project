import torch
import numpy as np
import pandas as pd
from dataset import *
from modules import RNN
from torch.utils.data import DataLoader, random_split

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load data
X = read_processed_dataset()
# X = process_dataset(save_csv=True)

max_time = get_max_time(X)

_,y = read_dataset()

# for col in X.columns:
#     X[col] = X[col].astype(np.float32)

# y = read_dataset()[1]
y = pd.DataFrame([0,1,1,0,0,1,0,1,0,1], dtype=np.float32)

league_dataset = LeagueDataset(X,y)

# Get size of splitting datasets
n = y.shape[0]
train_size = int(0.7*n)
validation_size = int(0.2*n)
test_size = n - train_size - validation_size

# print(y)
# print(X.shape, train_size, validation_size, test_size)

# Split dataset
train_set, validation_set, test_set = random_split(dataset=league_dataset,
                                                lengths=[train_size,validation_size,test_size])

# Data loader
train_set = DataLoader(train_set, batch_size=1)
validation_set = DataLoader(validation_set, batch_size=1)
test_set = DataLoader(test_set, batch_size=1)

# Create model
lr = 0.001
hidden_size = 128

rnn = RNN(input_size=max_time, hidden_size=hidden_size, output_size=2)
rnn = rnn.to(device)
optimiser = torch.optim.Adam(rnn.parameters(), lr=lr)
loss_function = torch.nn.CrossEntropyLoss()

# Training model
epochs = 3

for epoch in range(epochs):
    for batch, (train, outcome) in enumerate(train_set):
        train = torch.autograd.Variable(train).to(device)
        outcome = torch.autograd.Variable(outcome).to(device)

        print(train, train.shape)

        predict = rnn(train)
        loss = loss_function(predict, y)

        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        loss, current = loss.item(), batch*len(X)
        print(f'loss: {loss} [{current}/{10}]')



# Training
# def train(dataloader, model, loss_fn, optimiser):
#     size = len(dataloader.dataset)

#     for batch, (X,y) in enumerate(dataloader):
#         X,y = torch.autograd.Variable(X), torch.autograd.Variable(y)
        
#         predict = model(X)
#         loss = loss_fn(predict, y)

#         optimiser.zero_grad()
#         loss.backward()
#         optimiser.step()

#         loss, current = loss.item(), batch*len(X)
#         print(f'loss: {loss} [{current}/{size}]')

# for epoch in range(1,31):
#     train(train_set, rnn, loss_function, optimiser)