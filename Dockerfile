FROM ubuntu:18.04

RUN apt-get clean && apt-get update && apt-get install -y \
    vim \
    curl \
    wget \
    libpq-dev \
    supervisor \
    python3-dev \
    locales \
    python3-pip npm \
    qrencode \
    postgresql-client pgtop \
    nginx

RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN pip3 install django==2.0.2 gunicorn requests django-rest-framework

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/log/nginx/;
RUN mkdir -p /var/cdn/files;
RUN mkdir -p /var/cdn/files-master;
RUN mkdir -p /var/log/cdn/;

RUN echo 'testtest' > /var/cdn/files-master/lolkek.png;

WORKDIR /opt/cdn_node
VOLUME /var/cdn/

EXPOSE 8002
EXPOSE 8001
EXPOSE 8000

COPY . /opt/cdn_node
WORKDIR /opt/cdn_node

RUN cp project/local_settings.sample.py project/local_settings.py

COPY conf/supervisord.conf /etc/supervisor/supervisord.conf
COPY conf/prod.conf /etc/supervisor/conf.d/cdn_node.conf
COPY conf/nginx.conf /etc/nginx/nginx.conf

VOLUME /data/
VOLUME /conf/
VOLUME /static/
VOLUME /media/

CMD test "$(ls /conf/local_settings.py)" || cp project/local_settings.sample.py /conf/local_settings.py; \
    rm project/local_settings.py;  ln -s /conf/local_settings.py project/local_settings.py; \
    python3 ./manage.py migrate; \
    /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon