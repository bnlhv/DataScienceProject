from pathlib import Path
from typing import List, Dict

import pandas as pd
from bs4 import BeautifulSoup

from crawler.utils import beautiful_soup_scraping, Status404CounterException, BRITANNICA_URL


def get_empty_origin_artists(df: pd.DataFrame) -> List:
    """
    Extract  artists with no origin in the dataset

    :param df: the Dataframe
    :return: List of these artists
    """
    return df.copy().loc[df["artist_origin"].isnull(), "artist_name"].unique().tolist()


def main_loop(df: pd.DataFrame) -> List[Dict]:
    """
    Iterate on the artists names and fins their origin in britannica

    :param df: the dataframe with artists
    :return: List of artists and their origin if found
    """
    artists = get_empty_origin_artists(df)
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

    return results


if __name__ == '__main__':
    """ Function that get home town of artists data from ranker.com """
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing_with_origins.csv").copy()
    results = main_loop(df)
    pd.DataFrame(results).to_csv(Path.cwd().parent / "data" / "artists_and_origins2.csv")
