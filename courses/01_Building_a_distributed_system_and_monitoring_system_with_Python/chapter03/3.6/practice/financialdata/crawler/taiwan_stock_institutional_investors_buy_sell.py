import datetime
import json
import time
import typing

import requests

import pandas as pd
from loguru import logger
from pydantic import BaseModel


class Schema(BaseModel):
    stock_id: str
    stock_name: str
    Mainland_Area_exclude_Foreign_Dealer_Buy: int = 0
    Mainland_Area_exclude_Foreign_Dealer_Sell: int = 0
    Mainland_Area_exclude_Foreign_Dealer_Net: int = 0
    Foreign_Dealer_Buy: int = 0
    Foreign_Dealer_Sell: int = 0
    Foreign_Dealer_Net: int = 0
    Foreign_Dealer_Self_Buy: int = 0
    Foreign_Dealer_Self_Sell: int = 0
    Foreign_Dealer_Self_Net: int = 0
    Foreign_Investors_include_Mainland_Area_Buy: int = 0
    Foreign_Investors_include_Mainland_Area_Sell: int = 0
    Foreign_Investors_include_Mainland_Area_Net: int = 0
    Investment_Trust_Buy: int = 0
    Investment_Trust_Sell: int = 0
    Investment_Trust_Net: int = 0
    Dealer_Proprietary_Buy: int = 0
    Dealer_Proprietary_Sell: int = 0
    Dealer_Proprietary_Net: int = 0
    Dealer_Hedging_Buy: int = 0
    Dealer_Hedging_Sell: int = 0
    Dealer_Hedging_Net: int = 0
    Dealer_Buy: int = 0
    Dealer_Sell: int = 0
    Dealer_self_Buy: int = 0
    Dealer_self_Sell: int = 0
    Dealer_self_Net: int = 0
    Dealer_Net: int = 0
    Total_Net: int = 0
    date: str


def is_weekend(date: datetime.date) -> bool:
    return date.weekday() in [6]


def gen_task_paramter_list(start_date: str, end_date: str) -> typing.List[str]:
    """data_source 主要用於 queue, 不排除掉周六, 因為過去(2007以前)週六會交易"""
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    days = (end_date - start_date).days + 1
    date_list = [
        start_date + datetime.timedelta(days=day) for day in range(days)
    ]
    date_list = [
        dict(
            crawler_date=str(d),
            data_source=data_source,
        )
        for d in date_list
        for data_source in [
            "twse",
            "tpex",
        ]
        if not is_weekend(d)
    ]
    return date_list


def tpex_header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge.php?l=zh-tw",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def twse_header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": 'https://www.twse.com.tw/zh/page/trading/fund/T86.htmlsec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler_twse(date: str) -> pd.DataFrame:
    crawler_date = date.replace("-", "")
    crawler_timestamp = int(datetime.datetime.now().timestamp())
    time.sleep(5)
    url = (
        "https://www.twse.com.tw/fund/T86?"
        f"response=json&date={crawler_date}&selectType=ALL&_={crawler_timestamp}"
    )
    resp = requests.get(url=url, headers=twse_header())
    columns = [
        "stock_id",
        "stock_name",
        "Foreign_Investors_include_Mainland_Area_Buy",
        "Foreign_Investors_include_Mainland_Area_Sell",
        "Foreign_Investors_include_Mainland_Area_Net",
        "Foreign_Dealer_Self_Buy",
        "Foreign_Dealer_Self_Sell",
        "Foreign_Dealer_Self_Net",
        "Investment_Trust_Buy",
        "Investment_Trust_Sell",
        "Investment_Trust_Net",
        "Dealer_Net",
        "Dealer_self_Buy",
        "Dealer_self_Sell",
        "Dealer_self_Net",
        "Dealer_Hedging_Buy",
        "Dealer_Hedging_Sell",
        "Dealer_Hedging_Net",
        "Total_Net",
    ]
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = resp_data.get("data", "")
        data = pd.DataFrame(data, columns=columns)
        data["date"] = date
    else:
        data = pd.DataFrame(columns=columns)
    return data


def crawler_tpex(date: str) -> pd.DataFrame:
    crawler_date = date.replace(
        date.split("-")[0], str(int(date.split("-")[0]) - 1911)
    )
    crawler_date = crawler_date.replace("-", "/")
    crawler_timestamp = int(datetime.datetime.now().timestamp())
    time.sleep(5)
    url = (
        "https://www.tpex.org.tw/web/stock/3insti/daily_trade/"
        "3itrade_hedge_result.php?l=zh-tw&se=AL&t=D"
        f"&d={crawler_date}&_={crawler_timestamp}"
    )
    resp = requests.get(
        url=url,
        headers=tpex_header(),
    )
    columns = [
        "stock_id",
        "stock_name",
        "Mainland_Area_exclude_Foreign_Dealer_Buy",
        "Mainland_Area_exclude_Foreign_Dealer_Sell",
        "Mainland_Area_exclude_Foreign_Dealer_Net",
        "Foreign_Dealer_Buy",
        "Foreign_Dealer_Sell",
        "Foreign_Dealer_Net",
        "Foreign_Investors_include_Mainland_Area_Buy",
        "Foreign_Investors_include_Mainland_Area_Sell",
        "Foreign_Investors_include_Mainland_Area_Net",
        "Investment_Trust_Buy",
        "Investment_Trust_Sell",
        "Investment_Trust_Net",
        "Dealer_Proprietary_Buy",
        "Dealer_Proprietary_Sell",
        "Dealer_Proprietary_Net",
        "Dealer_Hedging_Buy",
        "Dealer_Hedging_Sell",
        "Dealer_Hedging_Net",
        "Dealer_Buy",
        "Dealer_Sell",
        "Dealer_Net",
        "Total_Net",
    ]
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = resp_data.get("aaData", "")
        data = pd.DataFrame(data)
        data = data.drop([24], axis=1)
        data.columns = columns
        data["date"] = date
    else:
        data = pd.DataFrame()
    return data


def check_schema(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("check_schema")
    df_dict = df.to_dict("r")
    df_schema = [Schema(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df


def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("clear_data")
    for column in [
        "Mainland_Area_exclude_Foreign_Dealer_Buy",
        "Mainland_Area_exclude_Foreign_Dealer_Sell",
        "Mainland_Area_exclude_Foreign_Dealer_Net",
        "Foreign_Dealer_Buy",
        "Foreign_Dealer_Sell",
        "Foreign_Dealer_Net",
        "Foreign_Dealer_Self_Buy",
        "Foreign_Dealer_Self_Sell",
        "Foreign_Dealer_Self_Net",
        "Foreign_Investors_include_Mainland_Area_Buy",
        "Foreign_Investors_include_Mainland_Area_Sell",
        "Foreign_Investors_include_Mainland_Area_Net",
        "Investment_Trust_Buy",
        "Investment_Trust_Sell",
        "Investment_Trust_Net",
        "Dealer_Proprietary_Buy",
        "Dealer_Proprietary_Sell",
        "Dealer_Proprietary_Net",
        "Dealer_Hedging_Buy",
        "Dealer_Hedging_Sell",
        "Dealer_Hedging_Net",
        "Dealer_Buy",
        "Dealer_Sell",
        "Dealer_self_Buy",
        "Dealer_self_Sell",
        "Dealer_self_Net",
        "Dealer_Net",
        "Total_Net",
    ]:
        if column in df:
            df[column] = df[column].astype(str).str.replace(",", "").astype(int)
    df["stock_name"] = df["stock_name"].str.replace(" ", "")
    return df


def crawler(
    parameters: typing.Dict[
        str,
        typing.List[typing.Union[str, int, float]],
    ]
) -> pd.DataFrame:
    logger.info(parameters)
    date = parameters.get("crawler_date", "")
    data_source = parameters.get("data_source", "")
    if data_source == "twse":
        df = crawler_twse(date=date)
    elif data_source == "tpex":
        df = crawler_tpex(date=date)
    df = clear_data(df)
    df = check_schema(df)
    return df
