import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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
    
    def fetch_detail_text(self, url):
        if self.config_reader.get_scrape_detail_text():
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    
                    html_content = page.content()
                    browser.close()

                    soup = BeautifulSoup(html_content, "html.parser")
                    for tag in soup(["script", "style", "header", "footer", "nav", "iframe", "noscript", "form", "aside"]):
                        tag.decompose()

                    visible_text = soup.get_text(separator=' ', strip=True)
                    # Trim everything after "Podmínky Jobs.cz"
                    visible_text = self._trim_after_phrase(visible_text, "Pošleme Vám obdobné nabídky")
                    
                    return self._make_string_json_safe(visible_text)

            except Exception as e:
                self.logger.error_playwright(e)
        
        return None

    def _trim_after_phrase(self, text, phrase):
        index = text.find(phrase)
        if index != -1:
            text = text[:index]
        return text

    def _make_string_json_safe(self, string):
        safe_string = string.replace('\\', '\\\\').replace('"', '\\"')
        return safe_string