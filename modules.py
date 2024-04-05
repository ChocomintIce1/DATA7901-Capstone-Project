import torch
import torch.nn as nn


class RNN(nn.Module):
    """
    https://www.kaggle.com/code/kanncaa1/recurrent-neural-network-with-pytorch#1
    The model for Recurrent Neural Network using PyTorch.
    """

    def __init__(self, hidden_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
    
    def forward(self, input, hidden):
        ...