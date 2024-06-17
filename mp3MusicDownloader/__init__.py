# -*- encoding: utf-8 -*-
"""mp3 downloader

概要:
youtube上にあるプレイリストをそのままmp3ファイルに変換しディレクトリにまとめます.
(今時ないけど)mp3しか再生できないシステムの車とかに使えます.

使い方:
適当な名前のディレクトリを作り，そこからこのファイルを実行します.
その際,第一引数にplaylistのURLを指定します.

例:
"七人のカリスマ"の,"カリスマジャンボリー"をダウンロードする場合を考えます.
リンク: https://youtu.be/V8tzcj14CeQ?list=OLAK5uy_nnMRNR5oZmp2RIg8z3vLyGSBDfKHEVuLw
↑この，?list=以下をURLとここでは呼称しています.
ディレクトリ構成が,

app.py
カリスマ/
 └カリスマジャンボリー/

で,いまカリスマジャンボリー/がカレントディレクトリとすると,コンソールで

> python ../../app.py --url "OLAK5uy_nnMRNR5oZmp2RIg8z3vLyGSBDfKHEVuLw"

を実行することで,カリスマジャンボリー/内に.mp3音楽ファイルが生成されます.

オプション:
- --url [url] <必須>
youtube playlistのurlを指定します.
- --save_videos [bool] <任意>
ダウンロードに使用した動画をtmpファイル内に保存します. 
"""
import os
import sys
import shutil
import pathlib
from typing import Final

import tqdm # type: ignore
import fire # type: ignore
import ffmpeg # type: ignore
from term_printer import Color, cprint # type: ignore
from yt_dlp import YoutubeDL, DownloadError # type: ignore
from googleapiclient.discovery import build, Resource # type: ignore

import usbMusicDownloader.env as env

from pprint import pprint


# const value
YOUTUBE_API_SERVICE_NAME: Final[str] = "youtube"
YOUTUBE_API_VERSION: Final[str] = "v3"
YOUTUBE_API_KEY: Final[str] = env.YOUTUBE_API_KEY

YOUTUBE: Final[Resource] = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY)

DIR_PATH: Final[str] = "./"


def playlist_search(youtube: Resource, playlist_id: str) -> dict:
    """urlからプレイリストを検索し,メタデータを取得してくる

    Args:
        youtube (Resource): youtube data api v3のresourceの実体
        playlist_id (str): プレイリストのurl (playlist=[ここの文字列のみを入れる])

    Returns:
        dict: 検索結果
    """
    return youtube.playlistItems().list(
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

    error_videos = []
    
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

        
def __real_main(url, save_video=False) -> None:
    """main
    """
    cprint("Starting Process...", attrs=[Color.GREEN])
    
    playlistID: str = url

    response: dict = playlist_search(YOUTUBE, playlistID)

    videos: dict = response.get("items")

    download_playlist_videos(videos)
    
    convert_mp3_allFile(save_video)
    
    cprint("Finished!", attrs=[Color.GREEN])
        
        
def main():
    fire.Fire(__real_main)