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


def clean_origin_name(origin) -> str:
    """
    Function that retuns only State if the value inside is like for example:
    'Los Angeles, California' -> 'California'

    :param origin: string value with or without ,
    :return: string without ,
    """
    if ", " in origin:
        origin = origin.split(", ")[1]
    return origin


def to_country_code(origin) -> int:
    """
    Function that convert the string value to int with pycountry package.

    :param origin: place name
    :return: integer of country code
    """
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
    """
    Function that manages convert of the string value place to the country code protocol.

    :param df: Dataframe to change
    :return: Changed dataframe
    """
    df["origin"] = df["origin"].apply(clean_origin_name)
    df["origin"] = df["origin"].apply(to_country_code)
    df = df.rename(columns={'origin': 'country_code'})
    return df
