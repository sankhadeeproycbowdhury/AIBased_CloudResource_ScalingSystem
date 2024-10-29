# # Use an official Python runtime as the base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /Amity_Hackathon

# # Copy the current directory contents into the container at /Amity_Hackathon
# COPY . .

# # Install any necessary dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the port the app runs on
# EXPOSE 65432

# # Run the application
# CMD ["python", "server.py"]  # Updated CMD to use JSON format



# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 65432

# Define environment variable for the database
ENV DATABASE_PATH /app/data.db

# Run the Python application when the container starts
CMD ["python", "server.py"]

