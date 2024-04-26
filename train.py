import torch
import numpy as np
import pandas as pd
from dataset import *
from modules import RNN
from torch.utils.data import DataLoader, random_split

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load data
X = read_processed_dataset(r'C:\Users\Jae\iCloudDrive\DATA7901\Project\DATA7901-Capstone-Project\processed_X1.csv')
y = read_dataset()[1]
# y = pd.DataFrame([0,1,1,0,0,1,0,1,0,1], dtype=np.float32)

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
batch_size = 32
train_set = DataLoader(train_set, batch_size=batch_size)
validation_set = DataLoader(validation_set, batch_size=batch_size)
test_set = DataLoader(test_set, batch_size=batch_size)

# Create model
lr = 0.001
hidden_size = 128

max_time = get_max_time(X)
rnn = RNN(input_size=max_time, feature_size=X.shape[1], hidden_size=hidden_size, output_size=2)
rnn = rnn.to(device)
optimiser = torch.optim.Adam(rnn.parameters(), lr=lr)
loss_function = torch.nn.CrossEntropyLoss()

# Training model
epochs = 3

for epoch in range(epochs):
    print(f"--------- Epoch #{epoch} ---------")
    for batch, (train, outcome) in enumerate(train_set):
        train = torch.autograd.Variable(train).to(device)
        outcome = torch.autograd.Variable(outcome).to(device, dtype=torch.long)

        predict = rnn(train)
        # print('printing shape', predict.size(0), outcome.size(0))
        # print('predict', predict)

        outcome1 = []
        for o in outcome:
            outcome1.append(o)
        outcome = torch.LongTensor(outcome1)

        loss = loss_function(predict, outcome)

        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        if batch % 30 == 0:
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