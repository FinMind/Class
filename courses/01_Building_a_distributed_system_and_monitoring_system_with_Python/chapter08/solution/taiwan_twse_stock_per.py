import typing
import requests

import pandas as pd


def crawler(date: str) -> pd.DataFrame:
    URL = "https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date={0}&selectType=ALL".format(date.replace("-", ""))
    response = requests.get(URL, verify=False)
    if response.json()["stat"] in ["很抱歉，沒有符合條件的資料!", "查詢日期小於94年9月2日，請重新查詢!"]:
        return pd.DataFrame()

    data = response.json()["data"]
    data = pd.DataFrame(list(data), columns=response.json()["fields"])
    data["date"] = date
    return data


if __name__ == "__main__":
    date = "2022-05-03"
    data = crawler(date)
    print(data)