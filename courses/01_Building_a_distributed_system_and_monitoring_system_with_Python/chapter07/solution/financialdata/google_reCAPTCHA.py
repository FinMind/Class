import io
import time

import pandas as pd
import requests
from loguru import logger

from financialdata import config

APIKEY_2CAPTCHA = config.APIKEY_2CAPTCHA


def get_2captcha_jobid(url:str) -> str:
    data_sitekey = "6LcCoP8SAAAAAKzsvbTXymxqNWcC-dAhDYik0V3C"
    two_captcha_url = f"http://2captcha.com/in.php?key={APIKEY_2CAPTCHA}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={url}"
    res_job_id = requests.get(two_captcha_url)
    rid = res_job_id.text.split("|")[-1]
    logger.info(f"rid:{rid}")
    return rid


def get_g_recaptcha_response(rid:str) -> str:
    g_recaptcha_response = ""
    for i in range(10):
        two_captcha_res_url = f"http://2captcha.com/res.php?id={rid}&key={APIKEY_2CAPTCHA}&action=get"
        res = requests.get(two_captcha_res_url)
        g_recaptcha_response = res.text.split("|")[-1]
        logger.info(f"g_recaptcha_response:{g_recaptcha_response}")
        if g_recaptcha_response in ["CAPCHA_NOT_READY"]:
            time.sleep(5)
        else:
            break
    return g_recaptcha_response


def get_2captcha_token(url: str) -> str:
    jobid = get_2captcha_jobid(url)
    g_recaptcha_response = get_g_recaptcha_response(jobid)
    return g_recaptcha_response


def request_data(stock_id:str, url:str) -> pd.DataFrame:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "369",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.tpex.org.tw",
        "Origin": "https://www.tpex.org.tw",
        "Referer": "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    form_data = {
        "charset": "BIG5",
        "g-recaptcha-response": get_2captcha_token(url),
        "stk_code": stock_id,
    }

    res = requests.post(
        url=url, headers=headers, data=form_data, timeout=120
    )
    tem = res.text.replace(f"券商買賣證券成交價量資訊\r\n證券代碼,{stock_id}\r\n", "")

    df = pd.read_csv(io.StringIO(tem))
    return df


def crawler(stock_id):
    url = "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/download_ALLCSV.php"
    df = pd.DataFrame()
    try:
        df = request_data(stock_id, url)
    except Exception as e:
        logger.error(e)
    return df


if __name__ == "__main__":
    stock_id = "6488"
    df = crawler(stock_id)
    print(df)
