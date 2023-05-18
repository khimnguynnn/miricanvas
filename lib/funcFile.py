from datetime import datetime
from pathlib import Path
import os
import random
from pathlib import Path

current_path = os.path.dirname(os.path.abspath(__file__))

def ImagesPath():
    return current_path + "\\Images"

def timeInfor():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def getImageFolders():
    FolderName = []
    p = Path(ImagesPath().replace("lib\\", ""))
    subdirectories = [x for x in p.iterdir() if x.is_dir()]
    for directory in subdirectories:
        FolderName.append(directory.name)
    return FolderName

def getItemsInFolder(folder):
    svgFile = []
    hashtag = None
    folder_path = Path(ImagesPath().replace("lib\\", "") + "\\" + folder)
    for item in folder_path.iterdir():
        if item.name.__contains__(".svg"):
            svgFile.append(item.name)
        
        elif item.name.__contains__(".txt"):
            hashtag = item.name
        else:
            pass
    return svgFile, hashtag

def hashtagList(name, folder, filename):
    name = name.lower()
    p = Path(ImagesPath().replace("lib\\", "") + f"\\{folder}\\{filename}")
    with open(p, "r") as f:
        words = f.read().split(",")

    hashtag = random.sample(words, k=24)
    hashtag.insert(0, name)

    return hashtag


def plusImages(folder, images):
    p = current_path.replace("\\", "/").replace("lib", "Images")

    path = ''
    for item in images:
        path += fr"{p}/{folder}/{item}" + ' \n '
    return path.strip()

def MoveImage(folder, file):
    file_path = Path(f"./Images/{folder}/{file}")
    file_path.unlink()

