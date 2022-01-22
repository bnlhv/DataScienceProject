from pathlib import Path

import pandas as pd
import numpy as np

if __name__ == '__main__':
    df_data = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing.csv")
    df_origins = pd.read_csv(Path.cwd().parent / "data" / "artists_and_origins_ranker.csv")
    df_origins2 = pd.read_csv(Path.cwd().parent / "data" / "artists_and_origins_britannica.csv")
    df_origins3 = pd.read_csv(Path.cwd().parent / "data" / "artists_and_origins_famousbirthdays.csv")
    df_origins3 = df_origins3.rename(columns={'artist': 'artist_name'})
    findings = []
    for artist in df_data["artist_name"].unique().tolist():
        artist_origin = np.NaN
        for df in [df_origins3, df_origins2, df_origins]:
            try:
                row = df.index[df["artist_name"] == artist].tolist()[0]
                artist_origin = df.loc[row, "origin"]
                break
            except Exception:
                artist_origin = np.NaN

        df_data.loc[df_data["artist_name"] == artist, "artist_origin"] = artist_origin

    df_data.to_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing_with_origins_from_all_crawlers.csv")
    print(df_data["artist_origin"].isnull().sum())
