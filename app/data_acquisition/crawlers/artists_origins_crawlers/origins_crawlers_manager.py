"""
This module manage all origin crawlers and [britannica, famousbirthdays & ranker]
"""
from pathlib import Path

import numpy as np
import pandas as pd

from app.data_acquisition.crawlers.artists_origins_crawlers import famousbirthdays_crawler, ranker_crawler, \
    britannica_crawler


def artist_origin_manager(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manager that gwt all artists origin from crawlers.

    :param df: Dataframe to take artists from
    :return: new Dataframe with origins
    """
    df["origin"] = np.NaN
    df_famous = pd.read_csv(Path.cwd().parent.parent.parent / "data" / "artists_and_origins_famousbirthdays.csv")
    df_ranker = pd.read_csv(Path.cwd().parent.parent.parent / "data" / "artists_and_origins_ranker.csv")
    df_britannica = pd.read_csv(Path.cwd().parent.parent.parent / "data" / "artists_and_origins_britannica.csv")
    # todo: remove this
    found_counter = 1
    not_found_counter = 1
    for artist in df["artist_name"].unique().tolist():
        # for crawler in [famousbirthdays_crawler.get_artists_origins,
        #                 ranker_crawler.get_artists_origins,
        #                 britannica_crawler.get_artists_origins]:
        # todo: remove this
        for df_crawler in [df_famous, df_ranker, df_britannica]:
            try:
                # df_crawler = crawler()
                row = df_crawler.index[df_crawler["artist_name"] == artist].tolist()[0]
                artist_origin = df_crawler.loc[row, "origin"]
                df.loc[df["artist_name"] == artist, "artist_origin"] = artist_origin
                # todo: remove this
                found_counter += 1
                print(f"found = {found_counter}")
                break
            except Exception:
                not_found_counter += 1
                print(f"not found = {not_found_counter}")
                pass
        # todo: remove this
        print(f"finished {artist}")

    df.to_csv(
        path_or_buf=Path.cwd().parent.parent.parent / "data" / "04_origin_feature_update_from_crawler.csv",
        sep=",",
        columns=df.columns
    )
    # todo: remove this
    print("saved_csv")
    return df

artist_origin_manager(pd.read_csv(Path.cwd().parent.parent.parent / "data" /
                                  "02_tracks_from_spotify_with_word_count.csv"))

