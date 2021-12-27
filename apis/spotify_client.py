import os
from typing import List

import pandas as pd
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
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
        ))


def url_to_uri(playlists: List) -> List[str]:
    """
    Loop through all playlists end extract URI

    :param playlists: list of spotify playlist links
    :return: list of spotify playlists URIs
    """
    return [link.split("/")[-1].split("?")[0] for link in playlists]


def extract_data_from_playlists(client: Spotify, playlist_URIs: List) -> List:
    """
    Loop through all playlist's tracks and extract features.

    :param client: the client app
    :param playlist_URIs: the URI's for spotify's interaction
    :return: list of tracks
    """
    tracks = []
    i = 0
    for uri in playlist_URIs:
        for track in client.playlist_items(uri)["items"]:
            i += 1
            print(i)
            t = dict()
            try:
                t["track_uri"] = track["track"]["uri"]
                t["track_name"] = track["track"]["name"]
                t["artist_info"] = client.artist(track["track"]["artists"][0]["uri"])
                t["artist_name"] = track["track"]["artists"][0]["name"]
                t["artist_popularity"] = t["artist_info"]["popularity"]
                t["artist_followers"] = t["artist_info"]["followers"]["total"]
                t["artist_genres"] = t["artist_info"]["genres"]
                t["album"] = track["track"]["album"]["name"]
                t["track_popularity"] = track["track"]["popularity"]

                audio_features = client.audio_features(t["track_uri"])[0]
                t["track_danceability"] = audio_features["danceability"]
                t["track_energy"] = audio_features["energy"]
                t["track_loudness"] = audio_features["loudness"]
                t["track_tempo"] = audio_features["tempo"]
                t["track_duration_ms"] = audio_features["duration_ms"]
                t.pop("artist_info")

                tracks.append(t)
            except TypeError:
                pass

    return tracks


def save_tracks_in_csv(tracks: List) -> None:
    """
    Save the tracks that got from API to csv format.

    :param tracks: List of Track dicts
    """
    df = pd.DataFrame(data=tracks, columns=tracks[0].keys())

    df.to_csv(
        path_or_buf="tracks.csv",
        sep=",",
        columns=df.columns
    )


def get_playlists() -> List[str]:
    """
    :return: List of playlists in spotify.
    """
    return [
        "https://open.spotify.com/playlist/5PKZSKuHP4d27SXO5fB9Wl?si=68d4538fb82244f2",
        "https://open.spotify.com/playlist/37i9dQZF1DX2RxBh64BHjQ?si=061e0f903898441a",
        "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=cd24daeb11874d40",
        "https://open.spotify.com/playlist/37i9dQZF1DWWqNV5cS50j6?si=cf76361522214dc0",
        "https://open.spotify.com/playlist/65xSncKQzG6Suseh5gfYP1?si=df4666c35aa1400f",
        "https://open.spotify.com/playlist/37i9dQZF1DWY4xHQp97fN6?si=7e4afb0673a74582",
        "https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk?si=a37fe6f666bf44de",
        "https://open.spotify.com/playlist/37i9dQZF1DWT6MhXz0jw61?si=8ebd6428fda74531",
        "https://open.spotify.com/playlist/37i9dQZF1DXcxvFzl58uP7?si=dbcf0f39e9094137",
        "https://open.spotify.com/playlist/37i9dQZF1DXcWxeqLvgOCi?si=6a385f14564f48b1",
        "https://open.spotify.com/playlist/37i9dQZF1DXc8kgYqQLMfH?si=3b5eb11c884948cd",
        "https://open.spotify.com/playlist/37i9dQZF1DWWjGdmeTyeJ6?si=4251cd434e614650",
        "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR?si=ef98179516a54d2c",
        "https://open.spotify.com/playlist/37i9dQZF1DWVA1Gq4XHa6U?si=5130d5e19f144189",
        "https://open.spotify.com/playlist/37i9dQZF1DWVzZlRWgqAGH?si=3cc3ed45d8114287"
    ]


def main() -> None:
    """ Main function of APIs module. Get the data from the API """
    load_dotenv()
    sp_client = spotify_client()
    URIs = url_to_uri(get_playlists())
    tracks = extract_data_from_playlists(sp_client, URIs)
    save_tracks_in_csv(tracks)


main()
