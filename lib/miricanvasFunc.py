from requests import Session
import json

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