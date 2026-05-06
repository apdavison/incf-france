#
# Build an image for deploying the INCF France website
#
# To build the image:
#  docker build -t neuroinf .
#
# To run the application in production:
#  docker run -d -p 443 -v /etc/letsencrypt:/etc/letsencrypt neuroinf
# To run the application locally:
#  docker run -d -p 443 -v `pwd`/letsencrypt:/etc/letsencrypt neuroinf
#
# To find out which port to access on the host machine, run "docker ps"
#
# To check the content of the docker container:
#  docker run -it neuroinf /bin/bash

FROM debian:stretch-slim
MAINTAINER Andrew Davison <andrew.davison@unic.cnrs-gif.fr>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing; apt-get -y -q install python3-dev python3-setuptools sqlite3 python3-psycopg2 git supervisor build-essential nginx-extras python3-pip wget apt-transport-https
RUN wget -q https://artifacts.elastic.co/GPG-KEY-elasticsearch; apt-key add GPG-KEY-elasticsearch
RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list
RUN apt-get update --fix-missing; apt-get -y -q install filebeat
RUN pip3 install --upgrade pip
RUN unset DEBIAN_FRONTEND

RUN pip3 install uwsgi

ENV SITEDIR /home/docker/site

COPY requirements.txt $SITEDIR/requirements.txt

WORKDIR /home/docker
RUN pip3 install -r $SITEDIR/requirements.txt
ENV PYTHONPATH  /home/docker:/home/docker/site:/usr/local/lib/python3.5/dist-packages:/usr/lib/python3.5/dist-packages

COPY node_modules $SITEDIR/node_modules
COPY manage.py $SITEDIR/manage.py
COPY app $SITEDIR/app
COPY media $SITEDIR/media
COPY incf_france $SITEDIR/incf_france
COPY directory /home/docker/directory
COPY templates $SITEDIR/templates

WORKDIR $SITEDIR
RUN if [ -f $SITEDIR/db.sqlite3 ]; then rm $SITEDIR/db.sqlite3; fi
RUN python3 manage.py check
RUN python3 manage.py collectstatic --noinput
RUN unset PYTHONPATH

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY deployment $SITEDIR/deployment
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s $SITEDIR/deployment/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s $SITEDIR/deployment/supervisor-app.conf /etc/supervisor/conf.d/
RUN mv /etc/filebeat/filebeat.yml /etc/filebeat/filebeat.yml.orig
RUN ln -s $SITEDIR/deployment/filebeat.yml /etc/filebeat/filebeat.yml
RUN mkdir -p /etc/elk-certs
RUN ln -s $SITEDIR/deployment/elk-ssl.crt /etc/elk-certs/elk-ssl.crt
RUN ln -s $SITEDIR/deployment/elk-ssl.key /etc/elk-certs/elk-ssl.key
#RUN ln -sf /dev/stdout /var/log/nginx/access.log
#RUN ln -sf /dev/stderr /var/log/nginx/error.log

COPY data_all.json $SITEDIR/initial_data.json

EXPOSE 80 443
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]

