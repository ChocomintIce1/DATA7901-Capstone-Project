import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


def get_dataset() -> pd.DataFrame:
    """
    Reads the csv file and returns the dataframe.

    Returns:
        tuple: Returns a predictor dataframe and label dataframe
    """
    df = pd.read_csv('archive/games.csv')
    X = df.drop(['winner'], axis=1)
    y = df['winner']

    return X, y

def test_train(train_split=0.7, validation_split=0.2, normalise=True) -> pd.DataFrame:
    """
    Creates training, validation and testing datasets.
    Initially configured to a 70-20-10 split

    Returns:
        tuple: Returns a tuple of (X_train, X_validation, ..., y_test) 
    """
    X, y = get_dataset()

    if normalise:
        X = normalize(X.iloc[:,2:])

    validation_split = validation_split/train_split

    X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=1-train_split)
    X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=validation_split)

    return X_train, X_validation, X_test, y_train, y_validation, y_test