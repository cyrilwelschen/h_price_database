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


def run(check_in_date, check_out_date):
    vdisplay = Xvfb()
    vdisplay.start()
    base_url = "https://www.zermatt.ch/en/content/view/full/4716/#/vacancy?"
    parse(base_url+"datefrom={}&dateto={}&rooms=1&adults1=2&type=all".format(check_in_date, check_out_date))
    vdisplay.stop()


if __name__ == "__main__":
    run("12.01.2019", "19.01.2019")
