import pandas as pd
from sklearn.model_selection import train_test_split


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

def test_train(train_split=0.7, validation_split=0.2) -> pd.DataFrame:
    """
    Creates training, validation and testing datasets.
    Initially configured to a 70-20-10 split

    Returns:
        tuple: Returns a tuple of (X_train, X_validation, ..., y_test) 
    """
    X, y = get_dataset()
    validation_split = validation_split/train_split
    print('n:', X.shape[0])

    X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=1-train_split)
    X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=validation_split)

    print(X_train.shape[0], X_validation.shape[0], X_test.shape[0])

    return X_train, X_validation, X_test, y_train, y_validation, y_test