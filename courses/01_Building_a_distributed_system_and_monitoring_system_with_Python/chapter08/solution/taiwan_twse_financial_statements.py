import typing
import requests
import numpy as np
import pandas as pd
from loguru import logger


def header():
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "161",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "mops.twse.com.tw",
        "Origin": "https://mops.twse.com.tw",
        "Referer": "https://mops.twse.com.tw/mops/web/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }


def no_reponse(response: str) -> bool:
    no_reponse_condiction = (
        "之公司不存在！" in response
        or "查無所需資料！" in response
        or "公司不繼續公開發行！" in response
        or "資料庫中查無需求資料" in response
        or "查詢無資料!" in response
    )
    return True if no_reponse_condiction else False


def crawler(
    parameter: typing.Dict[str, str]
) -> pd.DataFrame:
    logger.info(parameter)
    kind = parameter.get("kind")
    year = parameter.get("year")
    quar = parameter.get("quar")

    url = "https://mops.twse.com.tw/mops/web/ajax_t163sb04"
    form_data = {
        "encodeURIComponent": "1",
        "step": "1",
        "firstin": "1",
        "off": "1",
        "isQuery": "Y",
        "TYPEK": kind,
        "year": year,
        "season": f"0{quar}",
    }
    resp = requests.post(url, headers=header(), data=form_data)
    str_data = resp.text
    if no_reponse(str_data):
        df = pd.DataFrame()
    else:
        df = pd.read_html(str_data, header=None)
    return df

if __name__ == "__main__":
    # kind: sii, otc, rotc, pub
    parameter = {"kind":"sii", "year":111, "quar":1}
    df = crawler(parameter)
    print(df)