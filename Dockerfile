FROM ubuntu:18.04

RUN apt-get clean && apt-get update && apt-get install -y \
    supervisor \
    python3-dev \
    locales \
    python3-pip \
    nginx

ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/app
WORKDIR /opt/app

ADD requirements.txt /opt/app
RUN pip3 install -r /opt/app/requirements.txt

ADD webserver.py /opt/app
ADD clearing.py /opt/app

ADD supervisor/supervisord.conf /etc/supervisor/supervisord.conf
ADD supervisor/prod.conf /etc/supervisor/conf.d/app.conf
ADD nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon