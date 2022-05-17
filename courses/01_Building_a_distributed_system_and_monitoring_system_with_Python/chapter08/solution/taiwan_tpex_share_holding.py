import datetime
import typing
import requests

import pandas as pd
from loguru import logger


def header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/3insti/qfii/qfii.php?l=zh-tw&fbclid=IwAR3Scg28lvwa04-t4S-Fl-zxLreFr0pd6KehtvoHyRb3JDkmkQNBwWoq1VI",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler(date: str) -> pd.DataFrame:
    date = date.replace("-", "/")
    year = date.split("/")[0]
    date = date.replace(year, str(int(year) - 1911))
    url = "https://www.tpex.org.tw/web/stock/3insti/qfii/qfii_result.php?l=zh-tw&d={}".format(date)
    res = requests.get(
        url=url,
        headers=header(),
    )
    tem = res.json()
    columns = [
        "排行",
        "代號",
        "名稱",
        "發行股數(A)",
        "僑外資及陸資尚可投資股數",
        "僑外資及陸資持有股數",
        "僑外資及陸資尚可投資比率",
        "僑外資及陸資持有比率",
        "法令投資上限比率",
        "備註",
    ]
    data = pd.DataFrame(tem["aaData"], columns=columns)
    if len(data) == 0:
        return pd.DataFrame()
    return data


if __name__ == "__main__":
    df = crawler(date="2022-05-16")
    print(df)