import pandas as pd
from sklearn.preprocessing import LabelEncoder


def parse_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Function that parses string saves Series column to Tuple.
    This is for the `artist_genres` column.

    :param df: the dataframe to change.
    :param col: the column to parse.
    :return updated Dataframe
    """
    df_copy = df.copy()
    df_copy[col] = pd.Series([eval(instance[col]) for idx, instance in df_copy.iterrows()])

    return df_copy


def encode_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Function that preform label encoding on specific column.

    :param df: Dataframe to iterate on
    :param column: the column to label
    :return: Dataframe with labeled column
    """
    return LabelEncoder().fit_transform(df[column])


def chain(start, *funcs) -> pd.DataFrame:
    """
    Chain of function in data preparation.
    Credit: https://blog.finxter.com/how-to-chain-multiple-function-calls-in-python/

    :param start: initilize value of chain
    :param: *funcs: function to chain.
    :return: new Dataframe after chaining
    """
    res = start
    for func in funcs:
        res = func(res)
    return res