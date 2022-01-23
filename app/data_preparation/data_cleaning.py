import pandas as pd


def remove_noise_cols(df: pd.DataFrame) -> pd.DataFrame:
    not_valid_cols = [col for col in df.columns if "Unnamed" in col.split(":")] + ["track_uri", "track_name", "album"]
    return df.drop(columns=not_valid_cols)


def remove_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()
