from utils import Utils
from url_builder import UrlBuilder
from network_manager import NetworkManager
from logger import Logger
from scraper import Scraper
from salary_determiner import SalaryDeterminer
from config_reader import ConfigReader
from datetime import datetime

class Main:
    def __init__(self):

        # Generate the time stamp (execution ID)
        self.time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Dependencies
        self.config_reader = ConfigReader()
        self.logger = Logger(self.config_reader, self.time_stamp)
        self.network_manager = NetworkManager(self.logger, self.config_reader)
        self.url_builder = UrlBuilder(self.config_reader)
        self.utils = Utils(self.logger, self.network_manager, self.config_reader, self.url_builder)
        self.salary_determiner = SalaryDeterminer(self.network_manager, self.url_builder, self.logger, self.config_reader)

        # Init Scraper
        self.scraper = Scraper(
            logger=self.logger,
            utils=self.utils,
            network_manager=self.network_manager,
            url_builder=self.url_builder,
            salary_determiner=self.salary_determiner,
            time_stamp=self.time_stamp,
            config_reader=self.config_reader
        )

    def start_scraping(self):
        try:
            self.scraper.start_scraping()
        except Exception as e:
            self.logger.error_general(e)
            self.network_manager.send_slack_error_notif(self.time_stamp, e)
        finally:
            self.logger.flush_logs()
            self.network_manager.send_slack_finish_notif(self.time_stamp)

if __name__ == "__main__":
    main = Main()
    main.start_scraping()
