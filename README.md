# Job Scraper

This is a Python-based web scraping application designed to extract job listings from a job website, along with detailed information such as job titles, companies, salaries, and other metadata. The application includes built-in throttling, retry mechanisms, and configurable settings to ensure efficient and reliable scraping.

## Features
- **Throttled Web Scraping**: Ensures polite scraping by adding configurable delays between requests to avoid overwhelming the target website.
- **Binary Search Salary Estimation**: Estimates the maximum salary for a job listing by performing a binary search over filtered search results.
- **Configurable via `config.ini`**: Almost all aspects of the scraper, including network delays, URL parameters, and logging behavior, can be configured in a `config.ini` file.
- **Data Persistence**: Scraped job listings are saved as JSON files for further analysis or processing.
- **Detailed Logging**: Logs the progress and errors of the scraping process, providing insights into its operations.
