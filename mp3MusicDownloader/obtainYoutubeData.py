# -*- coding: utf-8 -*-
"""mp3 downloader
"""
import os
import shutil
import pathlib
from typing import Final

import tqdm # type: ignore
import ffmpeg # type: ignore
from yt_dlp import YoutubeDL, DownloadError # type: ignore
from googleapiclient.discovery import build, Resource # type: ignore

import mp3MusicDownloader.env as env


# const value
YOUTUBE_API_SERVICE_NAME: Final[str] = "youtube"
YOUTUBE_API_VERSION: Final[str] = "v3"
YOUTUBE_API_KEY: Final[str] = env.YOUTUBE_API_KEY

YOUTUBE: Final[Resource] = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY)

DIR_PATH: Final[str] = "./"


def playlist_search(playlist_id: str) -> dict:
    """urlからプレイリストを検索し,メタデータを取得してくる

    Args:
        youtube (Resource): youtube data api v3のresourceの実体
        playlist_id (str): プレイリストのurl (playlist=[ここの文字列のみを入れる])

    Returns:
        dict: 検索結果
    """
    return YOUTUBE.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            maxResults=50
        ).execute()
    

def download_playlist_videos(videos: dict) -> None:
    """playlistItems()で取得したデータのitems要素から,各動画をダウンロードする

    Args:
        videos (dict): playlistItems()で取得したデータのitems要素
    """
    ydl_opts = {
        'format':'bestaudio',
        'noprogress': True,
        'quiet': True
    }

    for i in tqdm.tqdm(range(len(videos)), desc="[Videos Downloading]"):
        url = videos[i].get("snippet").get("resourceId").get("videoId")
        ydl_opts["outtmpl"] = f'{str(i+1).zfill(2)}. %(title)s.%(ext)s'
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f"https://youtube.com/watch?v={url}"])
            except DownloadError:
                pass # 著作権の関係でダウンロードできない動画があったりしたら,ここを修正してそれが明示されるようにしなきゃいけないかも


def convert_mp3_allFile(save_video: bool) -> None:
    """カレントディレクトリにあるファイルを全てmp3に変換し,元ファイルをtmpディレクトリに送る
    
    Args:
        save_video (bool): mp3保存用に一旦ダウンロードした動画をtmpファイルに残したままにするか
    """
    files = os.listdir(DIR_PATH)
    current_dir:str = os.getcwd()

    tmp_dir:str = "../" + current_dir.split("/")[-1] + "_tmp"
    os.mkdir(tmp_dir)

    for file in tqdm.tqdm(files, desc="[Files Converting]"):
        file_name: str = pathlib.PurePath(file).stem + ".mp3"

        stream = ffmpeg.input(file) 
        stream = ffmpeg.output(stream, file_name) 
        ffmpeg.run(stream, quiet=True)
        
        shutil.move(file, tmp_dir)
    
    if not save_video:
        shutil.rmtree(tmp_dir)        