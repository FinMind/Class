import datetime
import re
import typing

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from loguru import logger
from tqdm import tqdm


def header():
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "hist.tpex.org.tw",
        "Referer": "http://hist.tpex.org.tw/hist/STOCK/3INSTI/3INSTITRAQRY.HTML",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }


def crawler(date: str) -> typing.Tuple[requests.models.Response, int]:
    if date < "2018-01-15":
        print("不支援 2018-01-15 之前的爬蟲")
    date2 = date.replace("-", "/")
    year = date2.split("/")[0]
    date2 = date2.replace(year, str(int(year) - 1911))
    url = "http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&d={}".format(
        date2
    )
    res = requests.get(url, header())
    columns = [
        "代號",
        "名稱",
        "外資及陸資(不含外資自營商)_買進股數",
        "外資及陸資(不含外資自營商)_賣出股數",
        "外資及陸資(不含外資自營商)_買賣超股數",
        "外資自營商_買進股數",
        "外資自營商_賣出股數",
        "外資自營商_買賣超股數",
        "外資及陸資_買進股數",
        "外資及陸資_賣出股數",
        "外資及陸資_買賣超股數",
        "投信_買進股數",
        "投信_賣出股數",
        "投信_買賣超股數",
        "自營商(自行買賣)_買進股數",
        "自營商(自行買賣)_賣出股數",
        "自營商(自行買賣)_買賣超股數",
        "自營商(避險)_買進股數",
        "自營商(避險)_賣出股數",
        "自營商(避險)_買賣超股數",
        "自營商_買進股數",
        "自營商_賣出股數",
        "自營商_買賣超股數",
        "三大法人買賣超股數合計",
        ""
    ]
    tem = res.json()
    data = pd.DataFrame(tem["aaData"], columns=columns)
    if len(data) == 0:
        return pd.DataFrame()
    return data


if __name__ == "__main__":
    df = crawler(date="2022-05-16")
    print(df)