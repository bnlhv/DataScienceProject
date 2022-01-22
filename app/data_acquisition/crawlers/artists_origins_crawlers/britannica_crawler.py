"""
This module finds artists origins from britannica's site
"""
import pandas as pd
from bs4 import BeautifulSoup

from app.data_acquisition.crawlers.utils import beautiful_soup_scraping, Status404CounterException, BRITANNICA_URL


def get_artists_origins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Iterate on the artists names and fins their origin in britannica

    :param df: the dataframe with artists
    :return: dataframe of artists and origins from this crawler
    """
    artists = df.copy().loc[df["artist_origin"].isnull(), "artist_name"].unique().tolist()
    results = []

    for artist in artists:
        try:
            soup = beautiful_soup_scraping(BeautifulSoup.find,
                                           BRITANNICA_URL + "-".join(artist.split(" ")),
                                           "dd", {"class": "d-inline"})
            dt = beautiful_soup_scraping(BeautifulSoup.find,
                                         BRITANNICA_URL + "-".join(artist.split(" ")),
                                         "dt", {"class": "d-inline"})
            if "born" in dt.text.lower():
                soup = soup.find_all("span", "fact-item")
                origin = soup[-1].find("a").text
                results.append(
                    {
                        "artist_name": artist,
                        "origin": origin
                    }
                )
        except Status404CounterException:
            pass
        except AttributeError:
            pass

    return pd.DataFrame(results)
