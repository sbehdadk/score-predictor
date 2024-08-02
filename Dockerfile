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

# Create a shell script to run both FastAPI and Streamlit
RUN echo "#!/bin/bash\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
    streamlit run streamlit.py --server.port 8501\n" > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Expose the necessary ports
EXPOSE 8000 8501

# Command to run the shell script
CMD ["/app/start.sh"]
