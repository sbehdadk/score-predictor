#--- PREREQS:  
#   - https://huggingface.co/spaces/radames/nginx-gradio-reverse-proxy/tree/main
#   - https://muellerzr.github.io/blog/huggingface_docker.html
#   - https://www.tecmint.com/enable-nginx-status-page/

#--- USAGE:
#--- to build/rebuild the image; make sure you stop and remove the container if you are replacing/upgrading; or change the version tag# from 0.0.1
#--- to tag the image prior to push to DockerHub; docker login and then register user/image:tag
#--- to push this image to DockerHub, example based on the repo: kidcoconut73/<img>

#   docker build -t img_nginx_hugspace:0.0.1 .
#   docker create -it -p 49130:39130 --name ctr_nginx_hugspace img_nginx_hugspace:0.0.1
#   docker start -it ctr_nginx_hugspace

#   docker run -it -p 7860:7860 -p 49131:39131 -p 49132:39132 --name ctr_nginx_templ img_nginx_templ:0.0.1

#   docker push kidcoconut73/<img:tag>


#--- use a base image of python
FROM python:3.9-slim

# Install nginx and give permissions to 'pn'
# See https://www.rockyourcode.com/run-docker-nginx-as-non-root-user/
USER root

# Update package list and install nginx
RUN apt-get -y update && apt-get -y install nginx

# Create necessary directories and set permissions
RUN mkdir -p /var/cache/nginx \
    /var/log/nginx \
    /var/lib/nginx
RUN touch /var/run/nginx.pid

# Create a user group and a user
RUN groupadd user
RUN useradd -d /home/user -ms /bin/bash -g user -G user -p user user
RUN chown -R user:user /var/cache/nginx \
    /var/log/nginx \
    /var/lib/nginx \
    /var/run/nginx.pid

# Update nginx config; establish routes/proxy pass; remove user directive
COPY ./nginx/etc.nginx.confd_default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/etc.nginx_nginx.conf /etc/nginx/nginx.conf
#COPY ./nginx/etc.nginx.sites-available.default /etc/nginx/sites-available/default

# Switch to the user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set docker image working directory to /app
RUN mkdir $HOME/app
WORKDIR $HOME/app

# Install dependencies
COPY --chown=user ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Explicitly install Streamlit and verify version
RUN pip install --no-cache-dir streamlit==1.12.0
RUN streamlit --version

# Copy necessary files
COPY --chown=user ./_env_config/stg_dev/utl_dkr_preRun.sh ./scripts/docker/
COPY --chown=user ./fastapi ./fastapi
COPY --chown=user ./streamlit ./streamlit
COPY --chown=user ./env.py ./env.py
COPY --chown=user ./src ./src
COPY --chown=user ./tests ./tests

# Give execute permissions to the preRun script
RUN chmod +x ./scripts/docker/utl_dkr_preRun.sh

# Set the PYTHONPATH to include the app directory
ENV PYTHONPATH="/home/user/app"

# Expose necessary ports
EXPOSE 7860
EXPOSE 49131
EXPOSE 49132

# Establish environment prereqs
ENTRYPOINT ["./scripts/docker/utl_dkr_preRun.sh"]
