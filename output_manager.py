import os
import json
from azure.storage.blob import BlobServiceClient

class OutPutManager:
    def __init__(self, logger, timestamp, config_reader):
        self.logger = logger
        self.timestamp = timestamp
        self.config_reader = config_reader
        self.save_locally = self.config_reader.get_save_output_locally_instead_of_cloud()
        self.output_dir = self.config_reader.get_output_directory()
        
        # Get Azure Blob Storage connection details
        self.connection_string = self.config_reader.get_azure_blob_connection_string()
        self.container_name = self.config_reader.get_blob_container_name()
        
        if self.save_locally:
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize BlobServiceClient if connection string is provided.
        if self.connection_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                self.logger.blob_client_init_successfull()
            except Exception as e:
                self.logger.failed_blob_init(e)
                self.blob_service_client = None
        else:
            self.logger.failed_blob_init_no_string()
            self.blob_service_client = None

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
        filename = f"jobs_{self.timestamp}_{page_number}.json"
        output_file = os.path.join(self.output_dir, filename)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=4)
            self.logger.saved_jobs(output_file)
        except Exception as e:
            self.logger.failed_to_save_jobs_locally()

    def _save_logs_locally(self, logs):
        log_filename = f"{self.timestamp}.log"
        log_file_path = os.path.join(self.output_dir, log_filename)
        try:
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(logs)
        except Exception as e:
            self.logger.failed_to_save_logs_locally()

    def _save_jobs_to_cloud(self, jobs, page_number):
        if not self.blob_service_client:
            self.logger.missing_connection_string()
            return
        
        filename = f"jobs_{self.timestamp}_{page_number}.json"
        try:
            # Convert jobs to JSON string
            jobs_json = json.dumps(jobs, ensure_ascii=False, indent=4)
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)
            blob_client.upload_blob(jobs_json)
            self.logger.upload_successfull(filename)
        except Exception as e:
            self.logger.failed_job_upload(e)

    def _save_logs_to_cloud(self, logs):
        if not self.blob_service_client:
            self.logger.missing_connection_string()
            return
        
        log_filename = f"{self.timestamp}.log"
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=log_filename)
            blob_client.upload_blob(logs)
            self.logger.upload_successfull(log_filename)
        except Exception as e:
            self.logger.failed_log_upload(e)
