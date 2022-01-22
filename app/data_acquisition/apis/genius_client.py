import os
import re
from pathlib import Path
from typing import Optional

import pandas as pd
from lyricsgenius import Genius


def song_name(song: str) -> str:
    """
    Get only the song name, dissemble with regex.

    :param song: song name with special letters
    :return: cleaned song name
    """
    match1 = re.match(r"(\([^()]*\))(.*)(-[^()]*)", song)  # to choose only song name "(..) \w+ -..."
    match2 = re.match(r"(\w+)(\(.*)", song)  # to remove "(..."
    match3 = re.match(r"(.*)(-.*)", song)  # to remove "-..."
    if match1:
        name = match1.group(2)
    elif match2:
        name = match2.group(1)
    elif match3:
        name = match3.group(1)
    else:
        name = song

    return name


def word_count(song_name: str, artist_name: str, genius: Genius) -> Optional[int]:
    """
    Function to return the lyrics count in a song

    :param artist_name: the song artist name
    :param song_name: the song name
    :param genius: genius api client
    :return: count of words
    """
    try:
        found = genius.search_song(title=song_name, artist=artist_name)
        lyrics = found.lyrics.splitlines()
        lyrics = list(filter(lambda x: x != "" and "[" not in x, lyrics))
        lyrics = " ".join(lyrics)
        lyrics = lyrics.split(" ")[:-1]

        return len(lyrics)
    except Exception:
        print("didn't succeed")
        return None


def genius_manager(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genius API manager, iterate through all songs and get words count.

    :param df: Dtaframe to iterate on
    :return: df with new column "words_count"
    """
    genius = Genius(access_token=os.getenv('GENIUS_ACCESS_TOKEN'),
                    excluded_terms=["(Remix)", "(Live)"])
    sub_df = df.loc[:, ["track_name", "artist_name"]]
    df["words_count"] = [word_count(song_name(instance[0]), instance[1], genius) for idx, instance in sub_df.iterrows()]
    df.to_csv(path_or_buf=Path.cwd().parent.parent / "data" / "02_tracks_from_spotify_with_word_count.csv",
              sep=",",
              columns=df.columns)
    return df
