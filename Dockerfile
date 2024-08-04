FROM python:3.10-slim

# Create a new user and group for non-root operations
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

# Set the working directory
WORKDIR /app

# Install required packages and dependencies
COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y python3-distutils nginx && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration files
COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Ensure Nginx configuration files have correct permissions
RUN chown -R root:root /etc/nginx && \
    chmod -R 644 /etc/nginx/nginx.conf /etc/nginx/conf.d/app.conf

# Create necessary directories for Nginx and set correct permissions
RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi /var/lib/nginx/scgi /var/lib/nginx/uwsgi && \
    chown -R appuser:appgroup /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    chmod -R 755 /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run

# Create a directory for application logs and set permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs && \
    chmod -R 755 /app/logs

# Ensure log files have correct permissions
RUN touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown appuser:appgroup /var/log/nginx/access.log /var/log/nginx/error.log

# Create a shell script to run FastAPI, Streamlit, and Nginx
RUN echo "#!/bin/bash\n\
    service nginx start \
    echo 'Starting FastAPI...'\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
    sleep 5\n\
    echo 'Starting Streamlit...'\n\
    streamlit run app_streamlit.py --server.port 8501 --server.address 0.0.0.0 &\n\
    sleep 5\n" > /app/start.sh



# echo 'Starting Nginx...'\n\
# nginx -g 'daemon off;'\n
# Make the script executable
RUN chmod +x /app/start.sh

# Change ownership of the /app directory to appuser
RUN chown -R appuser:appgroup /app

# Expose ports
EXPOSE 8080 8000 8501

# Switch to non-root user
USER appuser

# Start the services
CMD ["sh", "/app/start.sh"]