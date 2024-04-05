import torch
import torch.nn as nn


class RNN(nn.Module):
    """
    https://www.kaggle.com/code/kanncaa1/recurrent-neural-network-with-pytorch#1
    https://pytorch.org/tutorials/beginner/former_torchies/nnft_tutorial.html
    The model for Recurrent Neural Network using PyTorch.
    """

    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, input, hidden):
        hidden = self.layer1(input)
        output = self.layer2(hidden)

        return hidden, output