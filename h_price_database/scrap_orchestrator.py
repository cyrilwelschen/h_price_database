"""
Class to orchestrate scrapping: starting it with right routines, collecting results and handing it over.
"""

from h_price_database.logger import Logger


class ScrapOrchestrator:

    def __init__(self):
        self.log = Logger()
