import torch
from dataset import *
from modules import RNN
from torch.utils.data import Dataset, DataLoader, random_split


# Load data
X = read_processed_dataset()
y = read_dataset()[1]

league_dataset = LeagueDataset(X,y)
print('league_dataset len:', len(league_dataset))
n = y.shape[0]
train_size = int(0.7*n)
validation_size = int(0.2*n)
test_size = n - train_size - validation_size

train_set, validation_set, test_set = random_split(dataset=league_dataset,
                                                lengths=[train_size,validation_size,test_size])