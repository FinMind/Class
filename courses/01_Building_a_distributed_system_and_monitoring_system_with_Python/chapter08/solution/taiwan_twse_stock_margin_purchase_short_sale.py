import datetime
import typing

import pandas as pd
from loguru import logger


def header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "http://www.twse.com.tw/zh/page/trading/exchange/MI_MARGN.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler(date: str) -> pd.DataFrame:
    url = "http://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date={}&selectType=ALL".format(
        date.replace("-", "")
    )
    res = requests.get(url, header())
    try:
        data = res.json()["data"]
    except Exception as e:
        logger.error(e)
        return pd.DataFrame()

    if len(data) == 0:
        return pd.DataFrame()

    colname = [
        "股票代號",
        "股票名稱",
        "融資_買進",
        "融資_賣出",
        "融資_現金償還",
        "融資_前日餘額",
        "融資_今日餘額",
        "融資_限額",
        "融資_買進",
        "融資_賣出",
        "融劵_現金償還",
        "融劵_前日餘額",
        "融劵_今日餘額",
        "融劵_限額",
        "資劵相抵",
        "註記",
    ]
    data = pd.DataFrame(data)
    data.columns = colname
    return data

if __name__ == "__main__":
    df = crawler(date="2022-05-16")
    print(df)