import os
import time

import cv2
import numpy as np
import pandas as pd
from loguru import logger
from selenium import webdriver

from financialdata.vcode import VerifyCode


vc_model = VerifyCode()


def run_chrome() -> webdriver.chrome.webdriver.WebDriver:
    logger.info("run_chrome")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--verbose")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "/tmp/data",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
        },
    )
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver",
        chrome_options=options,
    )
    time.sleep(1)
    return driver


def input_stock_id(
    driver: webdriver.chrome.webdriver.WebDriver, stock_id: str
) -> webdriver.chrome.webdriver.WebDriver:
    logger.info("input_stock_id")
    el = driver.find_elements_by_xpath('//*[@id="TextBox_Stkno"]')
    el[0].send_keys(stock_id)
    return driver


def find_download_link(driver: webdriver.chrome.webdriver.WebDriver) -> str:
    el = driver.find_elements_by_xpath('//*[@id="HyperLink_DownloadCSV"]')
    if el:
        href = el[0].get_attribute("href")
        logger.info(f"get href: {href}")
        return href
    return ""


def download_file(driver: webdriver.chrome.webdriver.WebDriver, href: str):
    logger.info("download_file")
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {
            "behavior": "allow",
            "downloadPath": "/tmp/data",
        },
    }
    driver.execute("send_command", params)
    driver.get(href)
    time.sleep(1)
    logger.info("download")


def load_file(stock_id: str) -> pd.DataFrame:
    file_path = f"/tmp/data/{stock_id}.csv"
    data = pd.read_csv(file_path, encoding="big5hkscs", skiprows=2)
    os.remove(file_path)
    logger.info("read csv")
    return data


def get_vcode_and_verify(
    driver: webdriver.chrome.webdriver.WebDriver,
) -> webdriver.chrome.webdriver.WebDriver:
    for i in range(10):
        driver.find_elements_by_xpath(
            '//*[@id="Panel_bshtm"]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div[1]/img'
        )
        driver.save_screenshot("/tmp/img/temp.png")
        time.sleep(1)
        img = cv2.imread("/tmp/img/temp.png")
        img = img[320:380, 300:500]
        text = vc_model.predict(img)
        logger.info(text)
        el = driver.find_elements_by_xpath(
            '//*[@id="Panel_bshtm"]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div[2]/input'
        )

        el[0].send_keys(text)
        el = driver.find_elements_by_xpath('//*[@id="btnOK"]')
        el[0].click()

        el = driver.find_elements_by_xpath('//*[@id="Label_ErrorMsg"]')
        if el[0].text == "驗證碼錯誤!":
            logger.error(f"Retry {i}, {el[0].text}")
        else:
            return driver
    return driver


def crawler(stock_id):
    df = pd.DataFrame()
    try:
        url = "https://bsr.twse.com.tw/bshtm/bsMenu.aspx"
        driver = run_chrome()
        driver.get(url)

        # 輸入股票代碼
        driver = input_stock_id(driver, stock_id)

        # 下載驗證碼，並做驗證
        driver = get_vcode_and_verify(driver)

        # 尋找下載 csv 的 link
        href = find_download_link(driver)

        # 下載 csv
        download_file(driver, href)

        # 讀取 csv
        df = load_file(stock_id)
        driver.close()
    except Exception as e:
        logger.error(e)
    return df


if __name__ == "__main__":
    stock_id = "2330"
    df = crawler(stock_id=stock_id)
    print(df)

