import typing

import pandas as pd
import requests
from loguru import logger


def header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "http://www.twse.com.tw/zh/page/trading/fund/T86.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler(date: str) -> pd.DataFrame:
    date2 = date.replace("-", "")
    url = "http://www.twse.com.tw/fund/T86?response=json&date={}&selectType=ALLBUT0999".format(
        date2
    )
    res = requests.get(url, header())
    res.encoding = "utf-8"
    tem = res.json()
    if tem["stat"] in ["查詢日期小於101年05月02日，請重新查詢!", "很抱歉，沒有符合條件的資料!"]:
        return pd.DataFrame()
    elif tem["stat"] == "很抱歉，目前線上人數過多，請您稍候再試":
        print("很抱歉，目前線上人數過多，請您稍候再試")
        raise
    fields = tem["fields"]
    data = pd.DataFrame(tem["data"], columns=fields)
    return data


if __name__ == "__main__":
    date = "2022-04-12"
    df = crawler(date)
    print(df)