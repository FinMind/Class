import typing

import pandas as pd
from loguru import logger


def header() -> typing.Dict[str, str]:
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "http://www.twse.com.tw/zh/page/trading/fund/MI_QFIIS.html",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler(date: str) -> pd.DataFrame():
    url = "http://www.twse.com.tw/fund/MI_QFIIS?response=json&date={}&selectType=ALLBUT0999".format(date.replace("-", ""))
    res = requests.get(url, header())
    res.encoding = "utf-8"
    tem = res.json()
    if tem["stat"] != "OK":
        logger.info(res.text)
        return pd.DataFrame()
    data = pd.DataFrame(tem["data"], columns=tem["fields"])
    if len(data) == 0:
        logger.info(res.text)
        return pd.DataFrame()
    return data


if __name__ == "__main__":
    df = crawler(date="2022-04-12")
    print(df)