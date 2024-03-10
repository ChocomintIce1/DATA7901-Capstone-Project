import torch
import torch.nn as nn


class RNN(nn.Module):
    """
    The model for Recurrent Neural Network using PyTorch.
    """

    def __init__(self):
        super(RNN, self).__init__()