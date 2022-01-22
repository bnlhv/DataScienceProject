"""
This module finds lyrics of sing from AZlyrics site for columns word_amount and is_explicit_content.
This module is a backup for the songs that the apis could't find.
"""
import random
from pathlib import Path
from time import sleep
from typing import Tuple

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from app.data_acquisition.crawlers.utils import AZLYRICS_URL, beautiful_soup_scraping, Status404CounterException


def get_track_azlyrics_url(artist_name: str, track_name: str) -> str:
    """
    This function manipulate strings and produce valid URL for scraping lyrics
    from azlyrics website.

    :param artist_name: The artist's name.
    :param track_name: The song's name.
    :return: valid URL
    """
    # Remove spaces, ', (, ...
    artist = "".join([c for c in artist_name.lower().replace(" ", "").split("(")[0] if c.isalpha()])
    track = "".join([c for c in track_name.lower().replace(" ", "").split("(")[0] if c.isalpha()])

    return f"{AZLYRICS_URL}/{artist}/{track}.html"


def get_track_html(artist_name: str, track_name: str) -> str:
    """
    Scrape the html page of the track and find the lyrics.

    :param artist_name: The artist's name.
    :param track_name: The song's name.
    :return: the lyrics
    """
    url = get_track_azlyrics_url(artist_name, track_name)
    html = beautiful_soup_scraping(BeautifulSoup.find, url, "div",
                                   {"class": "col-xs-12 col-lg-8 text-center"}).text
    # Hard-coding in this site to fetch the lyrics because the dix doesn't have specefic class
    lyrics = html.strip()
    lyrics = lyrics[lyrics.find("\n\n\n\n") + 5: lyrics.find("Submit Corrections")].splitlines()
    # Remove the song names and all the empty strings and pop the last ""
    lyrics = list(filter(None, lyrics[2:]))
    lyrics = lyrics.pop()
    lyrics = "".join(lyrics)
    print(lyrics)
    return lyrics


def is_explict_words_in_track(artist_name: str, track_name: str) -> Tuple[int, int]:
    """
    Check if there are any explict words in the song.

    ----- Credits to data.world for bad_words.csv, dataset name "list of bad words" -------

    :param artist_name: The artist's name.
    :param track_name: The song's name.
    :return: 1 if there are such lyrics else 0
    """
    bad_words_df = pd.read_csv(Path.cwd().parent / "data" / "bad_words.csv")
    bad_words = bad_words_df.iloc[:, 0].to_list()
    lyrics = get_track_html(artist_name, track_name)

    if any(word in bad_words for word in lyrics):
        return 1, len(lyrics)
    return 0, len(lyrics)


def lyrics_crawler_manager(df: pd.DataFrame) -> pd.DataFrame:
    """ Function that fill blank is_explict in dataset. """
    print("in lyricis crawler")
    df_copy = df.copy()
    sub_df = df.loc[np.logical_and(df["is_explicit_content"] != 0,
                                   df["is_explicit_content"] != 1), :]
    for idx, instance in sub_df.iterrows():
        artist = instance["artist_name"]
        track = instance["track_name"]
        try:
            sleep(random.randint(2, 10))  # Sleep for randomized time for scraping not getting blocked
            df_copy.loc[idx, "is_explicit_content"], df_copy.loc[idx, "words_count"] = \
                is_explict_words_in_track(artist_name=artist, track_name=track)
        except Status404CounterException:
            df_copy.loc[idx, "words_count"] = np.NaN
            df_copy.loc[idx, "is_explicit_content"] = np.NaN
        except Exception:
            pass  # pass this song...

    df_copy.to_csv(Path.cwd() / "03_explict_feature_update_from_crawler.csv")

    return df_copy
