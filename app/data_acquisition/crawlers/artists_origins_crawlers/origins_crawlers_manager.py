from pathlib import Path

import numpy as np
import pandas as pd

from app.data_acquisition.crawlers.artists_origins_crawlers import famousbirthdays_crawler, ranker_crawler, \
    britannica_crawler


def artist_origin_manager(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manager that gwt all artists orgigin from crawlers.

    :param df: Dataframe to take artists from
    :return: new Dataframe with origins
    """
    df["origin"] = np.NaN
    for artist in df["artist_name"].unique().tolist():
        for crawler in [famousbirthdays_crawler.get_artists_origins,
                        ranker_crawler.get_artists_origins,
                        britannica_crawler.get_artists_origins]:
            try:
                df_crawler = crawler()
                row = df_crawler.index[df_crawler["artist_name"] == artist].tolist()[0]
                artist_origin = df_crawler.loc[row, "origin"]
                df.loc[df["artist_name"] == artist, "artist_origin"] = artist_origin
                break
            except Exception:
                pass

    df.to_csv(
        path_or_buf=Path.cwd().parent / "data" / "04_origin_feature_update_from_crawler.csv",
        sep=",",
        columns=df.columns
    )

    return df
