# Use a standard Python base image instead of relying on AWS's custom image
FROM python:3.11-slim

# Set working directory
WORKDIR /app/muna_kalati

# Install pip and other dependencies
RUN apt-get update && apt-get install -y python3-pip

# Copy requirements file
COPY muna_kalati/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY muna_kalati/ .

# Expose port (default for App Runner is 8080, but you can configure it)
EXPOSE 8000

# Start application
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000