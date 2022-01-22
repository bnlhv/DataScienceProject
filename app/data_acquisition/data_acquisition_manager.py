"""
This module is the data acquisition manager, it creates a pipeline and go through
all apis and crawlers for data fetching.
"""
from pathlib import Path

from apis.deezer_client import deezer_manager
from apis.spotify_client import spotify_manager
from app.data_acquisition.apis.genius_client import genius_manager
from app.data_acquisition.crawlers.lyrics_crawlers.lyrics_crawler import lyrics_crawler_manager
from crawlers.artists_origins_crawlers.origins_crawlers_manager import artist_origin_manager


def manage() -> None:
    """
    Manager of the Data acquisition module.

    :return: new Dataframe
    """
    df = spotify_manager()
    for func in [genius_manager, deezer_manager, lyrics_crawler_manager, artist_origin_manager]:
        df = func(df)
    df.to_csv(
        path_or_buf=Path.cwd() / "05_raw_data_from_apis_and_crawlers.csv",
        sep=",",
        columns=df.columns
    )


if __name__ == '__main__':
    manage()
