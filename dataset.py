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
    df = pd.read_csv(r'D:\DATA7901-Capstone-Project\archive\LeagueofLegends.csv') # Windows
    # df = pd.read_csv('/media/jae/Games/DATA7901-Capstone-Project/archive/LeagueofLegends.csv') # Linux

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

def process_time(game_length, events, max_time):
    """
    Helper function

    Args:
        game_length (int): Length of the game in minutes
        events (list): a timeline of where a team gets an objective.

    Returns:
        list: A readable form of events that occured in that game
    """
    timeline = [0] * game_length

    for event in events:
        event_time = math.floor(event[0])
        timeline[event_time] += 1
    
    # Fill the rest of timeline with the last event
    for time in range(game_length, max_time):
        timeline.append(timeline[game_length - 1])

    return timeline

def process_dataset(X=None, save_csv=False) -> pd.DataFrame:
    """
    Process the data so that it is readable by Pandas and PyTorch.
    Also populates uneventful periods.

    Returns:
        pd.DataFrame: Readable version of dataframe
    """
    if X is None:
        X,_ = read_dataset()
    
    # Max time length in dataset
    max_time = get_max_time(X)

    # Create new dataframe to append new columns to.
    new_X = pd.DataFrame(columns=X.columns)

    # Iterate through every row
    for index0, row in X.iterrows():
        new_row = []
        game_length = 0

        # Iterate through every feature
        for index1, col in enumerate(row):
            col = ast.literal_eval(col) # convert str to list

            # get game length
            if index1 == 0:
                game_length = len(col)
            
            
            # If column is gold related, no modification needed
            if 'gold' in X.columns[index1]:
                # Fill the rest of timeline with the last event
                for time in range(game_length, max_time):
                    col.append(col[game_length - 1])
                
                new_row.append(col)


            else:
                new_row.append(process_time(game_length, col, max_time))
        
        # Append new row to the new dataframe
        new_X.loc[index0] = new_row

    if save_csv:
        print('saved csv')
        new_X.to_csv('processed_X1.csv', index_label=False)

    return new_X

def read_processed_dataset(df='C:/Users/Jae/Desktop/processed_X - Copy.csv') -> pd.DataFrame:
    '''
    To speed up execution, simply convert the dataset to a readable dataset.

    Args:
        df (str): The directory of the dataset. Defaults to r'C:/Users/Jae/Desktop/processed_X.csv'.

    Returns:
        dataframe: Returns the transformed dataset
    '''
    df = pd.read_csv(df)

    # for col, _ in enumerate(df.columns):
    #     for row, _ in df.iterrows():
    #         df.iloc[row,col] = ast.literal_eval(df.iloc[row,col])

    # for col in df.columns:
    #     df[col] = df[col].apply(ast.literal_eval)
    #     print(col, df[col])

    return df

def test_train(X, y, train_split=0.7, validation_split=0.2, normalise=True) -> pd.DataFrame:
    """
    Creates training, validation and testing datasets.
    Initially configured to a 70-20-10 split

    Returns:
        tuple: Returns a tuple of (X_train, X_validation, ..., y_test) 
    """
    if normalise:
        ...

    validation_split = validation_split/train_split

    # Get train and validation dataset
    X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=1-train_split)

    # Get validation and test dataset
    X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=validation_split)

    return X_train, X_validation, X_test, y_train, y_validation, y_test

class LeagueDataset(torch.utils.data.Dataset):
    """
    Creates a dataset that handles the temporal data and allows Torch to read
    the data by converting the dataset to a Tensor.
    """
    def __init__(self, data, label):
        """
        Initilaiser for class.

        Args:
            data (List): Returns the game data based on index
            label (List): The match outcome
        """
        self.data = data
        self.label = label

    def __len__(self):
        return self.label.shape[0]

    def __getitem__(self, index):
        return (torch.Tensor([ast.literal_eval(data) for data in self.data.iloc[index, :]]),
                torch.Tensor(self.label.iloc[index]))

# Debugging stuff
# X, y = read_dataset()
# X = pd.read_csv(r'C:\Users\Jae\Desktop\processed_X.csv')
# print(X)

# X = X.iloc[1,:]
# lst = [ast.literal_eval(x) for x in X]
# print(torch.tensor(lst))
# print(read_processed_dataset())