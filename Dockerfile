# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install forego to manage multiple processes
RUN apt-get update && apt-get install -y forego

# Create a Procfile to start both FastAPI and Streamlit
RUN echo "web: sh -c 'uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit.py --server.port 8501'" > Procfile

# Expose the necessary ports
EXPOSE 8000 8501

# Command to run the application
CMD ["forego", "start", "-f", "Procfile"]
