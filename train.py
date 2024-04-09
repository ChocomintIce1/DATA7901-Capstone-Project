import torch
from dataset import *
from modules import RNN
from torch.utils.data import DataLoader, random_split


# Load data
X = read_processed_dataset()
y = read_dataset()[1]

league_dataset = LeagueDataset(X,y)

n = y.shape[0]
train_size = int(0.7*n)
validation_size = int(0.2*n)
test_size = n - train_size - validation_size

train_set, validation_set, test_set = random_split(dataset=league_dataset,
                                                lengths=[train_size,validation_size,test_size])

train_set = DataLoader(train_set, batch_size=32)
validation_set = DataLoader(validation_set, batch_size=32)
test_set = DataLoader(test_set, batch_size=32)

# Create model
lr = 0.001
hidden_size = 128

rnn = RNN(input_size=X.shape[1], hidden_size=hidden_size, output_size=2)
optimiser = torch.optim.Adam(rnn.parameters(), lr=lr)

# Training
def train(category_tensor, line_tensor):
    rnn.zero_grad()

    for i in range(category_tensor.size()[0]):
        ...