FROM python:3.10-slim

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y python3-distutils nginx && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN rm /etc/nginx/sites-enabled/default

COPY nginx/app.conf /etc/nginx/conf.d/
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN chown -R root:root /etc/nginx && \
    chmod -R 644 /etc/nginx/nginx.conf

RUN mkdir -p /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run /var/lib/nginx/body && \
    chown -R appuser:appgroup /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run && \
    chmod -R 755 /var/lib/nginx /var/log/nginx /var/cache/nginx /var/run /run

RUN chown -R appuser:appgroup /var/log

RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app/logs

RUN echo "#!/bin/bash\n\
    echo 'Starting FastAPI...'\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
    sleep 5\n\
    echo 'Starting Streamlit...'\n\
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &\n\
    sleep 5\n\
    echo 'Starting Nginx...'\n\
    nginx -g 'daemon off;'\n" > /app/start.sh

RUN chmod +x /app/start.sh

RUN chown -R appuser:appgroup /app

EXPOSE 80
EXPOSE 8000
EXPOSE 8501

USER appuser

CMD ["sh", "/app/start.sh"]
