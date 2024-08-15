import configparser

class ConfigReader:
    def __init__(self, config_path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    # General configurations
    def get_limit_to_one_page(self):
        return self.config.getboolean("general", "limit_to_one_page", fallback=True)
    
    def get_scrape_full_job_pages(self):
        return self.config.getboolean("general", "scrape_full_job_pages", fallback=False)
    
    def get_save_output_locally(self):
        return self.config.getboolean("general", "save_output_locally", fallback=True)
    
    def get_output_directory(self):
        return self.config.get("general", "output_directory", fallback="out")
    
    # Connection configurations
    def get_remote_storage_connection_string(self):
        return self.config.get("connection", "remote_storage_connection_string", fallback=None)
    
    # Logger configurations
    def get_capture_level(self):
        return self.config.get("logger", "capture_level", fallback="DEBUG")

    def get_console_level(self):
        return self.config.get("logger", "console_level", fallback="INFO")

    def get_file_level(self):
        return self.config.get("logger", "file_level", fallback="DEBUG")
    
    # Request configurations
    def get_delay_min(self):
        return self.config.getint("requests", "delay_min", fallback=1)

    def get_delay_max(self):
        return self.config.getint("requests", "delay_max", fallback=3)

    def get_sleep_time(self):
        return self.config.getint("requests", "sleep_time", fallback=5)

    def get_retries(self):
        return self.config.getint("requests", "retries", fallback=1)

    # URL Builder configurations
    def get_base_url(self):
        return self.config.get("url", "base_url", fallback="https://www.jobs.cz/prace/")

    def get_general_scrape_url(self):
        return self.config.get("url", "general_scrape_url", fallback="is-it-vyvoj-aplikaci-a-systemu/")

    def get_location(self):
        return self.config.get("url", "location", fallback="praha/")

    def get_radius(self):
        return self.config.get("url", "radius", fallback="0")

    def get_date_range(self):
        return self.config.get("url", "date_range", fallback="24h")
    
    def get_large_page_number(self):
        return self.config.getint("url", "large_page_number", fallback=1000)

    # Binary Search configurations
    def get_salary_start(self):
        return self.config.getint("binary_search", "salary_start", fallback=5000)

    def get_salary_end(self):
        return self.config.getint("binary_search", "salary_end", fallback=200000)

    def get_salary_step(self):
        return self.config.getint("binary_search", "salary_step", fallback=5000)