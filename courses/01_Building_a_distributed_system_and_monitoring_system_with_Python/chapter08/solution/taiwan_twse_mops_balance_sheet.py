import typing
import requests

import pandas as pd
from loguru import logger


def no_response(response: str) -> bool:
    if not response or "查無所需資料" in response:
        return True
    else:
        return False


def crawler(parameter: typing.Dict[str, str]) -> pd.DataFrame:
    logger.info(parameter)
    kind = parameter.get("kind", "sii")
    year = parameter.get("year", 111)
    quar = parameter.get("quar", 1)

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
    url = "https://mops.twse.com.tw/mops/web/ajax_t163sb05"
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