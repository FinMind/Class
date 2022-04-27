import time
import requests

from financialdata import config


APIKEY_2CAPTCHA = config.APIKEY_2CAPTCHA
data_sitekey = "6LcCoP8SAAAAAKzsvbTXymxqNWcC-dAhDYik0V3C"
url = "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/download_ALLCSV.php"

two_captcha_url = f"http://2captcha.com/in.php?key={APIKEY_2CAPTCHA}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={url}"
res0 = requests.get(two_captcha_url)
rid = res0.text.split("|")[-1]
print(f"rid:{rid}")
time.sleep(20)

two_captcha_res_url = f"http://2captcha.com/res.php?id={rid}&key={APIKEY_2CAPTCHA}&action=get"
res1 = requests.get(two_captcha_res_url)
g_recaptcha_response = res1.text.split("|")[-1]
print(f"g_recaptcha_response:{g_recaptcha_response}")

stock_id = "6488"

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
    "g-recaptcha-response": g_recaptcha_response,
    "stk_code": stock_id,
}

res = requests.post(
    url=url, headers=headers, data=form_data, timeout=120
)
print(res.text)
