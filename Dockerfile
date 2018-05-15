FROM ubuntu:18.04
EXPOSE 8080

RUN apt-get clean && apt-get update && apt-get install -y \
    supervisor \
    python3-dev \
    locales \
    python3-pip \
    nginx

RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN pip3 install django==2.0.5 \
                 gunicorn==19.8.1 \
                 requests==2.18.4 \
                 djangorestframework==3.8.2

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/cdn/asset /var/cdn/logs

COPY . /opt/cdn_node
WORKDIR /opt/cdn_node

RUN cp project/local_settings.sample.py project/local_settings.py

COPY conf/supervisord.conf /etc/supervisor/supervisord.conf
COPY conf/prod.conf /etc/supervisor/conf.d/cdn_node.conf
COPY conf/nginx.conf /etc/nginx/nginx.conf

CMD test "$(ls /conf/local_settings.py)" || cp project/local_settings.sample.py /conf/local_settings.py; \
    rm project/local_settings.py;  ln -s /conf/local_settings.py project/local_settings.py; \
    python3 ./manage.py migrate; \
    /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon