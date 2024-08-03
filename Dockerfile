FROM python:3.10-slim

# Create a non-root user
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies and Nginx
RUN apt-get update && \
    apt-get install -y python3-distutils nginx && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Ensure directories exist and set permissions for Nginx and application files
RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    chown -R appuser:appgroup /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    chmod -R 755 /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs && \
    chmod -R 755 /app/logs && \
    touch /app/logs/fastapi.log /app/logs/streamlit.log /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown appuser:appgroup /app/logs/fastapi.log /app/logs/streamlit.log /var/log/nginx/access.log /var/log/nginx/error.log

# Create the start script
RUN echo "#!/bin/bash\n\
    echo 'Starting FastAPI...'\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &> /app/logs/fastapi.log &\n\
    sleep 5\n\
    echo 'Starting Streamlit...'\n\
    streamlit run streamlit.py --server.port 8501 --server.address 0.0.0.0 &> /app/logs/streamlit.log &\n\
    sleep 5\n\
    echo 'Starting Nginx...'\n\
    nginx -g 'daemon off;'\n" > /app/start.sh

# Make the start script executable
RUN chmod +x /app/start.sh
RUN chown -R appuser:appgroup /app

# Expose necessary ports
EXPOSE 8080 8000 8501

# Switch to the non-root user
USER appuser

# Start the services
CMD ["sh", "/app/start.sh"]
