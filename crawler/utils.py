from typing import Any

import requests
from bs4 import BeautifulSoup

AZLYRICS_URL = "https://www.azlyrics.com/lyrics"
RANKER_URL = "https://www.ranker.com/fact-lists/recording-artists-and-groups/hometown"


class Status404CounterException(BaseException):
    pass


def beautiful_soup_scraping(url: str, *args: Any, **kwargs: Any) -> str:
    """
    Scrape with Beautiful Soup generic.

    :param url: the Url to fetch the data from
    :return: text of element that is sent in *args and **kwargs
    """
    response = requests.get(url)
    if response.status_code == 404:
        raise Status404CounterException()

    soup = BeautifulSoup(response.text, "lxml")
    return soup.find(*args, **kwargs).text
