import json
import os

class FileManager:
    def __init__(self, logger, timestamp, config_reader):
        self.logger = logger
        self.timestamp = timestamp
        self.config_reader = config_reader
        
        self.output_dir = self.config_reader.get_output_directory()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_page_jobs(self, jobs, page_number):
        filename = f"jobs_{self.timestamp}_page_{page_number}.json"
        output_file = os.path.join(self.output_dir, filename)
        
        # Save the JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=4)
        self.logger.saved_jobs(output_file)
