"""
File containing functionality to scrap zermatt.ch for hotel prices
"""

from selenium import webdriver
from xvfbwrapper import Xvfb
from h_price_database.logger import Logger


log = Logger()


def parse(url):
    print("Starting")
    log.log("Starting")

    response = webdriver.Chrome('../drivers/chromedriver')
    response.get(url)
    print(response.current_url)


if __name__ == "__main__":
    vdisplay = Xvfb()
    vdisplay.start()
    parse("https://www.zermatt.ch/en/book")
    vdisplay.stop()
