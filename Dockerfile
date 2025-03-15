# Use an official Python runtime as a parent image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /mkapp

# Copy the current directory contents into the container
COPY . /mkapp

# Install any needed packages specified in requirements.txt and collect static files
RUN pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for AWS App Runner
ENV PORT=8080

# Run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]