from pathlib import Path

# import mlb as mlb
import pandas as pd
import pycountry
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import itertools
from collections import Counter

states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
          "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
          "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
          "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
          "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
          "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin",
          "WY": "Wyoming"}


def remove_noise_cols(df: pd.DataFrame) -> pd.DataFrame:
    valid_cols = ["track_uri", "artist", "artist_popularity", "artist_followers",
                  "artist_genres", "track_popularity", "track_danceability", "track_energy",
                  "track_loudness", "track_tempo", "track_duration_ms", "is_explict_content", "country_code"]
    cols_to_remove = list(filter(lambda x: x not in valid_cols, df.columns))

    return df.drop(columns=cols_to_remove)


def remove_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def clean_origin_name(origin):
    if ", " in origin:
        origin = origin.split(", ")[1]
    return origin


def to_country_code(origin):
    try:
        country = pycountry.countries.search_fuzzy(origin)
        if len(country) == 1:
            origin = int(country[0].numeric)
        elif origin in states or origin in states.values():
            origin = int(pycountry.countries.search_fuzzy('United States of America')[0].numeric)
    except:
        return origin
    return origin


def convert_origin_to_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    df["artist_origin"] = df["artist_origin"].apply(clean_origin_name)
    df["artist_origin"] = df["artist_origin"].apply(to_country_code)
    df = df.rename(columns={'artist_origin': 'country_code'})
    return df


def parse_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Function that parses string saves Series column to Tuple.
    This is for the `artist_genres` column.

    :param df: the dataframe to change.
    :param col: the column to parse.
    :return updated Dataframe
    """
    df_copy = df.copy()
    df_copy[col] = pd.Series([eval(instance[col]) for idx, instance in df_copy.iterrows()])

    return df_copy


def convert_artist_genres_to_dummies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that operates on `artist_genres` in Dataframe and return df with dummies.

    :param df: The given Dataframe to preform action on.
    :return: new Dataframe
    """
    mlb = MultiLabelBinarizer()

    # Numpy matrix of dummies
    genres = mlb.fit_transform(df["artist_genres"])

    df_genres = pd.DataFrame(data=genres, columns=mlb.classes_)

    # return concatenated dataframe
    return pd.concat([df, df_genres], axis=1)


def drop_correlated_dummy_genre_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that drop high correlated features of the `artist_genres` dummy features.

    :param df: the Dataframe to preform action on
    :return: new Dataframe
    """
    # Get correlation matrix
    corr = df.corr()

    # Create a mask for values above 90%
    # But also below 100% since it variables correlated with the same one
    mask = (df.corr() > 0.9) & (df.corr() < 1.0)
    high_corr = corr[mask]

    # Create a new column mask using any() and ~
    col_to_filter_out = ~high_corr[mask].any()

    # Apply new mask
    X_clean = df[high_corr.columns[col_to_filter_out]]

    return X_clean


def artist_genres_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that handles all this pipeline.

    :param df: the Dataframe to preform action on
    :return: new Dataframe
    """
    df_copy = parse_column(df, "artist_genres")
    df_copy = convert_artist_genres_to_dummies(df_copy)
    df_copy = drop_correlated_dummy_genre_features(df_copy)

    return df_copy


def convert_artist_genres_to_dummies2(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = parse_column(df, col)
    list_of_genres = list(itertools.chain(*df[col]))
    occurrences = Counter(list_of_genres)
    popular_genres = ['pop', 'rock', 'rap', 'country', 'mellow gold', 'country', 'edm', 'house', 'metal',
                      'soul',
                      'r&b', 'permanent wave', 'urban contemporary', 'adult standards', 'electro', 'alt z', 'hip pop',
                      'motown',
                      'quiet storm', 'funk', 'singer-songwriter', 'folk', 'disco', 'neo mellow']

    for genre in popular_genres:
        df[genre] = 0

    for i, genre_tuple in enumerate(df[col]):
        for genre in genre_tuple:
            for popular_genre in popular_genres:
                if genre in popular_genre:
                    df.loc[i, popular_genre] = 1

    df["hip pop"] = 0
    df["trap"] = 0
    for i, genre_tuple in enumerate(df[col]):
        for genre in genre_tuple:
            if genre == "hip pop":
                df.loc[i, "hip pop"] = 1
            if genre == "trap":
                df.loc[i, "trap"] = 1
    return df


if __name__ == '__main__':
    # labelEncoder = LabelEncoder()
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_convert_artist_name_to_nominal.csv")
    df = convert_artist_genres_to_dummies2(df, "artist_genres")
    print("")
    # df = remove_nan_values(df.copy())
    # df["artist"] = labelEncoder.fit_transform(df["artist_name"])
    # df = remove_noise_cols(df)
    # df = convert_origin_to_country_codes(df)
    # df.reset_index(drop=True, inplace=True)
    df.to_csv(Path.cwd().parent / "data" / "final_dataset.csv")
