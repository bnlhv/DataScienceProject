"""
This module brings the data if a song has explicit content or not
"""
from pathlib import Path
from typing import List

import deezer
import numpy as np
import pandas as pd


def get_explict_feature_from_deezer(tracks: List[str], artists: List[str]) -> List[int]:
    """
    Function that gets list of tracks and their artist and get deezers same track
    for explict_lyrics feature.

    :param tracks: List of csv tracks from spotify
    :param artists: List of csv artists of the tracks from spotify, for double check
                    that the song is the same.
    :return: List of 1,0 booleans for the Dataframe.
    """
    dz_client = deezer.Client()
    is_explict = []
    for idx, (track, artist) in enumerate(zip(tracks, artists)):
        try:
            deezer_options = dz_client.search(track=track)
            for deezer_option in deezer_options:
                if deezer_option.artist.name.lower() == artist.lower():
                    is_explict.append(1 if deezer_option.as_dict()["explicit_lyrics"] is True else 0)
                    break
            if idx + 1 != len(is_explict):
                is_explict.append(np.NaN)
        except Exception:
            is_explict.append(np.NaN)

    return is_explict


def deezer_manager(df: pd.DataFrame) -> pd.DataFrame:
    """ Main function os deezer's module. """
    df_copy = df.copy()
    df_copy["is_explict_content"] = get_explict_feature_from_deezer(df_copy["track_name"], df_copy["artist_name"])
    df_copy.to_csv(Path.cwd().parent / "data" / "02_deezer_update_explict_content_feature.csv")

    return df
