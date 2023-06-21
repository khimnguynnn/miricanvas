from datetime import datetime
from pathlib import Path
import os
import random
from pathlib import Path
import glob
from requests import Session
import redis

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

    folder_path = Path(ImagesPath().replace("lib\\", "") + "\\" + folder)
    for item in folder_path.iterdir():
        if item.name.__contains__(".svg"):
            svgFile.append(item.name)

        else:
            pass
    return svgFile

def hashtagList(name):
    hashtag, source = getHashtag(name)
    return hashtag, source


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

def count_keywords(lst):
    keyword_count = {}
    for keyword in lst:
        if keyword in keyword_count:
            keyword_count[keyword] += 1
        else:
            keyword_count[keyword] = 1
    return keyword_count

def getHashtag(input_keyword):
    r = redis.Redis(host='localhost', port=6379, db=0)
    input_keyword = input_keyword.lower()
    ses = Session()

    ses.headers.update({
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    })

    keyword_list = []
    _From = ""
    string_keywords = ""

    if r.exists(input_keyword):
        _From = "Redis"
        value = (r.get(input_keyword)).decode()
        for tag in value.split(","):
            keyword_list.append(tag)
            
        r.close()
        
    else:
        url = "https://api.imstocker.com/api/search/searchWorks"
        data = {"query":{"text":input_keyword,"licenseType":None,"type":3,"hasModels":False,"microstock":None,"author":None,"exclude":None,"id_language":"1"},"options":{"offset":0,"count":30},"keyworder_session":None,"target":"site","id_language":"1","access_token":"4095:PmbMXqrVOzfugL9gb8ERF7w1lSekLqTKLBcG5QWFoKrBvkI6nxJpEER39HxLMxhxcb0smbbFTCg85m3483Sf0Axx"}
        
        resp = ses.post(url, json=data).json()
        for i in (resp["res"]["list"]):
            for j in (i["keywords"]):
                keyword = j["title_keyword"]
                keyword_list.append(keyword)

        result = count_keywords(keyword_list)
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        
        counts = 0
        keyword_list.clear()
        for keyword, _ in sorted_result:
            if counts == 24:
                break
            
            keyword_list.append(keyword)
            counts += 1

        string_keywords = ",".join(i for i in keyword_list)

        r.set(input_keyword, string_keywords)
        _From = "Keyworder"
        r.close()
    keyword_list.insert(0, input_keyword)

    keyword_list = list(dict.fromkeys(keyword_list))

    return keyword_list, _From