"""
File containing functionality to scrap zermatt.ch for hotel prices
"""

from selenium import webdriver
from selenium.common import exceptions as err
from xvfbwrapper import Xvfb
from h_price_database.logger import Logger
from time import sleep
from lxml import html


log = Logger()


class ScraperZermatt:

    def __init__(self):
        self.response = None

    def handle_cookies(self):
        cookieconsent = self.response.find_elements_by_xpath('//a[@aria-label="dismiss cookie message"]')
        if cookieconsent:
            cookieconsent[0].click()
            sleep(2)

    def analyse_page(self):
        page_results = []
        parser = html.fromstring(self.response.page_source, self.response.current_url)
        hotels_on_page = parser.xpath('//div[@class="media ng-scope"]')
        if hotels_on_page:
            log.log("Nr of hotels on page: "+str(len(hotels_on_page)))
            for hotel in hotels_on_page:
                hotel_name = hotel.xpath('.//span[@ng-bind="house.lis_name"]')[0].text_content()
                hotel_location = hotel.xpath('.//span[@ng-bind="house.lis_city"]')[0].text_content()
                hotel_price = hotel.xpath('.//span[contains(@ng-bind, "house.lis_price")]')[0].text_content()
                # todo: add info, e.g. 8 bed appartment
                # todo: add number of stars
                page_results.append([hotel_name, hotel_location, hotel_price])
        return page_results

    def main_routine(self):
        # todo: determine how many pages are acutally there
        pages = 10
        results = []
        while pages > 0:
            results.append(self.analyse_page())
            # go to next page
            next_page_buttons = self.response.find_elements_by_xpath('//a[@class="ng-binding"]')
            if next_page_buttons:
                try:
                    next_page_buttons[-2].click()
                    # except err.ElementNotVisibleException:
                    # continue
                except err.WebDriverException as e:
                    log.war(e)
                    self.handle_cookies()
            pages -= 1
        for page in results:
            for hotel in page:
                print(hotel)
        # todo: save to db instead of printing
        # todo: add info about check-in/out, timestamp of run, duration of stay, normalised price
        # todo: add column in db for "suspicious" behavior, e.g. not as many prices/hotels as expected
        print(results)
        print("nr of pages scraped: ", len(results))

    def scrap(self, check_in_date, check_out_date):
        vdisplay = Xvfb()
        vdisplay.start()
        base_url = "https://www.zermatt.ch/en/content/view/full/4716/#/vacancy?"
        full_url = base_url + "datefrom={}&dateto={}&rooms=1&adults1=2&type=all".format(check_in_date, check_out_date)
        self.response = webdriver.Chrome('../drivers/chromedriver')
        self.response.get(full_url)
        # todo: periodically check if search is finised and then scrap on instead of sleeping for 10 sec
        #  key will be the "A total of" ... accomodations were found.
        sleep(10)
        self.main_routine()
        vdisplay.stop()

    @staticmethod
    def dateformat():
        return "%d.%m.%Y"


if __name__ == "__main__":
    scraper = ScraperZermatt()
    scraper.scrap("12.03.2019", "19.03.2019")
