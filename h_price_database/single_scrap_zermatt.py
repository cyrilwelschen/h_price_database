"""
File containing functionality to scrap zermatt.ch for hotel prices
"""

from selenium import webdriver
from xvfbwrapper import Xvfb
from h_price_database.logger import Logger
from time import sleep
from lxml import html


log = Logger()


def parse(url):
    # log.log("Starting")
    response = webdriver.Chrome('../drivers/chromedriver')
    response.get(url)
    print(response.current_url)
    # todo: periodically check if search is finised and then go on instead of sleeping for 10 sec
    sleep(10)

    parser = html.fromstring(response.page_source, response.current_url)
    hotels_on_page = parser.xpath('//div[@class="media ng-scope"]')
    if hotels_on_page:
        log.log(len(hotels_on_page))
        for hotel in hotels_on_page:
            hotel_name = hotel.xpath('.//span[@ng-bind="house.lis_name"]')
            hotel_location = hotel.xpath('.//span[@ng-bind="house.lis_city"]')
            hotel_price = hotel.xpath('.//span[contains(@ng-bind, "house.lis_price")]')
            print(hotel_name[0].text_content(), hotel_location[0].text_content(), hotel_price[0].text_content())

    next_page_buttons = response.find_elements_by_xpath('//a[@class="ng-binding"]')
    if next_page_buttons:
        print(len(next_page_buttons))
        cookieconsent = response.find_elements_by_xpath('//a[@aria-label="dismiss cookie message"]')
        if cookieconsent:
            cookieconsent[0].click()
            sleep(2)
        next_page_buttons[-2].click()
        print(response.current_url)

        parser = html.fromstring(response.page_source, response.current_url)
        hotels_on_page = parser.xpath('//div[@class="media ng-scope"]')
        if hotels_on_page:
            log.log(len(hotels_on_page))
            for hotel in hotels_on_page:
                hotel_name = hotel.xpath('.//span[@ng-bind="house.lis_name"]')
                hotel_location = hotel.xpath('.//span[@ng-bind="house.lis_city"]')
                hotel_price = hotel.xpath('.//span[contains(@ng-bind, "house.lis_price")]')
                print(hotel_name[0].text_content(), hotel_location[0].text_content(), hotel_price[0].text_content())


def run(check_in_date, check_out_date):
    vdisplay = Xvfb()
    vdisplay.start()
    base_url = "https://www.zermatt.ch/en/content/view/full/4716/#/vacancy?"
    parse(base_url+"datefrom={}&dateto={}&rooms=1&adults1=2&type=all".format(check_in_date, check_out_date))
    vdisplay.stop()


if __name__ == "__main__":
    run("12.01.2019", "19.01.2019")
