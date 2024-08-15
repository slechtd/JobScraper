from file_manager import FileManager
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
        self.file_manager = FileManager(self.logger, self.time_stamp, self.config_reader)
        self.salary_determiner = SalaryDeterminer(self.network_manager, self.url_builder, self.logger, self.config_reader)

        # Init Scraper
        self.scraper = Scraper(
            logger=self.logger,
            utils=self.utils,
            network_manager=self.network_manager,
            url_builder=self.url_builder,
            file_manager=self.file_manager,
            salary_determiner=self.salary_determiner
        )

    def start_scraping(self):
        self.scraper.start_scraping()

if __name__ == "__main__":
    main = Main()
    main.start_scraping()
