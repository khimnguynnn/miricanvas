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
    try:
        return res["data"]["id"]
    except:
        print(res)

def getElementsID(cookie, memId):
    eleID = []
    name = []
    ses = session(cookie)
    url = f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&activeStatuses=HIDDEN&activeStatuses=INACTIVE&page=0&size=100&sort=createDate%2CDESC&contentSubmissionStatuses=TO_BE_SUBMITTED&memberId={memId}"
    
    res = ses.get(url).json()
    for i in res["data"]["content"]:
        try:
            eleID.append(i["id"])
            nameSplited = i["name"].split("-")
            if len(nameSplited) > 2:
                concatenated_name = ' '.join(nameSplited[1:])
                name.append(concatenated_name.replace(".svg", ""))
            else:
                name.append(i["name"].split("-")[1].split(".")[0])
        except:
            name.append(i["name"])
    return eleID, name

def submitItem(cookie, eleId, name, hashtag):
    try:
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
        else:
            return False
    except:

        return False


def checkBalance(cookie, memberid):
    ses = session(cookie)
    resp = ses.get(f"https://api-designhub.miricanvas.com/api/v1/accounting/achievement-summary?aggregateUnit=MONTHLY&endDate=1689866799999&page=0&size=50&startDate=1672498800000&licenseKeys={memberid}")
    if resp.status_code != 200:
        return 0
    try:
        return int(resp.json()["data"]["content"][0]["totalProfit"]["KRW"])
    except:
        return 0
    
def PendingElements(cookie, memberid):
    ses = session(cookie)
    resp = ses.get(f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&contentReviewItemStatuses=WAITING&contentReviewItemStatuses=RETRY&contentSubmissionStatuses=DONE&memberId={memberid}&size=1")
    if resp.status_code != 200:
        return None
    return resp.json()["data"]["pagination"]["totalCount"]

def ApprovedElements(cookie, memid):
    ses = session(cookie)
    resp = ses.get(f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&activeStatuses=HIDDEN&activeStatuses=INACTIVE&page=0&size=50&sort=contentReviewItem.approveDate%2CDESC&contentReviewItemStatuses=APPROVAL&contentSubmissionStatuses=DONE&endDate=1689866799999&licenseKey={memid}&startDate=1681578000000")
    if resp.status_code != 200:
        return None
    return resp.json()["data"]["pagination"]["totalCount"]