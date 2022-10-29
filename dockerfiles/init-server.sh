#!/bin/sh
export SEARXNG_SETTINGS_PATH=/etc/frea/settings.yml
export SEARXNG_SECRET=$(openssl rand -hex 16)

cp /var/frea/dockerfiles/uwsgi.ini /etc/searxng/uwsgi.ini

if [ -e /etc/searxng/settings.yml ]; then
  cp /etc/searxng/settings.yml /etc/frea/settings.yml
fi

if [ ! -e /etc/frea/settings.yml ]; then
  mv /var/frea/utils/templates/etc/frea/settings.yml /etc/frea/settings.yml
fi

if grep -q ultrasecretkey /var/frea/searx/settings.yml; then
  sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/var/frea/searx/settings.yml"
fi

su frea -c "uwsgi --master --http-socket 0.0.0.0:8888 /etc/searxng/uwsgi.ini"

