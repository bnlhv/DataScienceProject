import random
from pathlib import Path
from time import sleep
from typing import Any

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    """ Function that get home town of artists data from ranker.com """
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_preprocessing.csv").copy()
    # df = pd.read_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")
    for idx, instance in df.iterrows():
        artist = instance["artist_name"]
        track = instance["track_name"]
        try:
            sleep(random.randint(5, 20))  # Sleep for randomized time for scraping not getting blocked
            df_copy.loc[idx, "is_explict_content"] = \
                is_explict_words_in_track(artist_name=artist,
                                          track_name=track,
                                          scraping_method=beautiful_soup_scraping)
            # scraping_method=selenium_scraping if idx % 2 == 0
            # else beautiful_soup_scraping)
        except Status404CounterException:
            rows_to_delete.append(idx)
        except Exception:
            pass  # pass this song...

    df_copy.to_csv(Path.cwd().parent / "data" / "tracks_with_explict_content_from_api_and_crawler.csv")
