import requests


stock_id = "6488"
g_recaptcha_response = "03AGdBq24KtcpJRHtTwmX5mDd4DZkTeIQU2WQwI4Z9NMl4-ay24gLDkRpJqd26MpKIh1ab_7hMthHI0ib3PiExyNkEA5fsH-ntTTMyWFjh8wbYda1aMKOFSPmYmRao-D0wi5jvOvixgtQd5CpI0C0M4XrPSit78vAfHOLfQZx5sHRSmihG-DmOtrSRDIG6fKatWDMOoqUEuPChZWVtuHCDdphcuELGOKCS9rYwqq6Mw9n0CN1i0ZDus9iZ50bNlSYkDkmK_orkhiltNHsI5L-tk9IVpXpdP7M7J1OD3qT3tUxRaxAEsL4Hrm00IwQmcz7bznyWy02r7gTaZhoCgkfskLi5KMoTumnw7FbfI9YkP7m3u9saMsUQacvAZM74CdN66ORW9Uae-FgGzqRLG_t8gh68Yc87Hon-0YfSlgXStoaxDO47hCx1Uop8Wqr-w445-5KxmeNT-J4p"

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
    "g-recaptcha-response": g_recaptcha_response,
    "stk_code": stock_id,
    "charset": "BIG5"
}
# url = "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw"
url = "https://www.tpex.org.tw/web/stock/aftertrading/broker_trading/download_ALLCSV.php"
res = requests.post(
    url=url, headers=headers, data=form_data
)
tem = res.text
print(tem)
# print("1,374,649,744" in tem)



