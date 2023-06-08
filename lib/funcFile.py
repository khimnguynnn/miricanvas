from datetime import datetime
from pathlib import Path
import os
import random
from pathlib import Path
import glob
from requests import Session

ses = Session()
ses.headers.update({
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
})

def requestWord(word):
    if " " in  word:
        return word
    if len(word) < 6:
        return word
    data = {
        "action": "checkers_api",
        "content": word
    }

    resp = ses.post("https://writer.com/wp-admin/admin-ajax.php", data=data)

    try:
        if resp.status_code == 200:
            result = resp.json()["data"]["issues"][0]["suggestions"][0].lower()
            if result.replace(" ", "") == word:
                return result
            else:
                return word

    except:

        return word

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
    name = requestWord(name)

    hashtag = random.sample(words, k=20)
    hashtag.insert(0, name)
    hashtag = list(dict.fromkeys(hashtag))

    return hashtag


def plusImages(folder, images):
    p = current_path.replace("\\", "/").replace("lib", "Images")

    path = ''
    for item in images:
        path += fr"{p}/{folder}/{item}" + ' \n '
    return path.strip()

def DelImage(folder, file):
    file_path = Path(f"./Images/{folder}/{file}")
    file_path.unlink()

def RemoveEmptyFolder(folder):
    file_paths = glob.glob(f"./Images/{folder}/*")
    for file_path in file_paths:
        os.unlink(file_path)

    file_path = Path(f"./Images/{folder}/")
    file_path.rmdir()


def isHaveElements(folder, filename):
    file_path = Path(f"./Images/{folder}/{filename}")

    return True if len(open(file_path).read()) > 5 else False

    