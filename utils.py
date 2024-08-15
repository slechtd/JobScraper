import re
from bs4 import BeautifulSoup

class Utils:
    def __init__(self, logger, network_manager, config_reader, url_builder):
        self.logger = logger
        self.network_manager = network_manager
        self.config_reader = config_reader
        self.url_builder = url_builder

    def get_total_pages(self):
        if self.config_reader.get_limit_to_one_page():
            return 1

        large_page_url = self.url_builder.get_large_page_url()

        response = self.network_manager.throttled_request(large_page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        current_page_link = soup.find("a", class_="Pagination__link--current")
        if current_page_link:
            last_page = self._extract_numeric_value(current_page_link.get_text(strip=True))
            if last_page is not None:
                return last_page
            else:
                self.logger.pages_could_not_get_total()
        return 1

    def _extract_numeric_value(self, text):
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None

    def fetch_source_code(self, url):
        if self.config_reader.get_scrape_full_job_pages():
            response = self.network_manager.throttled_request(url)
            return response.text
        return "<placeholder>"
