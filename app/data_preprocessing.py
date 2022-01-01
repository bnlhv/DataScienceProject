from pathlib import Path

import pandas as pd



def remove_noise_cols(df: pd.DataFrame) -> pd.DataFrame:
    valid_cols = ["track_uri", "track_name", "artist_name", "artist_popularity", "artist_followers",
                  "artist_genres","album", "track_popularity", "track_danceability", "track_energy",
                  "track_loudness", "track_tempo", "track_duration_ms", "is_explict_content"]
    cols_to_remove = list(filter(lambda x: x not in valid_cols, df.columns))

    return df.drop(columns=cols_to_remove)

def remove_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


if __name__ == '__main__':
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")
    df = remove_nan_values(df.copy())
    df = remove_noise_cols(df)
    df.to_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing.csv")
