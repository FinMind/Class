import requests
import json
import pandas as pd


URL = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20220123&stockNo=2330&_=1642919411983"
resp = requests.get(URL)

resp_data = json.loads(resp.text)

data = pd.DataFrame(resp_data["data"], columns=resp_data["fields"])

print(data)