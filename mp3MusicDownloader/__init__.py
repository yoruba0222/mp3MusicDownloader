# -*- coding: utf-8 -*-
"""mp3 downloader
"""
import os
from typing import Final

import tqdm # type: ignore
import fire # type: ignore
from term_printer import Color, cprint # type: ignore

import mp3MusicDownloader.obtainSongData as songData
import mp3MusicDownloader.obtainYoutubeData as youtubeData
import mp3MusicDownloader.grantMetaData as metaData


DIR_PATH: Final[str] = "./"


def grantTitle() -> None:
    files: list[str] = os.listdir(DIR_PATH)
    
    for file in tqdm.tqdm(files, desc="GrantingData"):
        title = songData.get_title(file[4:-4])
        metaData.grantTitle(file, title)
        
        
def grantArtists() -> None:
    files: list[str] = os.listdir(DIR_PATH)
    
    for file in tqdm.tqdm(files, desc="GrantingData"):
        artists = songData.get_artists(file[4:-4])
        
        metaData.grantartists(file, artists)
        

def grantDate() -> None:
    files: list[str] = os.listdir(DIR_PATH)
    
    for file in tqdm.tqdm(files, desc="GrantingData"):
        date = songData.get_date(file[4:-4])
        
        metaData.grantDate(file, date)
    
    
def grantAllData() -> None:
    files: list[str] = os.listdir(DIR_PATH)
    
    for file in tqdm.tqdm(files, desc="GrantingData"):
        title = songData.get_title(file[4:-4])
        artists = songData.get_artists(file[4:-4])
        date = songData.get_date(file[4:-4])
        
        metaData.grantartists(file, artists)
        metaData.grantDate(file, date)
        metaData.grantTitle(file, title)


def __real_main(url, save_video=False, auto_metadata=False, auto_title=False, auto_artists=False, auto_date=False) -> None:
    """main
    """
    cprint("Starting Process...", attrs=[Color.GREEN])
    
    playlistID: str = url

    response: dict = youtubeData.playlist_search(playlistID)

    videos: dict = response.get("items")

    youtubeData.download_playlist_videos(videos)
    
    youtubeData.convert_mp3_allFile(save_video)
    
    # Automatically granting data to mp3 file
    if auto_metadata:
        grantAllData()
    if auto_title:
        grantTitle()
    if auto_artists:
        grantArtists()
    if auto_date:
        grantDate()
    
    cprint("Finished!", attrs=[Color.GREEN])


def main():
    fire.Fire(__real_main)