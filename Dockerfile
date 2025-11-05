############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
#FROM debian:bullseye-slim
FROM debian:bullseye

# File Author / Maintainer
LABEL image.author="andy.shepard@runbox.com"

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    iputils-ping \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/smart-home/app/requirements.txt
RUN pip install -r /var/www/smart-home/app/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./smart-home.conf /etc/apache2/sites-available/smart-home.conf
# Copy over the wsgi file, run.py and the app
COPY ./ /var/www/smart-home/

RUN a2dissite 000-default.conf
RUN a2ensite smart-home.conf
RUN a2enmod headers

# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80

WORKDIR /var/www/smart-home

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
