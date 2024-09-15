import time
import requests
import random
from threading import Lock

class MaxRetriesExceeded(Exception):
    pass

class NetworkManager:
    def __init__(self, logger, config_reader):
        self.logger = logger
        self.config_reader = config_reader
        self._last_request_time = 0
        self._request_lock = Lock()

        self.delay_min = self.config_reader.get_delay_min()
        self.delay_max = self.config_reader.get_delay_max()
        self.sleep_time = self.config_reader.get_sleep_time()
        self.retries = self.config_reader.get_retries()
        
        self.slack_hook_url = self.config_reader.get_slack_hook_url()

    def throttled_request(self, url):
        with self._request_lock:  # Single thread executes this block at a time
            current_time = time.time()
            time_since_last_request = current_time - self._last_request_time

            # Generate a random delay based on config values
            delay = random.uniform(self.delay_min, self.delay_max)

            if time_since_last_request < delay:
                time.sleep(delay - time_since_last_request)

            for attempt in range(self.retries):
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        self.logger.request_ok(response.status_code, url)
                        self._last_request_time = time.time()
                        return response
                    else:
                        self.logger.request_failed_will_retry(url, response.status_code)
                        time.sleep(self.sleep_time)
                except requests.exceptions.Timeout:
                    self.logger.request_timeout_will_retry(url, attempt, self.retries)
                    time.sleep(self.sleep_time)
                except requests.exceptions.RequestException as e:
                    self.logger.request_error(e)
                    raise
            self.logger.request_failed_retries(url, self.retries)
            raise MaxRetriesExceeded(f"Failed to retrieve data from {url} after {self.retries} attempts.")

    # Slack notifications

    def send_slack_finish_notif(self, time_stamp):
        message = f"{time_stamp}: 🤖 Scraping finished"
        self._send_slack_notif(message)

    def send_slack_error_notif(self, time_stamp, error_message):
        message = f"{time_stamp}: {error_message}"
        self._send_slack_notif(message)

    def _send_slack_notif(self, message):
        if self.slack_hook_url is None:
            self.logger.no_slack_webhook()
            return
        payload = {"text": message}
        try:
            response = requests.post(self.slack_hook_url, json=payload)
            if response.status_code != 200:
                self.logger.slack_request_error(response.status_code)
        except requests.exceptions.RequestException as e:
            self.logger.slack_request_error(e)
