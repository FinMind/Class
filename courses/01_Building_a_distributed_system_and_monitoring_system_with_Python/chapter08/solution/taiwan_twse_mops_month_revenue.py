import typing

import pandas as pd
import requests
from loguru import logger
from lxml import etree


def header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "mops.twse.com.tw",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }


def crawler(parameter: typing.Dict[str, str]) -> pd.DataFrame:
    logger.info(parameter)
    year = parameter.get("year", 111)
    month = parameter.get("month", 1)
    _type = parameter.get("_type", 'sii')
    foreign = parameter.get("foreign", 0)
    url = "https://mops.twse.com.tw/nas/t21/{}/t21sc03_{}_{}_{}.html".format(_type, year, month, foreign)

    response = requests.get(url, header())
    response.encoding = "big5"
    if not response.text:
        return pd.DataFrame()
    page = etree.HTML(response.text)
    stock_id = [
        x.text for x in page.xpath("//tr//td[@align='center']") if x.text != "-"
    ]
    temp = page.xpath("//tr//td")
    bo = 0
    month_revenue = []
    for i in range(len(temp)):
        if bo == 1:
            x = "{}000".format(
                temp[i + 1].text.replace(",", "").replace(" ", "")
            )
            month_revenue.append(x)
        bo = 0
        if temp[i].text in stock_id:
            bo = 1
    year = int(year) + 1911
    data = pd.DataFrame(
        dict(
            stock_id=stock_id,
            revenue=month_revenue,
            revenue_year=year,
            revenue_month=month,
        )
    )
    return data

if __name__ == "__main__":
    # _type: sii, otc
    # foreign: 0, 1
    parameter = {"kind":"sii", "year":111, "month":1, "_type":"sii", "foreign":0}
    df = crawler(parameter)
    print(df)