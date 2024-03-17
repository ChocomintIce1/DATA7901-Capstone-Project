import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

def process_dataset() -> pd.DataFrame:
    """
    Process the data so that it is readable by Pandas and PyTorch.

    Returns:
        pd.DataFrame: Readable version of dataframe
    """
    # Read dataset
    X, y = read_dataset()

    # Create new dataframe to append new columns to.
    new_X = pd.DataFrame()

    return new_X, y

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

print(test_train())

def plot_correlation_matrix() -> None:
    """
    Reference: https://seaborn.pydata.org/examples/many_pairwise_correlations.html
    Plots the correlation matrix between the predictor variables

    Returns:
        None
    """
    X, _ = get_dataset()

    # Set theme
    sns.set_theme(style="white")

    # Compute correlation matrix
    corr = X.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    # Plot graph
    plt.show()