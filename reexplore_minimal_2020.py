from selenium import webdriver
from time import sleep

if __name__ == "__main__":
    response = webdriver.Chrome('./drivers/chromedriver')
    # response.get("https://internal.swissptt.ch/indigo/win/")
    response.get("https://internal.swissptt.ch/indigo/win/QueryBuilder/DetailAntenna?entityModelName=PA_ANTENNA_P_SEARCHEXTENDED&rid=2040&execute=1")
    print(response)
    sleep(25)
    print(response.page_source)
    btn_runs = response.find_elements_by_xpath(
        '//div[@id="requestValueDialog"]//input')
    if btn_runs and isinstance(btn_runs, list):
        for b in btn_runs:
            # print(b.get_attribute("value"))
            print(b.text)
    btn_runs[-1].click()
    sleep(15)
    btn_runs = response.find_elements_by_xpath(
        '//div[@class="export-excel-btn"]')
    if btn_runs and isinstance(btn_runs, list):
        for b in btn_runs:
            # print(b.get_attribute("value"))
            print(b.text)
    btn_runs[-1].click()
