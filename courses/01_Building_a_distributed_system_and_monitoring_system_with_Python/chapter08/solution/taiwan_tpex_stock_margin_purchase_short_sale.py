import datetime
import typing

import pandas as pd
import requests
from loguru import logger


def header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler(date: str) -> pd.DataFrame:
    if date < "2007-01-01":
        return pd.DataFrame()
    try:
        y = str(int(date.split("-")[0]) - 1911)
        url = (
        "https://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=json&d={}".format(
                date.replace(date.split("-")[0], y).replace("-", "/")
            )
        )
        res = requests.get(url=url, headers=header())
        tem = res.json()
        colname = [
            "代號",
            "名稱",
            "融資_前資餘額(張)",
            "融資_資買",
            "融資_資賣",
            "融資_現償",
            "融資_資餘額",
            "融資_資屬證金",
            "融資_資使用率(%)",
            "融資_資限額",
            "融劵_前資餘額(張)",
            "融劵_資買",
            "融劵_資賣",
            "融劵_現償",
            "融劵_資餘額",
            "融劵_資屬證金",
            "融劵_資使用率(%)",
            "融劵_資限額",
            "資劵相抵(張)",
            "備註",
        ]
        data = pd.DataFrame(tem["aaData"], columns=colname)
    except Exception as e:
        logger.error(e)
        return pd.DataFrame()

    if len(data) == 0:
        return pd.DataFrame()
    return data


if __name__ == "__main__":
    df = crawler(date="2022-05-17")
    print(df)