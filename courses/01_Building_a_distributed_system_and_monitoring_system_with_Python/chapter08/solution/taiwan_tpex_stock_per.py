import requests

import pandas as pd


def crawler(date: str = "2019-01-01") -> pd.DataFrame:
    year = str(int(date.split("-")[0]) - 1911)
    date2 = "/".join([year] + date.split("-")[1:])
    url = "https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&d={}".format(date2)
    response = requests.get(url)
    if response.json()["aaData"] == []:
        return pd.DataFrame()

    data = response.json()["aaData"]
    data = pd.DataFrame(
        data,
        columns=[
            "stock_id",
            "stock_name",
            "PER",
            "dividend_per_share",
            "year",
            "dividend_yield",
            "PBR",
        ]
    )

    data["date"] = date
    return data

if __name__ == "__main__":
    date = "2022-05-03"
    data = crawler(date)
    print(data)