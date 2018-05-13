mkdir -p /var/log/nginx/;

apt-get update -y && \
    apt-get install -y wget && \
    /bin/bash -c "envsubst < /etc/cdn-node/nginx.conf > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"