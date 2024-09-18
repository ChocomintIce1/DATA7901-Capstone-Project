import torch
import torch.nn as nn
import torch.nn.functional as F


device = torch.device("cuda" if torch.cuda.is_available() else "CPU")


class RNN(nn.Module):
    """
    https://www.kaggle.com/code/kanncaa1/recurrent-neural-network-with-pytorch#1
    https://pytorch.org/tutorials/beginner/former_torchies/nnft_tutorial.html
    The model for Recurrent Neural Network using PyTorch.
    """

    def __init__(self, input_size, feature_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.input_size = input_size
        self.feature_size = feature_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # self.rnn = nn.RNN(input_size=input_size, hidden_size=self.hidden_size, num_layers=1, nonlinearity='relu', batch_first=True)
        self.rnn = nn.RNN(input_size=input_size, hidden_size=self.hidden_size, num_layers=1, batch_first=True)

        self.layer1 = nn.Linear(self.hidden_size, self.hidden_size)
        self.layer2 = nn.Linear(self.hidden_size, self.hidden_size)
        self.layer3 = nn.Linear(self.hidden_size, output_size)
        self.to(device)
        
        # working
        # self.layer2 = nn.Linear(self.input_size, output_size)

    def forward(self, x):
        # Initialise hidden state with zeros
        hidden0 = torch.autograd.Variable(torch.zeros(1, len(x), self.hidden_size).to(device))

        # One time step
        output, hidden = self.rnn(x, hidden0)
        output = F.relu(self.layer1(output[:, -1, :]))
        output = F.relu(self.layer2(output))
        output = F.softmax(self.layer3(output))

        return output