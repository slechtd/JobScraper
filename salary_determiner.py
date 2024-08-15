from bs4 import BeautifulSoup

class SalaryDeterminer:

    def __init__(self, network_manager, url_builder, logger, config_reader):
        self.network_manager = network_manager
        self.url_builder = url_builder
        self.logger = logger
        self.config_reader = config_reader
        self.low = self.config_reader.get_salary_start()
        self.high = self.config_reader.get_salary_end()
        self.step = self.config_reader.get_salary_step()

    def determine_salary_using_filtered_search(self, title, job_id):
        determined_salary = None

        try:
            # Check if the job listing is found with the lowest salary
            if not self._initial_salary_check(title, self.low, job_id):
                return "Cannot determine"

            # Perform optimized binary search to find the maximum salary
            determined_salary = self._binary_search_salary(title, job_id, self.low, self.high)

            # Return the salary at the lower bound or upper bound based on final check
            final_salary = determined_salary if determined_salary else "Cannot determine"
            self.logger.salary_determined(job_id, final_salary)
            return final_salary

        except Exception as e:
            self.logger.error_salary_determination({e})

    def _make_request_and_parse(self, url):
        response = self.network_manager.throttled_request(url)
        return BeautifulSoup(response.content, "html.parser")

    def _initial_salary_check(self, title, salary, job_id):
        initial_url = self.url_builder.build_url([title], salary=salary)
        self.logger.salary_determination_start(job_id)
        soup = self._make_request_and_parse(initial_url)

        if self._results_not_found_message_shown(soup):
            self.logger.salary_cannot_determine(job_id, salary)
            return False
        else:
            self.logger.salary_binary_search_start(job_id, salary)
            return True

    def _binary_search_salary(self, title, job_id, low, high):
        determined_salary = None

        while (high - low) > self.step:  # Adjusted for precision based on config
            mid = self._adjusted_midpoint(low, high)
            mid_url = self.url_builder.build_url([title], salary=mid)
            soup = self._make_request_and_parse(mid_url)

            if self._job_listing_found(soup, title, job_id):
                self.logger.salary_found_with_midpoint(job_id, mid)
                determined_salary = mid
                low = mid + 1
            else:
                self.logger.salary_not_found_with_midpoint(job_id, mid)
                high = mid - 1

        return determined_salary

    def _adjusted_midpoint(self, low, high):
        # Adjusted midpoint to prioritize salaries that are round numbers or end in 5000.
        mid = (low + high) // 2
        # Round down to the nearest 5000
        if mid % 10000 >= 5000:
            return (mid // 10000) * 10000 + 5000
        else:
            return (mid // 10000) * 10000

    def _results_not_found_message_shown(self, soup):
        return soup.find("div", string=lambda text: text and "Nenašli jsme" in text) is not None

    def _job_listing_found(self, soup, title, job_id):
        job_articles = soup.find_all("article", class_="SearchResultCard")
        for job_article in job_articles:
            title_found = job_article.find("h2", {"data-test-ad-title": title})
            id_found = job_article.find("a", {"data-jobad-id": job_id})
            if title_found is not None and id_found is not None:
                return True
        return False
