from datetime import datetime
from pathlib import Path
import os
import random

current_path = os.path.dirname(os.path.abspath(__file__))

def ImagesPath():
    return current_path + "/Images"

def timeInfor():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def getImageFolders():
    FolderName = []
    p = Path(ImagesPath().replace("lib/", ""))
    subdirectories = [x for x in p.iterdir() if x.is_dir()]
    for directory in subdirectories:
        FolderName.append(directory.name)
    return FolderName

def getItemsInFolder(folder):
    svgFile = []
    hashtag = None
    folder_path = Path(f'{ImagesPath().replace("lib/", "")}/{folder}')
    for item in folder_path.iterdir():
        if item.name.__contains__(".svg"):
            svgFile.append(item.name)
        
        elif item.name.__contains__(".txt"):
            hashtag = item.name
        else:
            pass
    return svgFile, hashtag

def hashtagList(name, filename):
    with open(filename, "r") as f:
        words = f.read().split(",")

    hashtag = random.sample(words, k=24)
    hashtag.insert(0, name)

    return hashtag
