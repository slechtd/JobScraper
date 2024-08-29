# Start from a minimal Python image
FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright with only Chromium
RUN apt-get update && apt-get install -y wget libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libxcomposite1 libxrandr2 libxdamage1 libpango1.0-0 libxcursor1 fonts-liberation libappindicator3-1 libdbus-glib-1-2 && rm -rf /var/lib/apt/lists/* \
    && pip install playwright \
    && playwright install chromium

# Copy the application code
COPY . /app

# Command to run your application
CMD ["python", "main.py"]
