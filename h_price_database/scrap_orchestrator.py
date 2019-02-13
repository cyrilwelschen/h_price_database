"""
Class to orchestrate scrapping: starting it with right routines, collecting results and handing it over.
"""

from datetime import datetime as dt
from h_price_database.logger import Logger
from h_price_database.db_handler import Database
from h_price_database.single_scrap_zermatt import ScraperZermatt
from h_price_database.date_construction_helper import DateConstructionHelper

DB_COLUMNS = ["name", "check_in", "check_out", "price", "scrap_timestamp", "scrap_site",
              "stay_duration", "normalised_price",
              "destination", "stars", "accomodation_info", "err_war", "accomodation_type"]
DB_TYPES = ["text", "text", "text", "real", "text", "text",
            "integer", "real",
            "text", "integer", "text", "text", "text"]


class ScrapOrchestrator:

    def __init__(self, db_path=None):
        self.log = Logger()
        db_path = db_path if db_path else dt.now().strftime("%Y%m%d_%h%m%s") + "scrp_db.db"
        self.db = Database(db_path)
        # todo: construct Scraper Super Calls and make all scraper inherit and override them
        self.scraper = ScraperZermatt()
        self.date_constructor = DateConstructionHelper(self.scraper.dateformat())
        self.setup_db()
        self.check_in = ""
        self.check_out = ""

    def setup_db(self):
        # MUST HAVES: name, check_in, check_out, price, scrap_timestamp, scrap_site
        # DERIVED MUST HAVES: stay_duration, normalised_price
        # OPTIONAL: destination, stars, accomodatoin_info (e.g. 8-bedroom), err_war, accomodation_type (e.g. apartments)
        self.db.create_table("scraps", DB_COLUMNS, DB_TYPES)

    def start(self):
        date_dics = self.date_constructor.standard_date_cycle()
        check_ins = []
        check_outs = []
        for di in date_dics:
            check_ins.append(di["check_in"])
            check_outs.append(di["check_out"])
        counter = 0
        for i, o in zip(check_ins, check_outs):
            counter += 1
            if counter <= 10:
                print("Scraping run {}: ".format(counter), i, o)
                # todo: start subprocess and retry if returns with an error (without subprocess whole cycling is broke)
                scrap_result = self.scraper.scrap(i, o)
                if scrap_result and len(scrap_result) > 5:
                    self.check_in = i
                    self.check_out = o
                    self.scraped_to_db(scrap_result)
                    self.db.commit()
        self.db.close()

    def scraped_to_db(self, list_of_dics):
        for dic in list_of_dics:
            self.db.write_entry(*self.conv_res_to_db(dic))

    def conv_res_to_db(self, single_hotel_dic):
        right_order_db_input = []
        single_hotel_dic["check_in"] = self.check_in
        single_hotel_dic["check_out"] = self.check_out
        single_hotel_dic["scrap_timestamp"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        single_hotel_dic["scrap_site"] = self.scraper.scrap_site
        check_in_dt = dt.strptime(self.check_in, self.scraper.dateformat())
        check_out_dt = dt.strptime(self.check_out, self.scraper.dateformat())
        day_delta = check_out_dt - check_in_dt
        single_hotel_dic["stay_duration"] = day_delta.days
        single_hotel_dic["normalised_price"] = str(int(float(single_hotel_dic["price"].replace(",", ""))/day_delta.days))
        single_hotel_dic["accomodation_type"] = "Hotel" if "Hotel" in single_hotel_dic["name"] else ""
        for col in DB_COLUMNS:
            try:
                writable_element = single_hotel_dic[col]
            except KeyError:
                writable_element = ""
            right_order_db_input.append(writable_element)
        return right_order_db_input


if __name__ == "__main__":
    orchestrator = ScrapOrchestrator("/home/cyril/Desktop/scrap_test_one.db")
    orchestrator.start()
