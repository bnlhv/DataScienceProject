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
    audio_features = client.audio_features(track["track"]["uri"])[0]

    return dict(
        track_uri=track["track"]["uri"],
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
    i = 0
    for uri in playlist_URIs:
        try:
            results = client.playlist_items(uri)
            tracks = results["items"]
            i += len(tracks)
            print(i)
            [t.append(construct_track_from_response(client, track)) for track in tracks]
            while results["next"]:
                results = client.next(results)
                tracks = results["items"]
                i += len(tracks)
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
        "https://open.spotify.com/playlist/37i9dQZF1DX9PXZbuB8BjJ?si=bb862919df804292",  # Rap Diggers
        "https://open.spotify.com/playlist/0h9Gaqt2sNJ8M5aMV3h9BO?si=0b8ecf1d9c254225",  # Rap Classics 90-00
        "https://open.spotify.com/playlist/37i9dQZF1DX5Ejj0EkURtP?si=d77e1bd4807a4ed7",  # All Out 2010s
        "https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd?si=7f6ca13b63fc441b",  # All Out 2000s
        "https://open.spotify.com/playlist/37i9dQZF1DXbpLIJzuZ9tc?si=d99f34cff35640ca",  # Deep Dive: 70s Pop
        "https://open.spotify.com/playlist/37i9dQZF1DX50zbPdCCGia?si=3ad8e465ba164cc8",  # 70s Soft Rock
        "https://open.spotify.com/playlist/37i9dQZF1DX6hO1vx5AApi?si=e5ae3123f00b4ccc",  # Sad 70s
        "https://open.spotify.com/playlist/37i9dQZF1DWTTn6daQVbOa?si=832bf723aabd455d",  # Soft 70s
        "https://open.spotify.com/playlist/37i9dQZF1DWWzVPEmatsUB?si=c54a263e8a734792",  # Mellow Morning
        "https://open.spotify.com/playlist/37i9dQZF1DX504r1DvyvxG?si=731d877176dc4fd2",  # Classic Acoustic
        "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6?si=ee711a30d7be48a2",  # Chill Hits
        "https://open.spotify.com/playlist/37i9dQZF1DX1clOuib1KtQ?si=a8e551a25af74b3f",  # This is Eminem
        "https://open.spotify.com/playlist/37i9dQZF1DX45xYefy6tIi?si=ba0a03b0ff434e2c",  # The Last Dance
        "https://open.spotify.com/playlist/37i9dQZF1DWXNFSTtym834?si=d743a4c0e2ce4eca",  # 00s Metal Classics
        "https://open.spotify.com/playlist/37i9dQZF1DX1kydukZhLms?si=94cca41b2a9147c6",  # Metal Ballads
        "https://open.spotify.com/playlist/37i9dQZF1DXcfZ6moR6J0G?si=74fa7ec9fd414728",  # Nu Metal Generation
        "https://open.spotify.com/playlist/37i9dQZF1DX2LTcinqsO68?si=977aceb0c62f40a7",  # Old School Metal
        "https://open.spotify.com/playlist/37i9dQZF1DX5J7FIl4q56G?si=74439a5da28747bd",  # New Metal Tracks
        "https://open.spotify.com/playlist/37i9dQZF1DWXbttAJcbphz?si=5ad3bb1ae96547f7",  # I Love My 2010s R&B
        "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4?si=487e991498e848c3",  # Feelin' Good
        "https://open.spotify.com/playlist/37i9dQZF1DX82GYcclJ3Ug?si=d8aa4e9c40154753",  # The New Alt
        "https://open.spotify.com/playlist/37i9dQZF1DWT59aKliWtId?si=de1144284d2b4d34",  # Grade A
        "https://open.spotify.com/playlist/37i9dQZF1DXa6YOhGMjjgx?si=bdf4f769e038464b",  # New Alt Rock Mixtape
        "https://open.spotify.com/playlist/37i9dQZF1DX9GRpeH4CL0S?si=8301c1428d714f8a",  # Essential Alternative
        "https://open.spotify.com/playlist/37i9dQZF1DX873GaRGUmPl?si=f5f1b27b114149ea",  # Alternative 10s
        "https://open.spotify.com/playlist/37i9dQZF1DX0YKekzl0blG?si=c677a6f91f684afc",  # Alternative 00s
        "https://open.spotify.com/playlist/37i9dQZF1DWWvhKV4FBciw?si=15ccf78f4ec84622",  # Funk & Soul
        "https://open.spotify.com/playlist/37i9dQZF1DWT7oUl2XAhgF?si=6f90fabdd5ba4e25",  # Retro Soul
        "https://open.spotify.com/playlist/37i9dQZF1DWULEW2RfoSCi?si=a3c4c3394382433b",  # 70s Soul Classics
        "https://open.spotify.com/playlist/37i9dQZF1DX62Nfha2yFhL?si=a45a39af4312457e",  # Soul Lounge
        "https://open.spotify.com/playlist/37i9dQZF1DWTx0xog3gN3q?si=1f342114bae04e40",  # Uplifting Soul Classics
        "https://open.spotify.com/playlist/37i9dQZF1DWTkxQvqMy4WW?si=510e2908f32c4d1c",  # Chillin' On a Dirt Road
        "https://open.spotify.com/playlist/37i9dQZF1DX5OrO2Jxuvdn?si=de2256cc29724337",  # Country Workout
        "https://open.spotify.com/playlist/37i9dQZF1DWZBCPUIUs2iR?si=023c1fff5b634072",  # Country's Greatest Hits
        "https://open.spotify.com/playlist/37i9dQZF1DX8S0uQvJ4gaa?si=446ba0623f214e18",  # New Boots
        "https://open.spotify.com/playlist/37i9dQZF1DX8WMG8VPSOJC?si=cf6c020ff8e54708",  # Country Kind Of Love
        "https://open.spotify.com/playlist/37i9dQZF1DWWH0izG4erma?si=2e6cd7eb91bc4af6",  # Country Rocks
        "https://open.spotify.com/playlist/37i9dQZF1DX3LyU0mhfqgP?si=04ed0de514a444eb",  # Out Now
        "https://open.spotify.com/playlist/37i9dQZF1DX59HcpGmPXYR?si=a53bf619f8cd492b",  # Pride Classics
        "https://open.spotify.com/playlist/37i9dQZF1DWViyN2b86Qnu?si=ba12099e63c44324",  # Transcend
        "https://open.spotify.com/playlist/37i9dQZF1DWTLrNDPW5co2?si=196b55e70e0746d8",  # Club Resistance
        "https://open.spotify.com/playlist/37i9dQZF1DWTMR78LDoAZC?si=043dd9f7d79c4dc5",  # Alternative Pride
        "https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO?si=ae6ac1cea2a14802",  # Dance Hits
        "https://open.spotify.com/playlist/37i9dQZF1DWSf2RDTDayIx?si=929765c14cc742a3",  # Happy Beats
        "https://open.spotify.com/playlist/37i9dQZF1DXccH49bh52dB?si=55bd0720b7e445a9",  # Chilled Dance Hits
        "https://open.spotify.com/playlist/37i9dQZF1DWTwnEm1IYyoj?si=3e0133c3fdd244f3",  # Soft Pop Hits
        "https://open.spotify.com/playlist/37i9dQZF1DWUZMtnnlvJ9p?si=77a05c8d08034aa1",  # The Ultimate Hit Mix
    ]


def main() -> None:
    """ Main function of APIs module. Get the data from the API """
    load_dotenv()
    sp_client = spotify_client()
    URIs = url_to_uri(get_playlists()[:10])
    tracks = extract_data_from_playlists(sp_client, URIs)
    save_tracks_in_csv(tracks)


main()
