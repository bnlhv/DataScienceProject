import itertools

import pandas as pd

from app.data_preparation.utils import parse_column


def popular_genre_dummies(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function is reducing the dummy features genres potential from 800+ to 15~

    :param df: the input Dataframe to work on
    :return: Dataframe with new dummy features
    """
    df_copy = parse_column(df, "artist_genres")
    set_of_genres = set(list(itertools.chain(*df_copy["genres"])))
    popular_genres = ['pop', 'rock', 'rap', 'country', 'edm', 'house', 'metal', 'soul',
                      'r&b', 'electro', 'hip hop', 'funk', 'folk', 'disco']
    """
    This dict is going to be:
    {
        "energy pop": ["pop"],
        "hip pop": ["hip hop", "european rap", ....],
        ...
    }
    """
    all_sub_genres = dict()
    # Initialization of new features of only popular_genres
    df_copy = df_copy.join(pd.DataFrame(0, columns=popular_genres, index=df_copy.index))
    # Turn to set to get only uniques
    for genre in list(set_of_genres):
        all_sub_genres[genre] = [popular_genre for popular_genre in popular_genres if
                                 any(popular_genre.split()) in genre]
    for popular_genre in popular_genres:
        df_copy[popular_genre] = [1 if popular_genre in any(instance["genres"]) else 0 for idx, instance in
                                  df_copy.iterrows()]
    # Assign 1 to dummy feature other genre if all others are 0's
    df_copy["other_genre"] = [1 if not any([df_copy.loc[idx, col] for col in df_copy.columns if col in popular_genres])
                              else 0 for idx, _ in df_copy.iterrows()]

    return df_copy.drop(columns=["genres"])