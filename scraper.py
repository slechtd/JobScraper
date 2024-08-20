from bs4 import BeautifulSoup
from job_listing import JobListing
from output_manager import OutPutManager

class Scraper:
    def __init__(self, logger, utils, network_manager, url_builder, salary_determiner, time_stamp, config_reader):
        self.logger = logger
        self.utils = utils
        self.network_manager = network_manager
        self.url_builder = url_builder
        self.salary_determiner = salary_determiner
        self.time_stamp = time_stamp
        self.config_reader = config_reader

        self.output_manager = OutPutManager(self.logger, self.time_stamp, self.config_reader)
    
    def start_scraping(self):
        try:
            general_url = self.url_builder.get_general_url()
            total_pages = self.utils.get_total_pages()
            for page_number in range(1, total_pages + 1):
                self.logger.scraping_page(page_number, total_pages)
                page_url = f"{general_url}&page={page_number}"  # Can be moved to the URL builder !!!!!!!!!!!!!!!!!!
                self._process_page(page_url, page_number)
        except AttributeError:
            self.logger.error_general("URL not found")
        except Exception as e:
            self.logger.error_general({e})
            raise
    
    def _process_page(self, url, page_number):
        try:
            response = self.network_manager.throttled_request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            job_sections = soup.find_all("article", class_="SearchResultCard")
            self.logger.number_of_listings_on_page(len(job_sections), page_number)
            jobs = [self._process_job_section(job_section, index + 1) for index, job_section in enumerate(job_sections)]
            self.output_manager.save_page_jobs([job for job in jobs if job is not None], page_number)
        except Exception as e:
            self.logger.error_scraping_page({e})
        
    def _process_job_section(self, job_section, search_position):
        try:
            job = JobListing(job_section, search_position, self.logger, self.utils, self.salary_determiner)
            return job.to_dict()
        except Exception as e:
            self.logger.error_general({e})
            return None
