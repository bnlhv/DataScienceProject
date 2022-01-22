from pathlib import Path

import pandas as pd

from data_cleaning import remove_nan_values, remove_noise_cols
from genres_reduction_feature_engineering import popular_genre_dummies
from origins_to_country_code_feature_engineering import origin_to_country_codes
from utils import encode_column, chain


def drop_correlated_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that drop high correlated features of the `artist_genres` dummy features.

    :param df: the Dataframe to preform action on
    :return: new Dataframe
    """
    corr = df.corr()
    mask = (df.corr() > 0.9) & (df.corr() < 1.0)
    high_corr = corr[mask]
    col_to_filter_out = ~high_corr[mask].any()
    X_clean = df[high_corr.columns[col_to_filter_out]]

    return X_clean


def manage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manager function that runs this preparation module.

    :param df: Dataframe from raw data
    :return: Dataframe prepared for visualizations and ML model
    """
    pipeline = [remove_nan_values, remove_noise_cols, origin_to_country_codes, popular_genre_dummies]
    df_copy = encode_column(df.copy(), "artist")

    return chain(df_copy, pipeline)

if __name__ == '__main__':
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_convert_artist_name_to_nominal.csv")
    df = popular_genre_dummies(df, "artist_genres")
    print("")
    # df = convert_origin_to_country_codes(df)
    # df.reset_index(drop=True, inplace=True)
    df.to_csv(Path.cwd().parent / "data" / "final_dataset.csv")
