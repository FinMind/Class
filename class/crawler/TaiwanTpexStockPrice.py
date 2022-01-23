import datetime
import json

import pandas as pd
import requests

URL = "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d={}&se=AL&_={}"

# 網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request
HEADER = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Host": "www.tpex.org.tw",
    "Referer": "https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php?l=zh-tw",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def crawler(para):
    crawler_date = para.get("crawler_date", "")
    crawler_timestamp = int(datetime.datetime.now().timestamp())

    resp = requests.get(
        url=URL.format(crawler_date, crawler_timestamp), headers=HEADER
    )
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = pd.DataFrame(resp_data["aaData"])
    else:
        data = pd.DataFrame()
    return data


if __name__ == "__main__":
    para = {
        "crawler_date": "111/01/21",
    }
    data = crawler(para)
    print(data)
