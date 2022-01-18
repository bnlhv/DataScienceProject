""" This module converts artist textual origin that was brought with crawler to country codes """
import pandas as pd
import pycountry

us_states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
             "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
             "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
             "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
             "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
             "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
             "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
             "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
             "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
             "WI": "Wisconsin",
             "WY": "Wyoming"}


def clean_origin_name(origin):
    if ", " in origin:
        origin = origin.split(", ")[1]
    return origin


def to_country_code(origin):
    try:
        country = pycountry.countries.search_fuzzy(origin)
        if len(country) == 1:
            origin = int(country[0].numeric)
        elif origin in us_states or origin in us_states.values():
            origin = int(pycountry.countries.search_fuzzy('United States of America')[0].numeric)
    except:
        return origin
    return origin


def origin_to_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    df["artist_origin"] = df["artist_origin"].apply(clean_origin_name)
    df["artist_origin"] = df["artist_origin"].apply(to_country_code)
    df = df.rename(columns={'artist_origin': 'country_code'})
    return df
