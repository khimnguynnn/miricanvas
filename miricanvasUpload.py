from pathlib import Path
import os, random, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from requests import Session
from datetime import datetime


current_path = os.path.dirname(os.path.abspath(__file__))

emailLogin = "khimnguynn@gmail.com"
password = "0708Khiem!"

def timeInfor():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def getImageFolders():
    FolderName = []
    p = Path(current_path)
    subdirectories = [x for x in p.iterdir() if x.is_dir() and x.name != "env"]
    for directory in subdirectories:
        FolderName.append(directory.name)
    return FolderName

def getItemsInFolder(folder):
    svgFile = []
    hashtag = None
    folder_path = Path(f'{current_path}/{folder}')
    for item in folder_path.iterdir():
        if item.name.__contains__(".svg"):
            svgFile.append(item.name)
        
        elif item.name.__contains__(".txt"):
            hashtag = item.name
        else:
            pass
    return svgFile, hashtag

def openChrome():
    options = webdriver.ChromeOptions()
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://designhub.miricanvas.com/login")

    email = driver.find_element(By.XPATH, "//input[@placeholder='Email']")

    for i in emailLogin:
        email.send_keys(i)
        sleep(random.uniform(0.1, 0.3))
    sleep(1)
    passw = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    for i in password:
        passw.send_keys(i)
        sleep(random.uniform(0.1, 0.3))
    sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Log In']").click()

    return driver

def getCookies(driver):
    cookie_string = ""
    for cookie in driver.get_cookies():
        name = cookie['name']
        value = cookie['value']
        cookie_string  += f"{name}={value}; "

    cookie_string = cookie_string[:-2]
    return cookie_string

def session(cookie):
    ses = Session()
    ses.headers.update({
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8,zh-TW;q=0.7,zh;q=0.6",
    "content-type": "application/json",
    "cookie": cookie,
    "origin": "https://designhub.miricanvas.com",
    "referer": "https://designhub.miricanvas.com/",
    "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    })
    return ses

def getMemId(cookie):
    url = "https://api-designhub.miricanvas.com/api/v1/members/get-current-member"
    ses = session(cookie)
    res = ses.get(url).json()
    return res["data"]["id"]

def getElementsID(cookie, memId):
    eleID = []
    name = []
    ses = session(cookie)
    url = f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&activeStatuses=HIDDEN&activeStatuses=INACTIVE&page=0&size=100&sort=createDate%2CDESC&contentSubmissionStatuses=TO_BE_SUBMITTED&memberId={memId}"
    
    res = ses.get(url).json()
    for i in res["data"]["content"]:

        eleID.append(i["id"])
        name.append(i["name"].split("-")[0])
    return eleID, name

def submitItem(cookie, eleId, name, hashtag):
    ses = session(cookie)
    url = f"https://api-designhub.miricanvas.com/api/v1/element-items/{eleId}"
    data1 = {"contentTier":"PREMIUM","name":name,"keywords": hashtag}
    resp = ses.patch(url, data=json.dumps(data1))
    if resp.status_code == 200:

        data2 = {"contentSubmissionStatus":"DONE"}
        url = f"https://api-designhub.miricanvas.com/api/v1/element-items/{eleId}/change-content-submission-status"
        resp = ses.patch(url, data=json.dumps(data2))
        if resp.status_code == 200:
            return True
    
    return False

def hashtagList(name, filename):
    with open(filename, "r") as f:
        words = f.read().split(",")

    hashtag = random.sample(words, k=24)
    hashtag.insert(0, name)

    return hashtag

if __name__ == "__main__":
    print(f"{timeInfor()} --> Starting Program")
    driver = openChrome()
    folders = getImageFolders()
    
    for folder in folders: 

        sleep(2)
        cookie = getCookies(driver)
        memId = getMemId(cookie)
        
        svg, hashtag = getItemsInFolder(folder)
        if hashtag == None:
            print(f"{timeInfor()} --> {folder} have not hashtag -> skip")
            continue
        else:
            driver.get("https://designhub.miricanvas.com/element/upload")
            sleep(1)
            

            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Select File or Folder']")))
            sleep(2)
            
            path = ""
            path_new = current_path.replace("\\", "/")
            for item in svg:

                path += fr"{path_new}/{folder}/{item}" + ' \n '

            path = path.strip()
            print(f"{timeInfor()} --> Started Upload Pack {folder}")
            driver.find_element(By.XPATH, "//input[@type='file']").send_keys(path)
            
            WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']")))
            print(f"{timeInfor()} --> Upload Elements Done")
            sleep(2)
            eleid, name = getElementsID(cookie, memId)
            print(f"{timeInfor()} --> Started Submit Elements for Approbation")
            for i, ele in enumerate(eleid):

                arrHashtag = hashtagList(name[i].lower(), f"{current_path}\\{folder}\\{hashtag}")

                if submitItem(cookie, ele, name[i], arrHashtag):

                    print(f"{timeInfor()} --> success upload element -> {name[i]}.svg")
                else:
                    print(f"{timeInfor()} --> failed upload element -> {name[i]}.svg")