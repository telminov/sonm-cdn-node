FROM ubuntu:18.04

RUN apt-get clean && apt-get update && apt-get install -y wget software-properties-common
RUN wget -qO - https://openresty.org/package/pubkey.gpg | apt-key add -
RUN add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"

RUN apt-get install -y \
    supervisor \
    python3-dev \
    locales \
    python3-pip \
    nginx libnginx-mod-http-lua \
    openresty



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

ENV LUA_PATH /etc/nginx/nginx-lua-prometheus
ADD nginx-lua-prometheus /etc/nginx/nginx-lua-prometheus


EXPOSE 80

CMD /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon