# -*- coding: utf-8 -*-
import os

from mutagen.easyid3 import EasyID3


def grantTitle(file: str, title: str) -> None:
    tags = EasyID3(file)
    tags["title"] = title
    tags.save()
    
    if not title == "":
        os.rename(file, file[:4] + title + file[-4:])


def grantartists(file: str, artists: list[str]) -> None:
    tags = EasyID3(file)
    tags["artist"] = ", ".join(artists)
    tags.save()


def grantDate(file: str, date: str) -> None:
    tags = EasyID3(file)
    tags["date"] = date
    tags.save()