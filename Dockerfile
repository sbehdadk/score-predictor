# Base image for Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# Install Streamlit, FastAPI, and Nginx
RUN pip install streamlit fastapi uvicorn
RUN apt-get update && apt-get install -y nginx

# Copy Nginx configuration files
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/app.conf /etc/nginx/conf.d/default.conf

# Expose ports for FastAPI, Streamlit, and Nginx
EXPOSE 8000
EXPOSE 8501
EXPOSE 8080

# Run Nginx, FastAPI, and Streamlit
CMD service nginx start && \
    uvicorn main:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit.py --server.port 8501
