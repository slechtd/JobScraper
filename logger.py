import logging
from logging.handlers import RotatingFileHandler
from threading import Lock
from enum import Enum
import os
from datetime import datetime #remove?

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class Logger:
    def __init__(self, config_reader, time_stamp):
        self.config_reader = config_reader
        self.time_stamp = time_stamp
        self._lock = Lock()
        self._initialize_logger()

    def _initialize_logger(self):
        with self._lock:
            capture_level = self._get_log_level(self.config_reader.get_capture_level())
            file_level = self._get_log_level(self.config_reader.get_file_level())
            console_level = self._get_log_level(self.config_reader.get_console_level())

            logger = logging.getLogger("ApplicationLogger")
            logger.setLevel(capture_level)

            log_dir = self.config_reader.get_output_directory()
            os.makedirs(log_dir, exist_ok=True)

            # Use the injected time_stamp for the log file name
            log_file_name = f"{self.time_stamp}.log"
            log_file_path = os.path.join(log_dir, log_file_name)

            # File handler
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(file_level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(console_level)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            self._logger = logger

    def _get_log_level(self, level_str):
        # Convert string log level from config to logging module level, default to DEBUG.
        return getattr(logging, level_str.upper(), logging.DEBUG)

    def _log(self, lvl: LogLevel, msg: str):
        if lvl == LogLevel.DEBUG:
            self._logger.debug(msg)
        elif lvl == LogLevel.INFO:
            self._logger.info(msg)
        elif lvl == LogLevel.WARNING:
            self._logger.warning(msg)
        elif lvl == LogLevel.ERROR:
            self._logger.error(msg, exc_info=True)
        elif lvl == LogLevel.CRITICAL:
            self._logger.critical(msg, exc_info=True)

    # Errors
    def error_general(self, error_message):
        self._log(LogLevel.ERROR, f"An error occurred: {error_message}")

    def error_scraping_page(self, page_number, error_message):
        self._log(LogLevel.ERROR, f"An error occurred while scraping page {page_number}: {error_message}")

    def error_initialising_job_listing(self, position, error_message):
        self._log(LogLevel.WARNING, f"Error initializing JobListing at position {position}: {error_message}")

    def error_salary_determination(self, error_message):
        self._log(LogLevel.ERROR, f"An error occurred during salary determination: {error_message}")

    # Scraping Process
    def pages_could_not_get_total(self):
        self._log(LogLevel.WARNING, "FAILED to get total number of pages, defaulting to 1.")

    def scraping_page(self, page_number, total_pages):
        self._log(LogLevel.INFO, f"SCRAPING PAGE {page_number}/{total_pages}")

    def number_of_listings_on_page(self, total_listings, page_number):
        self._log(LogLevel.INFO, f"{total_listings} job listings found on page {page_number}.")

    def scraping_completed(self):
        self._log(LogLevel.INFO, "SCRAPING COMPLETED")

    def listing_initialised(self, job_id):
        self._log(LogLevel.DEBUG, f"JobListing: {job_id} initialized successfully.")

    def salary_determined(self, job_id, salary):
        self._log(LogLevel.INFO, f"Job {job_id}: DETERMINED SALARY: {salary}")

    def salary_determination_start(self, job_id):
        self._log(LogLevel.DEBUG, f"Job {job_id}: DETERMINING SALARY")

    def salary_cannot_determine(self, job_id, salary):
        self._log(LogLevel.INFO, f"Job {job_id}: not found with salary: {salary}. CANNOT DETERMINE SALARY.")

    def salary_binary_search_start(self, job_id, salary):
        self._log(LogLevel.DEBUG, f"Job {job_id}: found with salary {salary}. Starting binary search")

    def salary_binary_new_midpoint(self, job_id, mid):
        self._log(LogLevel.INFO, f"Job {job_id}: Checking adjusted mid-point salary: {mid}")

    def salary_found_with_midpoint(self, job_id, mid):
        self._log(LogLevel.DEBUG, f"Job {job_id}: Job found with salary {mid}. Moving lower bound up.")

    def salary_not_found_with_midpoint(self, job_id, mid):
        self._log(LogLevel.DEBUG, f"Job {job_id}: Job not found with salary {mid}. Moving upper bound down.")

    # Networking
    def request_ok(self, status_code, url):
        self._log(LogLevel.DEBUG, f"Request successful: {status_code} - {url}")

    def request_error(self, error_message):
        self._log(LogLevel.CRITICAL, f"AN ERROR OCCURRED: {error_message}")

    def request_failed_will_retry(self, url, status_code):
        self._log(LogLevel.DEBUG, f"Request to {url} failed with status code {status_code}. Retrying in 5 seconds...")

    def request_timeout_will_retry(self, url, attempt, retries):
        self._log(LogLevel.CRITICAL, f"TIMEOUT occurred for {url}. Retrying ({attempt + 1}/{retries})...")

    def request_failed_retries(self, url, retries):
        self._log(LogLevel.CRITICAL, f"FAILED TO RETRIEVE DATA FROM: {url} AFTER {retries} ATTEMPTS.")

    # Output
    def saved_jobs(self, file):
        self._log(LogLevel.INFO, f"Saved jobs to {file}")