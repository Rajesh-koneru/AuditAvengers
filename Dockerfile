# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /AAapp

# Copy the requirements.txt file to the container
COPY requirements.txt /AAapp/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /AAapp

# Expose port 5000 to allow access to the Flask app
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "run.py"]
