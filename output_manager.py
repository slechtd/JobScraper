import os
import json

class OutPutManager:
    def __init__(self, logger, timestamp, config_reader):
        self.logger = logger
        self.timestamp = timestamp
        self.config_reader = config_reader
        self.save_locally = self.config_reader.get_save_output_locally()
        self.output_dir = self.config_reader.get_output_directory()

        if self.save_locally:
            os.makedirs(self.output_dir, exist_ok=True)

    def save_page_jobs(self, jobs, page_number):
        if self.save_locally:
            self._save_jobs_locally(jobs, page_number)
        else:
            self._save_jobs_to_cloud(jobs, page_number)

    def save_logs(self, logs):
        if self.save_locally:
            self._save_logs_locally(logs)
        else:
            self._save_logs_to_cloud(logs)

    def _save_jobs_locally(self, jobs, page_number):
        filename = f"jobs_{self.timestamp}_page_{page_number}.json"
        output_file = os.path.join(self.output_dir, filename)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=4)
            self.logger.saved_jobs(output_file)
        except Exception as e:
            self.logger.error_general(f"Failed to save jobs locally: {e}")

    def _save_logs_locally(self, logs):
        log_filename = f"{self.timestamp}.log"
        log_file_path = os.path.join(self.output_dir, log_filename)
        try:
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(logs)  # Write the collected logs to the file
        except Exception as e:
            self.logger.error_general(f"Failed to save logs locally: {e}")

    def _save_jobs_to_cloud(self, jobs, page_number):
        # Placeholder for future cloud implementation
        print("Saving jobs to cloud...")

    def _save_logs_to_cloud(self, logs):
        # Placeholder for future cloud implementation
        print("Saving logs to cloud...")
