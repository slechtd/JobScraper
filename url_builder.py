import urllib.parse
from enum import Enum

class DateRange(Enum):
    LAST_24_HOURS = "24h"
    LAST_3_DAYS = "3d"
    LAST_7_DAYS = "7d"
    NONE = None

class UrlBuilder:
    def __init__(self, config_reader):
        self.base_url = config_reader.get_base_url()
        self.general_scrape_url = config_reader.get_general_scrape_url()
        self.location = config_reader.get_location()
        self.radius = config_reader.get_radius()
        self.date_range = DateRange(config_reader.get_date_range())
        self.config_reader = config_reader
    
    def get_general_url(self):
        params = [
            self._build_date_param(),
            self._build_radius_param()
        ]
        url_params = "&".join(filter(None, params))
        return f"{self.base_url}{self.location}{self.general_scrape_url}?{url_params}"
    
    def get_large_page_url(self):
        large_page_number = self.config_reader.get_large_page_number()
        return f"{self.get_general_url()}&page={large_page_number}"
    
    def build_url(self, job_titles, salary=None):
        params = [
            self._build_title_params(job_titles),
            self._build_date_param(),
            self._build_salary_param(salary),
            self._build_radius_param()
        ]
        url_params = "&".join(filter(None, params))
        return f"{self.base_url}{self.location}?{url_params}"
    
    def _build_title_params(self, job_titles):
        return "&".join([f"q%5B%5D={urllib.parse.quote(title)}" for title in job_titles])
    
    def _build_date_param(self):
        if self.date_range is not None and self.date_range != DateRange.NONE:
            return f"date={self.date_range.value}"
        return ""
    
    def _build_salary_param(self, salary):
        return f"salary={salary}" if salary is not None else ""
    
    def _build_radius_param(self):
        return f"locality%5Bradius%5D={self.radius}"
