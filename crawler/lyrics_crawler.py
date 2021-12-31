import random
from pathlib import Path
from time import sleep
from typing import Callable

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from crawler.chrome_driver import driver

base_url = "https://www.azlyrics.com/lyrics"
status_404_counter = 0


class Status404CounterException(BaseException):
    pass


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

    return f"{base_url}/{artist}/{track}.html"


def beautiful_soup_scraping(url: str) -> str:
    """
    Scrape with Beautiful Soup.

    :param url: the Url to fetch the data from
    :return: text of div element
    """
    global status_404_counter

    response = requests.get(url)
    if response.status_code == 404:
        if status_404_counter == 3:
            raise Status404CounterException()
        else:
            status_404_counter += 1
    else:
        if status_404_counter == 0:
            pass
        else:
            status_404_counter -= 1

    soup = BeautifulSoup(response.text, "lxml")
    return soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).text


def selenium_scraping(url: str) -> str:
    """
    Scrape with selenium.

    :param url: the Url to fetch the data from
    :return: text of div element
    """
    driver.get(url)
    return driver.find_element_by_xpath("//div[@class='col-xs-12 col-lg-8 text-center']")


def get_track_html(artist_name: str, track_name: str, scraping_method: Callable) -> str:
    """
    Scrape the html page of the track and find the lyrics.

    :param scraping_method: Call different scraping method each time
    :param artist_name: The artist's name.
    :param track_name: The song's name.
    :return: the lyrics
    """
    url = get_track_azlyrics_url(artist_name, track_name)
    html = scraping_method(url)
    # Hard-coding in this site to fetch the lyrics because the dix doesn't have specefic class
    lyrics = html.strip()
    lyrics = lyrics[lyrics.find("\n\n\n\n") + 5: lyrics.find("Submit Corrections")].splitlines()
    # Remove the song names and all the empty strings and pop the last ""
    lyrics = list(filter(None, lyrics[2:]))
    lyrics = lyrics.pop()
    lyrics = "".join(lyrics)

    return lyrics


def is_explict_words_in_track(artist_name: str, track_name: str, scraping_method: Callable) -> int:
    """
    Check if there are any explict words in the song.

    ----- Credits to data.world for bad_words.csv, dataset name "list of bad words" -------

    :param scraping_method: Call different scraping method each time
    :param artist_name: The artist's name.
    :param track_name: The song's name.
    :return: 1 if there are such lyrics else 0
    """
    bad_words_df = pd.read_csv(Path.cwd().parent / "data" / "bad_words.csv")
    bad_words = bad_words_df.iloc[:, 0].to_list()
    lyrics = get_track_html(artist_name, track_name, scraping_method)

    if any(word in bad_words for word in lyrics):
        return 1
    return 0


def main() -> None:
    """ Function that fill blank is_explict in dataset. """
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_with_explict_content.csv")
    df_copy = df.copy()
    sub_df = df.loc[np.logical_and(df["is_explict_content"] != 0,
                                   df["is_explict_content"] != 1), :]
    for idx, instance in sub_df.iterrows():
        artist = instance["artist_name"]
        track = instance["track_name"]
        try:
            sleep(random.randint(5, 20))  # Sleep for randomized time for scraping not getting blocked
            df_copy.loc[idx, "is_explict_content"] = \
                is_explict_words_in_track(artist_name=artist,
                                          track_name=track,
                                          scraping_method=selenium_scraping if idx % 2 == 0
                                          else beautiful_soup_scraping)
        except Status404CounterException:
            df_copy.to_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")
            exit(1)
        except Exception:
            pass  # pass this song...

    print(df_copy["is_explict_content"].isnull().sum())

    df_copy.to_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")


main()
