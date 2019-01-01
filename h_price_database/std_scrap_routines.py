"""
File contains standard scraping routines/functions. E.g. to search for button and press if found.
"""

from lxml import html
from h_price_database.logger import Logger

log = Logger()


class StandardScraper:

    def __init__(self, response):
        self.name = "StandardScraper from std_scrap_routine.py"
        self.response = response
        self._parser = None
        self.parser()

    def parser(self):
        self._parser = html.fromstring(self.response.page_source, self.response.current_url)

    def find_like(self, tag, attr, value):
        return self._parser.xpath('.//{}[contains(@{}, "{}")]'.format(tag, attr, value))

    def find_exact(self, tag, attr, value):
        return self._parser.xpath('.//{}[@{}="{}"]'.format(tag, attr, value))

    def yield_like(self, tag, attr, value):
        return self._parser.xpath('.//{}[contains(@{}, "{}")]'.format(tag, attr, value))[0].text_content()

    def yield_exact(self, tag, attr, value):
        return self._parser.xpath('.//{}[@{}="{}"]'.format(tag, attr, value))[0].text_content()

    def push_button(self, button_element, index=0, pre_action_check=True, post_action_check=True, **allowed_exceptions):
        # todo: allowed_exceptions clause won't work!
        self.check(pre_action_check, post_action_check)
        """
        next_page_buttons = self.response.find_elements_by_xpath('//a[@class="ng-binding"]')
        if next_page_buttons:
            try:
                next_page_buttons[-2].click()
            except err.WebDriverException as e:
                log.war(e)
                self.handle_cookies()
        """
        try:
            button_element[index].click()
        except allowed_exceptions as e:
            log.war(e, "Std_Scraper_Allawoed_Exception")
            pass

    def find_exact_and_push(self, tag, attr, value, index=0, pre_action_check=True, post_action_check=True,
                            **allowed_exceptions):
        element_to_click = self.find_exact(tag=tag, attr=attr, value=value)
        self.push_button(element_to_click, index=index, pre_action_check=pre_action_check,
                         post_action_check=post_action_check, **allowed_exceptions)

    def find_like_and_push(self, tag, attr, value, index=0, pre_action_check=True, post_action_check=True,
                           **allowed_exceptions):
        element_to_click = self.find_like(tag=tag, attr=attr, value=value)
        self.push_button(element_to_click, index=index, pre_action_check=pre_action_check,
                         post_action_check=post_action_check, **allowed_exceptions)

    def set_value(self, pre_action_check=True, post_action_check=True, **allowed_exceptions):
        self.check(pre_action_check, post_action_check)
        try:
            pass
        except allowed_exceptions as e:
            log.war(e, "Std_Explorer_Allowed_Exception")
            pass

    def check(self, pre, post):
        if pre:
            self.pre_action_check()
        if post:
            self.post_action_check()

    def pre_action_check(self):
        pass

    def post_action_check(self):
        pass
