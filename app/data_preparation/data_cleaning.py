import pandas as pd


def remove_noise_cols(df: pd.DataFrame) -> pd.DataFrame:
    valid_cols = ["track_uri", "artist", "artist_popularity", "artist_followers",
                  "artist_genres", "track_popularity", "track_danceability", "track_energy",
                  "track_loudness", "track_tempo", "track_duration_ms", "is_explict_content", "country_code"]
    cols_to_remove = list(filter(lambda x: x not in valid_cols, df.columns))

    return df.drop(columns=cols_to_remove)


def remove_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()