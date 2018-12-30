"""
File contains standard scraping routines/functions. E.g. to search for button and press if found.
"""


from lxml import html


class Analyser:

    def __init__(self, response):
        self.name = "Analyser from std_scrap_routine.py"
        self.version = "0.0.1"
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

    # Example of analyse
    """"
        parser = html.fromstring(self.response.page_source, self.response.current_url)
        hotels_on_page = parser.xpath('//div[@class="media ng-scope"]')
        if hotels_on_page:
            log.log(len(hotels_on_page))
            for hotel in hotels_on_page:
                hotel_name = hotel.xpath('.//span[@ng-bind="house.lis_name"]')[0].text_content()
                hotel_location = hotel.xpath('.//span[@ng-bind="house.lis_city"]')[0].text_content()
                hotel_price = hotel.xpath('.//span[contains(@ng-bind, "house.lis_price")]')[0].text_content()
                page_results.append([hotel_name, hotel_location, hotel_price])
    """


class Explorer:

    def __init__(self):
        self.name = "Explorer from std_scrap_routine.py"
        self.version = "0.0.1"
        self.response = None

    def push_button(self, pre_action_check=True, post_action_check=True, **allowed_exceptions):
        self.check(pre_action_check, post_action_check)
        pass

    def set_value(self, pre_action_check=True, post_action_check=True, **allowed_exceptions):
        self.check(pre_action_check, post_action_check)
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

    # Example of explore
    """
    def handle_cookies(self):
        cookieconsent = self.response.find_elements_by_xpath('//a[@aria-label="dismiss cookie message"]')
        if cookieconsent:
            cookieconsent[0].click()
            sleep(2)
    """
