from enum import Enum
import base64

class JobListing:
    def __init__(self, job_section, search_position, logger, utils, salary_determiner, time_stamp, page_number, scrape_url):
        self.job_section = job_section
        self.logger = logger
        self.utils = utils
        self.salary_determiner = salary_determiner
        self.search_position = search_position
        self.time_stamp = time_stamp
        self.page_number = page_number
        self.scrape_url = scrape_url
        self.title_tag = self._get_title_tag()
        try:
            self.job_id = self._extract_job_id()
            self.title = self._extract_title()
            self.company = self._extract_company()
            self.location = self._extract_location()
            self.creation_date = self._extract_creation_date()
            self.tip = self._extract_tip()
            self.tags = self._extract_tags()
            self.displayed_salary_range = self._extract_salary()
            self.determined_max_salary = self._determine_max_salary() if self.displayed_salary_range is None else None
            self.atmoskop_url, self.atmoskop_reviews = self._extract_atmoskop_info()
            self.url = self._extract_url()
            self.page_text = self.utils.fetch_detail_text(self.url)
            self.logger.listing_initialised(self.job_id)
        except Exception as e:
            self.logger.error_initialising_job_listing(search_position, e)
            raise

    def to_dict(self):
        return {
            "execution_timestamp": self.time_stamp,
            "job_id": self.job_id,
            "scrape_url": self.scrape_url,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "creation_date": self.creation_date,
            "page_number": self.page_number,
            "search_position": self.search_position,
            "tip": self.tip,
            "tags": self.tags,
            "displayed_salary_range": self.displayed_salary_range,
            "determined_max_salary": self.determined_max_salary,
            "atmoskop_url": self.atmoskop_url,
            "reviews": self.atmoskop_reviews,
            "detail_page_url": self.url,
            "detail_page_text": self.page_text
            }
    
    def _get_title_tag(self):
        return self.job_section.find("h2", class_="SearchResultCard__title")

    def _extract_job_id(self):
        url_tag = self.title_tag.find("a") if self.title_tag else None
        return url_tag["data-jobad-id"] if url_tag else None

    def _extract_title(self):
        return self.title_tag.get_text(strip=True) if self.title_tag else None
    
    def _extract_company(self):
        company_tag = self.job_section.find("span", translate="no")
        return company_tag.get_text(strip=True) if company_tag else None

    def _extract_location(self):
        location_tag = self.job_section.find("li", {"data-test": "serp-locality"})
        return location_tag.get_text(strip=True) if location_tag else None

    def _extract_creation_date(self):
        creation_date_tag = self.job_section.find("div", {"data-test-ad-status": "default"})
        return creation_date_tag.get_text(strip=True) if creation_date_tag else None
    
    def _extract_tip(self):
        tip_tag = self.job_section.find("div", {"data-test-ad-status": "jobsTip"})
        return tip_tag.get_text(strip=True) if tip_tag else None

    def _extract_tags(self):
        tags = self.job_section.find_all("span", class_=["Tag", "Tag--neutral", "Tag--small", "Tag--subtle"])
        return [tag.get_text(strip=True) for tag in tags] if tags else []

    def _extract_salary(self):
        salary_tag = self.job_section.find("span", class_="Tag--success")
        if salary_tag:
            return salary_tag.get_text(strip=True)
        return None
    
    def _determine_max_salary(self):
        return self.salary_determiner.determine_salary_using_filtered_search(self.title, self.job_id)

    def _extract_atmoskop_info(self):
        atmoskop_tag = self.job_section.find("a", {"data-test": "serp-atmoskop"})
        if atmoskop_tag:
            return atmoskop_tag["href"], atmoskop_tag.get_text(strip=True)
        return None, None
    
    def _extract_url(self):
        url_tag = self.title_tag.find("a") if self.title_tag else None
        return url_tag["href"] if url_tag else None
