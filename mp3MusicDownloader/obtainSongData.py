# -*- coding: utf-8 -*-
"""Spotifyから楽曲名より楽曲情報を検索する
"""
from typing import Final
from pprint import pprint

import spotipy # type: ignore

from mp3MusicDownloader.env import SPOTIFY_CLIENT_KEY


__keyword: str = ""
__song_data: dict = {}

CLIENT_ID: Final[str] = '448b8c4a938e479782456a1170b82f9f' # App作成時のCliend ID
CLIENT_SECRET: Final[str] = SPOTIFY_CLIENT_KEY
CLIENT_CREDENTIALS_MANAGER: Final[spotipy.oauth2.SpotifyClientCredentials] = spotipy.oauth2.SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
SP: Final[spotipy.client.Spotify] = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)


def get_data(keyword: str) -> dict:
    """楽曲情報をキーワード検索する

    Args:
        keyword (str): 検索文字列

    Returns:
        dict: spofity web apiから送られてくるデータそのまま 一曲分のデータしか来ないようにしてある
    """
    global __song_data, __keyword
    
    if __keyword == "" or __keyword != keyword:
        __song_data = SP.search(keyword, type="track", limit=1)
    __keyword = keyword

    return __song_data


def get_artists(keyword: str) -> list:
    """楽曲のアーティスト情報をキーワード検索する

    Args:
        keyword (str): 検索文字列

    Returns:
        list: アーティストのリスト
    """
    global __song_data, __keyword

    if __keyword == "" or __keyword != keyword:
        __song_data = get_data(keyword)
    __keyword = keyword
    
    try:
        artists = [i.get("name") for i in __song_data.get("tracks").get("items")[0].get("artists")]
    except IndexError:
        artists = []
    
    return artists


def get_title(keyword: str) -> str:
    """楽曲の正式なタイトルをキーワード検索する

    Args:
        keyword (str): 検索文字列

    Returns:
        str: タイトル
    """
    global __song_data, __keyword
    
    if __keyword == "" or __keyword != keyword:
        __song_data = get_data(keyword)
    __keyword = keyword
        
    try:
        title = __song_data.get("tracks").get("items")[0].get("name")
    except IndexError:
        title = ""
    
    return title

def get_date(keyword: str) -> str:
    """楽曲の提供日時をキーワード検索する

    Args:
        keyword (str): 検索文字列
    Returns:
        str: 提供日時
    """
    global __song_data, __keyword
    
    if __keyword == "" or __keyword != keyword:
        __song_data = get_data(keyword)
    __keyword = keyword
       
    try: 
        date = __song_data.get("tracks").get("items")[0].get("album").get("release_date")
    except IndexError:
        date = ""
    
    return date