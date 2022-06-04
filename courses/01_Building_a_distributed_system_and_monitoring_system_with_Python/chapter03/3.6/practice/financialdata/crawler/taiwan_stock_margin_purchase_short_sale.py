import datetime
import json
import time
import typing

import requests

import pandas as pd
from loguru import logger


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
        "Host": "www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }


def crawler_tpex(date: str) -> pd.DataFrame:
    crawler_date = date.replace(
        date.split("-")[0], str(int(date.split("-")[0]) - 1911)
    )
    crawler_date = crawler_date.replace("-", "/")
    crawler_timestamp = int(datetime.datetime.now().timestamp())
    time.sleep(5)
    url = f"https://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=json&d={crawler_date}&_={crawler_timestamp}"
    resp = requests.get(url=url, headers=tpex_header())
    colname = [
        "stock_id",
        "stock_name",
        "MarginPurchaseYesterdayBalance",
        "MarginPurchaseBuy",
        "MarginPurchaseSell",
        "MarginPurchaseCashRepayment",
        "MarginPurchaseTodayBalance",
        "MarginPurchaseLimit",
        "ShortSaleYesterdayBalance",
        "ShortSaleBuy",
        "ShortSaleSell",
        "ShortSaleCashRepayment",
        "ShortSaleTodayBalance",
        "ShortSaleLimit",
        "OffsetLoanAndShort",
        "Note",
    ]
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = resp_data.get("aaData", "")
        data = pd.DataFrame(data)
        data = data.drop([7, 8, 15, 16], axis=1)
        data.columns = colname
        data["date"] = date
    else:
        data = pd.DataFrame()
    return data


# 網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request
def twse_header():
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_MARGN.html",
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
    url = f"https://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date={crawler_date}&selectType=ALL&_={crawler_timestamp}"
    resp = requests.get(url=url, headers=twse_header())
    columns = [
        "stock_id",
        "stock_name",
        "MarginPurchaseBuy",
        "MarginPurchaseSell",
        "MarginPurchaseCashRepayment",
        "MarginPurchaseYesterdayBalance",
        "MarginPurchaseTodayBalance",
        "MarginPurchaseLimit",
        "ShortSaleBuy",
        "ShortSaleSell",
        "ShortSaleCashRepayment",
        "ShortSaleYesterdayBalance",
        "ShortSaleTodayBalance",
        "ShortSaleLimit",
        "OffsetLoanAndShort",
        "Note",
    ]
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = resp_data.get("data", "")
        data = pd.DataFrame(data, columns=columns)
        data["date"] = date
    else:
        data = pd.DataFrame(columns=columns)
    return data


def clear_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("clear_data")
    for column in [
        "MarginPurchaseBuy",
        "MarginPurchaseSell",
        "MarginPurchaseCashRepayment",
        "MarginPurchaseYesterdayBalance",
        "MarginPurchaseTodayBalance",
        "MarginPurchaseLimit",
        "ShortSaleBuy",
        "ShortSaleSell",
        "ShortSaleCashRepayment",
        "ShortSaleYesterdayBalance",
        "ShortSaleTodayBalance",
        "ShortSaleLimit",
        "OffsetLoanAndShort",
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
    return df
