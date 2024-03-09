import pandas as pd


def get_dataset() -> tuple:
    """
    Reads the csv file and returns the dataframe.

    Returns:
        tuple: Returns a predictor dataframe and label dataframe
    """
    df = pd.read_csv('archive/games.csv')
    X = df.drop(['winner'], axis=1)
    y = df['winner']

    return X, y