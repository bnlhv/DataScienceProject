import os
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests
from dotenv import load_dotenv
from spotipy import Spotify, SpotifyClientCredentials


def spotify_client() -> Spotify:
    """
    Create a spotify client app instance.

    :return: Spotify instance
    """
    return Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            requests_timeout=60
        ))


def url_to_uri(playlists: List) -> List[str]:
    """
    Loop through all playlists end extract URI

    :param playlists: list of spotify playlist links
    :return: list of spotify playlists URIs
    """
    return [link.split("/")[-1].split("?")[0] for link in playlists]


def construct_track_from_response(client: Spotify, track: Spotify.track) -> Dict:
    """
    Function that gets a json response object and construct some values for dict

    :param client: spotify client
    :param track: json spotify track response
    :return: dict of this track
    """
    artist_info = client.artist(track["track"]["artists"][0]["uri"])
    track_uri = client.audio_features(track["track"]["uri"])[0]
    audio_features = client.audio_features(track_uri)[0]

    return dict(
        track_uri=track_uri,
        track_name=track["track"]["name"],
        artist_name=track["track"]["artists"][0]["name"],
        artist_popularity=artist_info["popularity"],
        artist_followers=artist_info["followers"]["total"],
        artist_genres=tuple(artist_info["genres"]),  # pandas can't hash lists
        album=track["track"]["album"]["name"],
        track_popularity=track["track"]["popularity"],
        track_danceability=audio_features["danceability"],
        track_energy=audio_features["energy"],
        track_loudness=audio_features["loudness"],
        track_tempo=audio_features["tempo"],
        track_duration_ms=audio_features["duration_ms"]
    )


def extract_data_from_playlists(client: Spotify, playlist_URIs: List) -> List:
    """
    Loop through all playlist's tracks and extract features.

    :param client: the client app
    :param playlist_URIs: the URI's for spotify's interaction
    :return: list of tracks
    """
    t = []
    for uri in playlist_URIs:
        try:
            results = client.playlist_items(uri)
            tracks = results["items"]
            [t.append(construct_track_from_response(client, track)) for track in tracks]
            while results["next"]:
                results = client.next(results)
                tracks = results["items"]
                [t.append(construct_track_from_response(client, track)) for track in tracks]
        except TypeError:  # different song name maybe
            pass
        except requests.exceptions.ReadTimeout:  # some can't read
            pass

    return t


def save_tracks_in_csv(tracks: List) -> None:
    """
    Save the tracks that got from API to csv format.

    :param tracks: List of Track dicts
    """
    df = pd.DataFrame(data=tracks, columns=tracks[0].keys())
    df.drop_duplicates(subset=["track_name", "artist_name"])  # Supposing that each song can appear in different playlists
    df.to_csv(
        path_or_buf=Path.cwd().parent / "data" / "tracks.csv",
        sep=",",
        columns=df.columns
    )


def get_playlists() -> List[str]:
    """
    :return: List of playlists in spotify.
    """
    return [
        "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",  # Today's Top Hits
        "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U",  # Rock Classics
        "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",  # Rap Caviar
        "https://open.spotify.com/playlist/37i9dQZF1DX4SBhb3fqCJd",  # Are & Be
        "https://open.spotify.com/playlist/37i9dQZF1DWVqfgj8NZEp1",  # Coffee Table Jazz
        "https://open.spotify.com/playlist/37i9dQZF1DX9stbPFTxeaB",  # Funky Heavy Bluesy
        "https://open.spotify.com/playlist/37i9dQZF1DX1lVhptIYRda",  # Hot Country
        "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0",  # Classical Essentials
        "https://open.spotify.com/playlist/37i9dQZF1DX10zKzsJ2jva",  # Viva Latino
        "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",  # Chill Hits
        "https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP",  # Beast Mode
        "https://open.spotify.com/playlist/37i9dQZF1DWY4xHQp97fN6",  # Get Turnt
        "https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk",  # Mega Hit Mix
        "https://open.spotify.com/playlist/37i9dQZF1DX6aTaZa0K6VA",  # Pop Up
        "https://open.spotify.com/playlist/37i9dQZF1DXcF6B6QPhFDv",  # Rock This
        "https://open.spotify.com/playlist/37i9dQZF1DX186v583rmzp",  # I Live My 90's Hip Hop
        "https://open.spotify.com/playlist/37i9dQZF1DX2RxBh64BHjQ",  # Most Necessary
        "https://open.spotify.com/playlist/37i9dQZF1DWVA1Gq4XHa6U",  # Gold School
        "https://open.spotify.com/playlist/37i9dQZF1DWYmmr74INQlb",  # I Love My 00's R&B
        "https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif",  # Dance Party
        "https://open.spotify.com/playlist/6ZTpgxK6BT92mmsqwETj9l",  # Rap Nation
        "https://open.spotify.com/playlist/1Pc5ExsgvUdkne29mAVvNJ",  # Dancehall Mix
        "https://open.spotify.com/playlist/37i9dQZF1DX0b1hHYQtJjp?si=7ec0fd04c09c49fb",  # Just Good Music
        "https://open.spotify.com/playlist/31ymdYCITDnZRtkKzP3Itp?si=2e868927fa894a35",  # Populat Music
        "https://open.spotify.com/playlist/37i9dQZF1DWSvKsRPPnv5o?si=5695c5fcf49e440e",  # Westside Story
        "https://open.spotify.com/playlist/37i9dQZF1DXe4Cw8IKKIvr?si=554c13bc3d024228",
        # Legendary Labels: Bad Boy Records
        "https://open.spotify.com/playlist/37i9dQZF1DXcDoDDetPsEg?si=378d7665a2734b12",  # Who We Be
        "https://open.spotify.com/playlist/0MSCX9tZWQmitMQsfhvZIl?si=d297420836654ab9",  # Indie Playlist
        "https://open.spotify.com/playlist/37i9dQZF1DXa9wYJr1oMFq?si=a3ff0c8bdf54433e",  # Pop Punk Powerhouses
        "https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL?si=08acd35737cf4919",  # Rock Party
        "https://open.spotify.com/playlist/5PKZSKuHP4d27SXO5fB9Wl?si=662f021dd96948c0",  # Best New Music
        "https://open.spotify.com/playlist/37i9dQZF1DWWqNV5cS50j6?si=b1c9e339aadd4f30",  # Anti Pop
        "https://open.spotify.com/playlist/65xSncKQzG6Suseh5gfYP1?si=7e701aa2e3744254",  # Pigeons & Planes
        "https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk?si=4870c337d6194d03",  # New Music Friday
        "https://open.spotify.com/playlist/37i9dQZF1DWT6MhXz0jw61?si=7af9e4960660478d",  # Mellow Bars
        "https://open.spotify.com/playlist/37i9dQZF1DXcxvFzl58uP7?si=b86f1c82df744edc",  # Bedroom Pop
        "https://open.spotify.com/playlist/37i9dQZF1DXc8kgYqQLMfH?si=b20dbdf703c64418",  # Lush Lofi
        "https://open.spotify.com/playlist/37i9dQZF1DWWjGdmeTyeJ6?si=112fb8dd6dee4939",  # Fresh Finds
        "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR?si=eea2cf11bc904049",  # Sad Indie
        "https://open.spotify.com/playlist/37i9dQZF1DWVzZlRWgqAGH?si=0fc2e31737a5454a",  # Butter
    ]


def main() -> None:
    """ Main function of APIs module. Get the data from the API """
    load_dotenv()
    sp_client = spotify_client()
    URIs = url_to_uri(get_playlists())
    tracks = extract_data_from_playlists(sp_client, URIs)
    save_tracks_in_csv(tracks)


main()
