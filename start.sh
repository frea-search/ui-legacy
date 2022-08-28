#!/usr/bin/env bash

sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
uwsgi --master --http-socket 8888 /usr/local/searxng/dockerfiles/uwsgi.ini