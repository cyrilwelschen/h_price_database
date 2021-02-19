"""
File containing functionality to scrap zermatt.ch for hotel prices
"""

from selenium import webdriver
from selenium.common import exceptions as err
from time import sleep
from lxml import html
from logger import Logger
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


log = Logger()


class ScraperZermatt:

    def __init__(self):
        self.response = None
        self.scrap_site = "zermatt.ch"

    def handle_cookies(self):
        cookieconsent = self.response.find_elements_by_xpath(
            '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]')
        if cookieconsent:
            cookieconsent[0].click()
            sleep(2)

    def analyse_page(self):
        page_results = []
        parser = html.fromstring(
            self.response.page_source, self.response.current_url)
        hotels_on_page = parser.xpath('//div[@class="media ng-scope"]')
        if hotels_on_page:
            log.log("Nr of hotels on page: "+str(len(hotels_on_page)))
            for hotel in hotels_on_page:
                hotel_name = hotel.xpath(
                    './/span[@ng-bind="house.lis_name"]')[0].text_content()
                hotel_location = hotel.xpath(
                    './/span[@ng-bind="house.lis_city"]')[0].text_content()
                hotel_price = hotel.xpath(
                    './/span[contains(@ng-bind, "house.lis_price")]')[0].text_content()
                try:
                    accomodation_info = hotel.xpath(
                        './/p[contains(@ng-bind, "house.lis_name_add")]')[0].text_content()
                except IndexError:
                    accomodation_info = ""
                stars = len(hotel.xpath(
                    './/i[@class="icon-star icon-hotel-star ng-scope"]'))
                page_results.append({"name": hotel_name, "destination": hotel_location, "price": hotel_price,
                                     "accomodation_info": accomodation_info, "stars": stars})
        return page_results

    def main_routine(self):
        last_page_reached = False
        safety_counter = 0
        results = []
        while not last_page_reached:
            self.handle_cookies()
            results.append(self.analyse_page())
            # go to next page
            next_page_links = self.response.find_elements_by_xpath(
                '//a[@class="ng-binding"]')
            if next_page_links:
                try:
                    next_page_links[-2].click()
                    # except err.ElementNotVisibleException:
                    # continue
                except err.WebDriverException as e:
                    log.war(e)
                    self.handle_cookies()
            """
            next_page_buttons = self.response.find_elements_by_xpath(
                '//li[@ng-repeat="page in pages"]')
            last_page_button_class = next_page_buttons[-1].get_attribute(
                "class")
            if last_page_button_class == "ng-scope disabled":
                last_page_reached = True
            safety_counter += 1
            if safety_counter > 30:
                last_page_reached = True
            """
            last_page_reached = True

        print(safety_counter)
        return results

    def scrap(self, check_in_date, check_out_date):
        base_url = "https://www.zermatt.ch/content/view/full/59606?&"
        full_url = base_url + "checkin={}&checkout={}&room=2".format(check_in_date, check_out_date)
        self.response = webdriver.Chrome()
        self.response.get(full_url)
        self.wait_for_load_finish()
        list_of_list_results = self.main_routine()
        master_list = []
        for li in list_of_list_results:
            master_list += li
        return master_list

    def wait_for_load_finish(self):
        timer = 0
        while timer < 10:
            sleep(1)
            timer += 1
            """
            loading_string = self.response.find_elements_by_xpath(
                '//div[@class="result_info ng-scope"]')
            try:
                search_progress_string = loading_string[0].text
                if "A total" in search_progress_string:
                    timer = 11
                print("progress string: ".format(search_progress_string))
                print("breaking timer")
            except AttributeError:
                print("finder failed")
            print("loading since {} sec".format(timer))
            """

    @staticmethod
    def dateformat():
        return "%d.%m.%Y"


if __name__ == "__main__":
    scraper = ScraperZermatt()
    result = scraper.scrap("20210316", "20210319")
    print(result)
    print(len(result))
