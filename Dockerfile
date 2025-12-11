# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Expose the port Django will run on
EXPOSE 8080

# Command to run the Django development server
CMD ["python", "/app/app/manage.py", "runserver", "0.0.0.0:8080"]