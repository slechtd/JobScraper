from threading import Lock
from enum import Enum
from output_manager import OutPutManager
from datetime import datetime

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
        self.logs = []
        self.output_manager = OutPutManager(self, self.time_stamp, self.config_reader)

    def _log(self, lvl: LogLevel, msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {lvl.name} - {msg}"
        print(log_entry)
        with self._lock:
            self.logs.append(log_entry)
    
    def flush_logs(self):
        self.output_manager.save_logs(self.get_logs())
        self._clear_logs()
        self._scraping_completed()

    def get_logs(self):
        with self._lock:
            return "\n".join(self.logs)

    def _clear_logs(self):
        with self._lock:
            self.logs.clear()

    # Errors
    def error_general(self, error_message):
        self._log(LogLevel.ERROR, f"An error occurred: {error_message}")

    def error_scraping_page(self, page_number, error_message):
        self._log(LogLevel.ERROR, f"An error occurred while scraping page {page_number}: {error_message}")

    def error_initialising_job_listing(self, position, error_message):
        self._log(LogLevel.ERROR, f"Error initializing JobListing at position {position}: {error_message}")

    def error_salary_determination(self, error_message):
        self._log(LogLevel.ERROR, f"An error occurred during salary determination: {error_message}")

    def failed_to_save_jobs_locally(self, error_message):
        self._log(LogLevel.ERROR, f"Failed to save jobs .json file locally: {error_message}")

    def failed_to_save_logs_locally(self, error_message):
        self._log(LogLevel.ERROR, f"Failed to save logs .log file locally: {error_message}")

    def missing_connection_string(self):
        self._log(LogLevel.ERROR, f"Missing connection string.")

    def failed_blob_init_no_string(self):
        self._log(LogLevel.ERROR, f"Failed to initialise BlobServiceClient: No connection string.")

    def failed_blob_init(self, error_message):
        self._log(LogLevel.ERROR, f"Failed to initialise BlobServiceClient: {error_message}")

    def failed_job_upload(self, error_message):
        self._log(LogLevel.ERROR, f"Failed to upload jobs to cloud: {error_message}")

    def failed_log_upload(self, error_message):
        self._log(LogLevel.ERROR, f"Failed to upload logs to cloud: {error_message}")

    # Cloud
    def blob_client_init_successfull(self):
        self._log(LogLevel.INFO, f"SUCCESSFULLY initialised BlobServiceClient")

    def upload_successfull(self, filename):
        self._log(LogLevel.INFO, f"Successfully uploaded {filename} to cloud storage.")

    # Scraping Process
    def pages_could_not_get_total(self):
        self._log(LogLevel.WARNING, "FAILED to get total number of pages, defaulting to 1.")

    def scraping_page(self, page_number, total_pages):
        self._log(LogLevel.INFO, f"SCRAPING PAGE {page_number}/{total_pages}")

    def number_of_listings_on_page(self, total_listings, page_number):
        self._log(LogLevel.INFO, f"{total_listings} job listings found on page {page_number}.")

    def _scraping_completed(self):
        self._log(LogLevel.INFO, "SCRAPING COMPLETED.")

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