import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ast
import math
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


def read_dataset() -> pd.DataFrame:
    """
    Reads the multiple csv files and combines into one.
    Obtained from: https://www.kaggle.com/datasets/chuckephron/leagueoflegends/data

    Returns:
        tuple: Returns a predictor dataframe and label dataframe
    """
    # Read csv
    df = pd.read_csv('archive/LeagueofLegends.csv')

    # Clean up dataset

    # According to this article, https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt403ee07f98e2e0fc
    # The predictor variables were:
    # Game time (the in-game time)
    # Gold % (player gold / total gold in game)
    # Tower kills
    # Dragon kills (whether a team has dragon soul or not)
    # Inhibitor timers (how long until an inhibitor respawns) for each inhibitor
    
    # Only predictor variables relating to the list above were selected.
    X = df[['golddiff', 'bKills', 'bTowers', 'bInhibs', 'bDragons', 'bBarons', 'bHeralds',
                'rKills', 'rTowers', 'rInhibs', 'rDragons', 'rBarons', 'rHeralds',
                'goldblueTop', 'goldblueJungle', 'goldblueMiddle', 'goldblueADC', 'goldblueSupport',
                'goldredTop', 'goldredJungle', 'goldredMiddle', 'goldredADC', 'goldredSupport']]

    # For selecting the labels, let 1 = blue side win and 0 = red side win
    y = df[['bResult']]

    return X, y

def get_max_time(X):
    """Helper function for finding the longest game.
    O(N) approach

    Args:
        X (dataframe): X

    Returns:
        int: returns longest game in minutes
    """
    MAX_TIME = 0
    for index, row in X.iterrows():
        row = ast.literal_eval(row[0])
        time = len(row)
        
        if time > MAX_TIME:
            MAX_TIME = time
        
    return MAX_TIME

def process_time(game_length, events):
    """
    Helper function

    Args:
        game_length (int): Length of the game in minutes
        events (list): a timeline of where a team gets an objective.

    Returns:
        list: A readable form of events that occured in that game
    """
    timeline = np.zeros(game_length)

    for event in events:
        event_time = math.floor(event[0])
        timeline[event_time] += 1

    return timeline

def process_dataset(X, save_csv=False) -> pd.DataFrame:
    """
    Process the data so that it is readable by Pandas and PyTorch.
    Also populates uneventful periods.

    Returns:
        pd.DataFrame: Readable version of dataframe
    """
    # Create new dataframe to append new columns to.
    new_X = pd.DataFrame(columns=X.columns)

    for index0, row in X.iterrows():
        new_row = []

        for index1, col in enumerate(row):
            game_length = len(col) if index1 == 0 else game_length # get game length
            col = ast.literal_eval(col) # convert str to list

            # If column is gold related, no modification needed
            if 'gold' in X.columns[index1]:
                new_row.append(col)

            else:   
                new_row.append(process_time(game_length, col))
        
        # Append new row to the new dataframe
        new_X.loc[index0] = new_row

    if save_csv:
        new_X.to_csv('processed_X.csv')

    return new_X

def test_train(train_split=0.7, validation_split=0.2, normalise=True) -> pd.DataFrame:
    """
    Creates training, validation and testing datasets.
    Initially configured to a 70-20-10 split

    Returns:
        tuple: Returns a tuple of (X_train, X_validation, ..., y_test) 
    """
    X, y = read_dataset()

    if normalise:
        ...

    validation_split = validation_split/train_split

    # Get train and validation dataset
    X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=1-train_split)

    # Get validation and test dataset
    X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=validation_split)

    return X_train, X_validation, X_test, y_train, y_validation, y_test

def to_tensor(X,y):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # X = DataLoader(dataset=X, batch_size=60)
    # y = DataLoader(dataset=y, batch_size=60)
    print(torch.Tensor(X.values))
    print(X.shape, y.shape)

    df = TensorDataset(X, y)

# X = pd.read_csv(r'C:\Users\Jae\Desktop\processed_X.csv')
# y = read_dataset()[1]
# to_tensor(X, y)