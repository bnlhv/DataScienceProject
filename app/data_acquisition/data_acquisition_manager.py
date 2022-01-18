from pathlib import Path

import pandas as pd

from apis.deezer_client import deezer_manager
from apis.spotify_client import spotify_manager
from crawlers.artists_origins_crawlers.origins_crawlers_manager import artist_origin_manager
from crawlers.lyrics_crawlers.lyrics_crawler import lyrics_crawler_manager


def manage() -> pd.DataFrame:
    """
    Manager of the Data acquisition module.

    :return: new Dataframe
    """
    df = spotify_manager()
    for func in [deezer_manager, lyrics_crawler_manager, artist_origin_manager]:
        df = func(df)
    df.to_csv(
        path_or_buf=Path.cwd().parent / "data" / "05_raw_data_from_apis_and_crawlers.csv",
        sep=",",
        columns=df.columns
    )

    return df

manage()
