from typing import Any, Callable

import requests
from bs4 import BeautifulSoup

AZLYRICS_URL = "https://www.azlyrics.com/lyrics"
RANKER_URL = "https://www.ranker.com/fact-lists/recording-artists-and-groups/hometown"
BRITANNICA_URL = "https://www.britannica.com/biography/"


class Status404CounterException(BaseException):
    pass


def beautiful_soup_scraping(method: Callable, url: str, *args: Any, **kwargs: Any) -> str:
    """
    Scrape with Beautiful Soup generic.

    :param url: the Url to fetch the data from
    :return: text of element that is sent in *args and **kwargs
    """
    response = requests.get(url)
    if response.status_code == 404:
        # todo: remove this
        print("404")
        raise Status404CounterException()

    soup = BeautifulSoup(response.text, "lxml")
    return soup.find(*args, **kwargs) if method == BeautifulSoup.find else soup.find_all(*args, **kwargs)
