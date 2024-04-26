import torch
import torch.nn as nn


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

        self.rnn = nn.RNN(input_size=input_size, hidden_size=self.hidden_size, num_layers=1, nonlinearity='relu', batch_first=True)

        # self.layer1 = nn.Linear(input_size, output_size)
        self.layer2 = nn.Linear(self.hidden_size, 2)
    
    def forward(self, x):
        # Initialise hidden state with zeros
        hidden0 = torch.autograd.Variable(torch.zeros(1, len(x), self.hidden_size))

        # One time step
        output, hidden = self.rnn(x, hidden0)
        # print(output.size())
        output = self.layer2(output[:, -1, :])
        # output = self.layer2(output[:, -1, :])

        return output