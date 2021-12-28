import random
from pathlib import Path
from time import sleep
from typing import Callable

import pandas as pd
import requests
from bs4 import BeautifulSoup

from crawler.chrome_driver import driver

base_url = "https://www.azlyrics.com/lyrics"


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
    response = requests.get(url)
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
    df_copy.drop_duplicates(inplace=True)
    for idx, instance in df.iterrows():
        artist = instance["artist_name"]
        track = instance["track_name"]
        try:
            if instance.isnull().sum() == 1:  # Must be in is_explict_content
                sleep(random.randint(10, 30))  # Sleep for randomized time for scraping not getting blocked
                df_copy.loc[idx, "is_explict_content"] = \
                    is_explict_words_in_track(artist_name=artist,
                                              track_name=track,
                                              scraping_method=selenium_scraping if idx % 2 == 0
                                              else beautiful_soup_scraping)
        except Exception:
            pass

    print(df_copy["is_explict_content"].isnull().sum())

    df_copy.to_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")


main()
