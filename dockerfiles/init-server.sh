#!/bin/sh
cp /var/frea/dockerfiles/uwsgi.ini /etc/searxng/uwsgi.ini

if [ ! -e /etc/searxng/settings.yml ]; then
  cp /var/frea/utils/templates/etc/searxng/settings.yml /etc/searxng/settings.yml
fi

if grep -q ultrasecretkey /etc/searxng/settings.yml; then
  sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
fi

su frea -c "uwsgi --master --http-socket 0.0.0.0:8888 /etc/searxng/uwsgi.ini"

