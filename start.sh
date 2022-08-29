#!/usr/bin/env bash

grep -q ultrasecretkey /etc/searxng/settings.yml && sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
su searxng -c "uwsgi --master --http-socket 8888 /usr/local/searxng/dockerfiles/uwsgi.ini"
