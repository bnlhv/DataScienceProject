from pathlib import Path
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup

from crawler.utils import beautiful_soup_scraping, Status404CounterException


def get_list_of_origins() -> List:
    """
    Preform request to the Ranker Api site

    :return: response entity
    """
    response = requests.post(url="https://cache-api.ranker.com/lists/es/query",
                             headers={
                                 "authority": "cache-api.ranker.com",
                                 "accept": "*/*",
                                 "content-type": "application/json",
                                 "origin": "https://www.ranker.com"
                             },
                             json={
                                 "factBased": "true",
                                 "paginationProperties": {"offset": 0, "limit": "360"},
                                 "sourceConfigurationIds": ["157"],
                                 "sourceList": "true"
                             }
                             )

    return response.json()["rankerLists"]


def main_loop(origin_data: List) -> List[Dict]:
    """
    Function that run main loop crawler at the site and parse HTML with bs4

    :param origin_data: the homepage data
    :return: final data of artist and their origin
    """
    origins = [origin["name"].split("from ")[-1] for origin in origin_data]
    links = ["https://" + link["url"][2:] for link in origin_data]
    data = []

    for origin, link in zip(origins, links):
        i = 1
        while True:
            try:
                ul_artists = beautiful_soup_scraping(BeautifulSoup.find,
                                                     link + f"?page={i}",
                                                     "ul", {"class": "gridView_list__1HGxW undefined"})
                for li_artist in ul_artists.find_all("li"):
                    if li_artist.get("class") == "gridItem_main__1ilxA gridItem_hasMedia__38WR2 gridItem_hasRank__3kRup" \
                                                 " gridItem_nonVotable__a5Xlj gridItem_hasProps__3R_km " \
                                                 "gridItem_bigGrid__1Camu gridItem_upVote__1WPgM".split(" "):
                        a = li_artist.find("a", {"class": "gridItem_name__wCyGi"})
                        if a:
                            artist_name = a.text
                            data.append(
                                {
                                    "artist_name": artist_name,
                                    "origin": origin
                                }
                            )
            except Status404CounterException:
                break
            else:
                i += 1

    return data


if __name__ == '__main__':
    """ Function that get home town of artists data from ranker.com """
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing.csv").copy()
    origin_data = get_list_of_origins()
    data = main_loop(origin_data)
    pd.DataFrame(data).to_csv(Path.cwd().parent / "data" / "artists_and_origins.csv")
