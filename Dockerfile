FROM python:3.10-slim

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y python3-distutils nginx && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN rm /etc/nginx/sites-enabled/default
COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN chown -R root:root /etc/nginx && \
    chmod -R 644 /etc/nginx/nginx.conf /etc/nginx/conf.d/app.conf

RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi /var/lib/nginx/scgi /var/lib/nginx/uwsgi && \
    chown -R appuser:appgroup /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    chmod -R 755 /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run

RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs && \
    chmod -R 755 /app/logs

RUN touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown appuser:appgroup /var/log/nginx/access.log /var/log/nginx/error.log

RUN echo "#!/bin/bash\n\
    echo 'Starting FastAPI...'\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
    sleep 5\n\
    echo 'Starting Streamlit...'\n\
    streamlit run streamlit.py --server.port 8501 --server.address 0.0.0.0 &\n\
    sleep 5\n\
    echo 'Starting Nginx...'\n\
    nginx -g 'daemon off;'\n" > /app/start.sh

RUN chmod +x /app/start.sh
RUN chown -R appuser:appgroup /app

EXPOSE 8080 8000 8501

USER appuser

CMD ["sh", "/app/start.sh"]
