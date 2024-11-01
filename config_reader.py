import configparser
import os

class ConfigReader:
    def __init__(self, config_path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    # General configurations
    def get_limit_to_one_page(self):
        return self.config.getboolean("general", "limit_to_one_page", fallback=True)
    
    def get_scrape_detail_text(self):
        return self.config.getboolean("general", "scrape_full_job_pages", fallback=True)
    
    def get_save_output_locally_instead_of_cloud(self):
        return self.config.getboolean("general", "save_output_locally_instead_of_cloud", fallback=True)
    
    def get_output_directory(self):
        return self.config.get("general", "output_directory", fallback="_out")
    
    # Cloud connection configuration
    def get_azure_blob_connection_string(self):
        return os.getenv("AZURE_BLOB_CONNECTION_STRING", None)

    def get_job_container_name(self):
        return os.getenv("JOB_CONTAINER_NAME", None)
    
    def get_log_container_name(self):
        return os.getenv("LOG_CONTAINER_NAME", None)
    
    # Slack notification webhook
    def get_slack_hook_url(self):
        return os.getenv("SLACK_WEBHOOK", None)

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
