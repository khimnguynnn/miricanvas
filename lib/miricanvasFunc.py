from requests import Session
import json
from time import sleep

class miricanvasFeature:
    def __init__(self, cookie, proxy=None):
        self.MEMID = "https://api-designhub.miricanvas.com/api/v1/members/get-current-member"
        # session
        self.ses = self.session(cookie)
        proxy = proxy.split(":")
        if proxy is not None:
            self.ses.proxies = {
                'http': f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
                'https': f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
            }
        # function need run first
        self.memid = self.memberID()
        #CONST URL
        self.ELEMENTID = f"https://api-designhub.miricanvas.com/api/v2/element-items/get-element-integration-items?activeStatuses=ACTIVE&activeStatuses=HIDDEN&activeStatuses=INACTIVE&page=0&size=50&sort=createDate%2CDESC&contentSubmissionStatuses=TO_BE_SUBMITTED&memberId={self.memid}"
        self.BALANCE_URL = f"https://api-designhub.miricanvas.com/api/v1/accounting/achievement-summary?aggregateUnit=YEARLY&endDate=1704036399999&page=0&size=50&startDate=1672498800000&licenseKeys={self.memid}"
        # self.RATE_URL = "https://openexchangerates.org/api/latest.json?app_id=91c457aae2834f16b872d16a2201e088"
        self.RATE_URL = "https://www.currency.me.uk/charts-fetch.php?c1=USD&c2=KRW&t=1"
        self.PENDING_URL = f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&contentReviewItemStatuses=WAITING&contentReviewItemStatuses=RETRY&contentSubmissionStatuses=DONE&memberId={self.memid}&size=1"
        self.ARPPROVED_URL = f"https://api-designhub.miricanvas.com/api/v1/element-items/get-element-integration-items?activeStatuses=WAITING&activeStatuses=ACTIVE&activeStatuses=HIDDEN&activeStatuses=INACTIVE&page=0&size=50&sort=contentReviewItem.approveDate%2CDESC&contentReviewItemStatuses=APPROVAL&contentSubmissionStatuses=DONE&endDate=1704036399999&licenseKey={self.memid}&startDate=1681578000000"

        
    def session(self, cookie):
        ses = Session()
        ses.headers.update({
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "content-type": "application/json",
        "Connection": "keep-alive",
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


    def memberID(self):
        try:
            resp = self.ses.get(self.MEMID)
            return resp.json()["data"]["id"] if resp.status_code == 200 else None
        except:
            return None


    def getElementsID(self):
        eleID = []
        name = []
        
        res = self.ses.get(self.ELEMENTID).json()
        for i in res["data"]:
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


    def submitItem(self, eleId, name, hashtag):
        url = f"https://api-designhub.miricanvas.com/api/v1/element-items/{eleId}"
        data1 = {"contentTier":"PREMIUM","name":name,"keywords": hashtag}
        try:
            resp = self.ses.patch(url, data=json.dumps(data1))
        except:
            return False
        
        if resp.status_code == 200:
            for _ in range(3):
                try:
                    data2 = {"contentSubmissionStatus":"DONE"}
                    url = f"https://api-designhub.miricanvas.com/api/v1/element-items/{eleId}/change-content-submission-status"
                    resp = self.ses.patch(url, data=json.dumps(data2))
                    return True if  resp.status_code == 200 else False
                except:
                    sleep(1)
                    continue
        return False

    def getKRWRate(self):
        resp = self.ses.get(self.RATE_URL)
        return round(resp.json()[0]["y"], 2) if resp.status_code == 200 else 1300

    def checkBalance(self):
        resp = self.ses.get(self.BALANCE_URL)

        try:
            balance = float(resp.json()["data"]["content"][0]["totalProfit"]["KRW"]) if resp.status_code == 200 else 0
        except:
            return 0
        
        try:
            balance_usd = float(resp.json()["data"]["content"][0]["totalProfit"]["USD"]) if resp.status_code == 200 else 0
        except:
            balance_usd = 0

        return round(balance / self.getKRWRate() + balance_usd, 2)


    def PendingElements(self):
        try:
            resp = self.ses.get(self.PENDING_URL)
            return resp.json()["data"]["pagination"]["totalCount"] if resp.status_code == 200 else None
        except:
            return None


    def ApprovedElements(self):
        try:
            resp = self.ses.get(self.ARPPROVED_URL)
            return resp.json()["data"]["pagination"]["totalCount"] if resp.status_code == 200 else None
        except:    
            return None
        
    

    def DeleteErrorElement(self, eleid):
        deleteData = {"activeStatus":"DELETED"}
        try:
            resp = self.ses.patch(f"https://api-designhub.miricanvas.com/api/v1/element-items/{eleid}", data=json.dumps(deleteData))
            return resp.status_code == 200
        except:
            return False
