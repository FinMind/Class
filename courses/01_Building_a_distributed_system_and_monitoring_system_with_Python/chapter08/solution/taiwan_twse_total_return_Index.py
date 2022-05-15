import typing
import requests

import pandas as pd
from loguru import logger


def crawler(date: str) -> pd.DataFrame:
    url = "https://www.twse.com.tw/indicesReport/MFI94U?response=json&date={}".format(date.replace("-", ""))
    response = requests.get(url)
    if response.json()["stat"] in ["很抱歉，沒有符合條件的資料!", "查詢日期小於94年9月2日，請重新查詢!"]:
        return pd.DataFrame()

    colname = [col.replace("\u3000", "") for col in response.json()["fields"]]
    df = response.json()["data"]
    df = pd.DataFrame(list(df), columns=colname)
    return df



if __name__ == "__main__":
    date = "2022-04-12"
    df = crawler(date)
    print(df)