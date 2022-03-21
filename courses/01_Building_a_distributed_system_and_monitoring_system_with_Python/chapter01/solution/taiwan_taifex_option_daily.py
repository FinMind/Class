import datetime
import io
import json
import typing

import pandas as pd
import requests

URL = "https://www.taifex.com.tw/cht/3/dlOptDataDown"


# 網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request
HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "101",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.taifex.com.tw",
    "Origin": "https://www.taifex.com.tw",
    "Referer": "https://www.taifex.com.tw/cht/3/dlOptDailyMarketView",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
}


def crawler(parameters:typing.Dict[str, str]) -> pd.DataFrame:
    crawler_date = parameters.get("crawler_date", "")

    crawler_date = crawler_date.replace("-", "/")
    form_data = {
        "down_type": "1",
        "commodity_id": "all",
        "queryStartDate": crawler_date,
        "queryEndDate": crawler_date,
    }
    resp = requests.post(
        url=URL, headers=HEADER, data=form_data,
    )
    zh_en_mapping = {
        "交易日期": "date",
        "契約": "option_id",
        "到期月份(週別)": "contract_date",
        "履約價": "strike_price",
        "買賣權": "call_put",
        "開盤價": "open",
        "最高價": "max",
        "最低價": "min",
        "收盤價": "close",
        "成交量": "volume",
        "結算價": "settlement_price",
        "未沖銷契約數": "open_interest",
        "最後最佳買價": "",
        "最後最佳賣價": "",
        "歷史最高價": "",
        "歷史最低價": "",
        "是否因訊息面暫停交易": "",
        "交易時段": "",
        "漲跌價":"",
        "漲跌%":"",
    }

    if resp.ok:
        data = pd.read_csv(io.StringIO(resp.text))
        data.columns = [zh_en_mapping[col] for col in data.columns]
        data.columns = list(data.columns[1:]) + [""]
        data["date"] = data.index
        data.index = range(len(data))
        data = data.drop("", axis=1)
        data["date"] = data["date"].str.replace("/", "-")
    else:
        data = pd.DataFrame()
    return data


if __name__ == "__main__":
    parameters = {
        "crawler_date": "2022-01-26",
    }
    data = crawler(parameters)
    print(data)
