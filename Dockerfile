# Use official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app


# Copy the rest of the application code
COPY . /app

# Copy requirements file and install dependencies

RUN pip install --no-cache-dir -r requirements.txt


# Expose the necessary port
EXPOSE 8080

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
