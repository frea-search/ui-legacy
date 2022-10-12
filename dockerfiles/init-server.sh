#!/bin/sh
cp /usr/local/searxng/dockerfiles/uwsgi.ini /etc/searxng/uwsgi.ini

if [ ! -e /etc/searxng/settings.yml ]; then
  cp /usr/local/searxng/utils/templates/etc/searxng/settings.yml /etc/searxng/settings.yml
fi

if grep -q ultrasecretkey /etc/searxng/settings.yml; then
  sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
fi

su searxng -c "uwsgi --master --http-socket 0.0.0.0:8888 /etc/searxng/uwsgi.ini"

