#!/usr/bin/env bash

f grep -q ultrasecretkey /etc/searxng/settings.yml; then
    sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
fi

uwsgi --master --http-socket 8888 /usr/local/searxng/dockerfiles/uwsgi.ini