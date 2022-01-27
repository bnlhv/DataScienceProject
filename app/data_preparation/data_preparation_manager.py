from pathlib import Path

import numpy as np
import pandas as pd

from data_cleaning import remove_nan_values, remove_noise_cols
from genres_reduction_feature_engineering import popular_genre_dummies
from origins_to_country_code_feature_engineering import origin_to_country_codes
from utils import encode_column


def drop_correlated_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that drop high correlated features of the `artist_genres` dummy features.
    Credit: https://www.projectpro.io/recipes/drop-out-highly-correlated-features-in-python

    :param df: the Dataframe to preform action on
    :return: new Dataframe
    """
    corr_matrix = df.corr().abs()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]

    return df.drop(df.columns[to_drop], axis=1)


def save_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function saves the data frame in the middle of the pipeline and returns is.

    :param df: Dataframe to save
    :return: same df
    """
    df.copy().to_csv(Path.cwd().parent / "data" / f"06_with_country_code.csv")
    return df


def manage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manager function that runs this preparation module with a pipeline of functions.

    :param df: Dataframe from raw data
    :return: Dataframe prepared for visualizations and ML model
    """
    df_copy = encode_column(df.copy(), "artist_name")
    for func in [remove_nan_values, remove_noise_cols, origin_to_country_codes, save_df,
                 popular_genre_dummies, save_df, drop_correlated_features]:
        df_copy = func(df_copy)
        print(f"finished {func.__name__}")

    return df_copy


if __name__ == '__main__':
    df = pd.read_csv(Path.cwd().parent / "data" / "04_origin_feature_update_from_crawler.csv")
    manage(df).to_csv(Path.cwd().parent / "data" / "07_final_dataset.csv")
