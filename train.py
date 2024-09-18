import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataset import *
from modules import RNN
from torch.utils.data import DataLoader, random_split

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load data
X = read_processed_dataset(r'C:\Users\Jae\iCloudDrive\UQ\DATA7901\Project\DATA7901-Capstone-Project\processed_X1.csv')
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
lr = 0.00001
hidden_size = 128

max_time = get_max_time(X)
# print('here', X.shape[1])
rnn = RNN(input_size=max_time, feature_size=X.shape[1], hidden_size=hidden_size, output_size=2)
rnn = rnn.to(device)
optimiser = torch.optim.Adam(rnn.parameters(), lr=lr)
loss_function = torch.nn.CrossEntropyLoss()

# Training model
def train(epochs=10, plot=True):
    training_loss_list = []
    validation_loss_list = []

    for epoch in range(epochs):
        training_epoch_loss_list = []
        print(f"--------- Epoch #{epoch} ---------")
        for batch, (train, outcome) in enumerate(train_set):
            train = torch.autograd.Variable(train).to(device, dtype=torch.float32)
            outcome = torch.autograd.Variable(outcome).to(device, dtype=torch.int16)

            predict = rnn(train)

            # Reformat outcome tensor
            outcome1 = []
            for o in outcome:
                outcome1.append(o)
            outcome = torch.LongTensor(outcome1)

            loss = loss_function(predict, outcome)
            optimiser.zero_grad()
            loss.backward()

            # Save training loss
            training_epoch_loss_list.append(loss_function(predict, outcome).item())

            optimiser.step()

            if batch % 30 == 0:
                loss, current = loss.item(), batch*len(X)
                print(f'loss: {loss} [{current}/{len(train_set.dataset)}]')

        # Average testing loss
        training_loss_list.append(np.mean(training_epoch_loss_list))

        # Testing
        rnn.eval()
        size = len(validation_set.dataset)

        correct = 0
        validation_loss = 0
        with torch.no_grad():
            validation_epoch_loss_list = []
            for batch, (validation, outcome) in enumerate(validation_set):
                validation = torch.autograd.Variable(validation).to(device)
                outcome = torch.autograd.Variable(outcome).to(device, dtype=torch.long)

                # Reformat outcome tensor
                outcome1 = []
                for o in outcome:
                    outcome1.append(o)
                outcome = torch.LongTensor(outcome1)

                predict = rnn(validation)
                validation_loss += loss_function(predict, outcome).item()

                # Save validation loss
                validation_epoch_loss_list.append(loss_function(predict, outcome).item())

                # Count correct predictions
                correct += (predict.argmax(1) == outcome).sum().item()

            # Average validation loss
            validation_loss_list.append(np.mean(validation_epoch_loss_list))

            print(f"Acc:{correct/size:>7f}, Avg Loss: {validation_loss/size:>7f}")

    # Plot training/validation loss graph
    if plot:
        print("training loss\n", training_loss_list) 
        print("validation loss\n", validation_loss_list)
        plt.plot(range(len(training_loss_list)), training_loss_list, 'b')
        plt.plot(range(len(validation_loss_list)), validation_loss_list, 'r')
        plt.show()


# Save the model
if __name__ == '__main__':
    train(10, True)
    save_model = True

    if save_model:
        print('Model saved')
        torch.save(rnn, 'League_of_Legends_predicition.pt')