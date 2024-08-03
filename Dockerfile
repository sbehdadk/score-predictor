FROM python:3.10-slim

# Create a new user and group before any operations
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

WORKDIR /app

# Install required packages and distutils
COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y python3-distutils nginx && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application files
COPY . /app

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration files
COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Ensure nginx.conf and other config files have correct permissions
RUN chown -R root:root /etc/nginx && \
    chmod -R 644 /etc/nginx/nginx.conf

# Create necessary directories with the right permissions
RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run \
    /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi /var/lib/nginx/uwsgi /var/lib/nginx/scgi && \
    chown -R appuser:appgroup /var/lib/nginx /var/cache/nginx /var/run /run && \
    chmod -R 755 /var/lib/nginx /var/cache/nginx /var/run /run

# Set appropriate permissions for the Nginx log directory
RUN chown -R nginx:adm /var/log/nginx && \
    chmod -R 755 /var/log/nginx

# Ensure appuser has write permissions for /var/log
RUN chown -R appuser:appgroup /var/log

# Create a directory for application logs and ensure appuser owns it
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs

# Create a shell script to run both FastAPI and Streamlit with debug info
RUN echo "#!/bin/bash\n\
    echo 'Starting FastAPI...'\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
    sleep 5\n\
    echo 'Starting Streamlit...'\n\
    streamlit run streamlit.py --server.port 8501 --server.address 0.0.0.0 &\n\
    sleep 5\n\
    echo 'Starting Nginx...'\n\
    nginx -g 'daemon off;'\n" > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Change ownership of the /app directory to appuser
RUN chown -R appuser:appgroup /app

# Expose the necessary ports
EXPOSE 80
EXPOSE 8000
EXPOSE 8501

# Switch to the new user for running application processes
USER appuser

# Command to run the shell script
CMD ["sh", "/app/start.sh"]
