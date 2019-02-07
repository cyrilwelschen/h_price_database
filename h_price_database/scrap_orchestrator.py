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
        pass

    def start(self):
        for check_in, check_out in self.date_constructor.standard_date_cycle():
            single_scrp_output = self.scraper.scrap(check_in, check_out)
            # todo: save to db
