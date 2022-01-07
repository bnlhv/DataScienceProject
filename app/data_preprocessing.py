from pathlib import Path
import pycountry
import pandas as pd

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
    valid_cols = ["track_uri", "track_name", "artist_name", "artist_popularity", "artist_followers",
                  "artist_genres", "album", "track_popularity", "track_danceability", "track_energy",
                  "track_loudness", "track_tempo", "track_duration_ms", "is_explict_content", "artist_origin"]
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


if __name__ == '__main__':
    df = pd.read_csv(Path.cwd().parent / "data" / "tracks_after_convert_origin_to_country_code.csv")
    df = remove_nan_values(df.copy())
    df = remove_noise_cols(df)
    df = convert_origin_to_country_codes(df)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(Path.cwd().parent / "data" / "tracks_after_convert_origin_to_country_code.csv")
