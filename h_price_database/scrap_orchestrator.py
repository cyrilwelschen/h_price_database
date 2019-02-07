"""
Class to orchestrate scrapping: starting it with right routines, collecting results and handing it over.
"""

from datetime import datetime as dt
from h_price_database.logger import Logger
from h_price_database.db_handler import Database
from h_price_database.single_scrap_zermatt import ScraperZermatt
from h_price_database.date_construction_helper import DateConstructionHelper


class ScrapOrchestrator:

    def __init__(self, db_path=None):
        self.log = Logger()
        db_path = db_path if db_path else dt.now().strftime("%Y%m%d_%h%m%s") + "scrp_db.db"
        self.db = Database(db_path)
        # todo: construct Scraper Super Calls and make all scraper inherit and override them
        self.scraper = ScraperZermatt()
        self.date_constructor = DateConstructionHelper(self.scraper.dateformat())
        self.setup_db()

    def setup_db(self):
        # MUST HAVES: name, check_in, check_out, price, scrap_timestamp
        # DERIVED MUST HAVES: stay_duration, normalised_price
        # OPTIONAL: destination, stars, hotel_info, err_war, accomodation_type
        self.db.create_table("scraps",
                             ["name", "check_in", "check_out", "price", "scrap_timestamp", "stay_duration",
                              "normalised_price", "destination", "stars", "hotel_info", "err_war", "accomodation_type"],
                             ["text", "text", "text", "integer", "text", "integer",
                              "integer", "text", "integer", "text", "text", "text"])

    def start(self):
        date_dics = self.date_constructor
        check_ins = []
        check_outs = []
        for di in date_dics:
            check_ins.append(di["check_in"])
            check_outs.append(di["check_out"])
        for i, o in zip(check_ins, check_outs):
            print(i, o)
            scrap_result = self.scraper.scrap(i, o)
