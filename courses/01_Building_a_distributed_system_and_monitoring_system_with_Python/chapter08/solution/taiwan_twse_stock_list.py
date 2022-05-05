import datetime
import typing

import pandas as pd
import requests
from loguru import logger
from lxml import etree


def header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Pragma": "no-cache",
        "Referer": "http://www.twse.com.tw/zh/page/trading/exchange/FMSRFK.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    }


def no_crawler_list():
    return [
        "全部",
        "全部(不含權證、牛熊證、可展延牛熊證)",
        "所有證券(不含權證、牛熊證)",
        "封閉式基金",
        "受益證券",
        "認購售權證",
        "展延型牛熊證",
        "認購權證(不含牛證)",
        "認售權證(不含熊證)",
        "牛證(不含可展延牛證)",
        "熊證(不含可展延熊證)",
        "牛熊證(不含展延型牛熊證)",
        "可展延牛證",
        "可展延熊證",
        "附認股權特別股",
        "附認股權公司債",
        "可轉換公司債",
        "認股權憑證",
        "所有證券",
        "委託及成交資訊(16:05提供)",
    ]


def create_industry_category_id() -> typing.List[
    typing.Dict[str, typing.Union[str, int, float]]
]:
    url = "http://www.twse.com.tw/zh/page/trading/exchange/BFT41U.html"
    res = requests.get(url, header())
    res.encoding = "utf-8"
    page = etree.HTML(res.text)
    temp = page.xpath('//select[@name="selectType"]//option')
    page = etree.HTML(res.text)
    temp = page.xpath("//option")
    loop_list = [
        dict(_id=te.attrib["value"], industry_category=te.text, _type="twse")
        for te in temp
        if te.text.replace(" ", "") not in no_crawler_list()
    ]
    return loop_list


def crawler(date:str) -> pd.DataFrame:
    datas = []
    industry_category = create_industry_category_id()
    for d in industry_category:
        try:
            logger.info(f"crawler id :{d}")
            _id = d.get("_id")
            url = "https://www.twse.com.tw/zh/api/codeFilters?filter={id}".format(id=_id)
            res = requests.get(url, header())
            data = pd.DataFrame(res.json())
            datas.append(data)
        except Exception as e:
            logger.info(e)
    datas = pd.concat(datas, axis=0)
    datas["date"] = date
    return datas

if __name__ == "__main__":
    date = "2022-05-05"
    data = crawler(date)
    print(data)
