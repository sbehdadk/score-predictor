FROM python:3.10-slim

# Create a new user and group
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

# Set the working directory
WORKDIR /app

# Install required packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application files
COPY . /app

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration files
COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Create necessary directories with the right permissions
RUN mkdir -p /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi /var/lib/nginx/uwsgi /var/lib/nginx/scgi /var/cache/nginx /var/run /var/log/nginx /etc/nginx && \
    chown -R appuser:appgroup /var/lib/nginx /var/log/nginx /var/run /etc/nginx /var/cache/nginx


# Create a shell script to run both FastAPI and Streamlit
RUN echo "#!/bin/bash\n\
    uvicorn main:app --host 127.0.0.1 --port 8000 &\n\
    streamlit run streamlit.py --server.port 8501 --server.address 127.0.0.1 &\n\
    nginx -g 'daemon off;'\n" > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Change ownership of the /app directory to appuser
RUN chown -R appuser:appgroup /app

# Switch to the new user
USER appuser

# Expose the necessary ports
EXPOSE 80

# Command to run the shell script
CMD ["/app/start.sh"]
