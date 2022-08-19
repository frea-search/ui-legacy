FROM debian:stable

ENTRYPOINT exec su-exec searxng:searxng uwsgi --master --http-socket 8888 /usr/local/searxng/searxng-src/dockerfiles/uwsgi.ini

RUN apt-get update && apt-get install -y \
    python3-dev python3-babel python3-venv \
    uwsgi uwsgi-plugin-python3 \
    git build-essential libxslt-dev zlib1g-dev libffi-dev libssl-dev
    
RUN useradd --shell /bin/bash --system \
    --home-dir "/usr/local/searxng" \
    --comment 'Privacy-respecting metasearch engine' \
    searxng
    
RUN mkdir "/usr/local/searxng" && chown -R "searxng:searxng" "/usr/local/searxng"


WORKDIR /usr/local/searxng
COPY --chown=searxng:searxng . .

RUN su searxng -c "python3 -m venv /usr/local/searxng/searx-pyenv"

RUN su searxng -c "echo \". /usr/local/searxng/searx-pyenv/bin/activate\" >> \"/usr/local/searxng/.profile\""  

RUN su searxng -c "pip install -U pip && \
                   pip install -U setuptools && \
                   pip install -U wheel && \
                   pip install -U pyyaml"
                   
RUN cd "/usr/local/searxng/searxng-src"
RUN pip install -e .

RUN mkdir -p "/etc/searxng"
RUN cp "/usr/local/searxng/searxng-src/utils/templates/etc/searxng/settings.yml" "/etc/searxng/settings.yml"
#RUN sed -i -e "s/ultrasecretkey/$(openssl rand -hex 16)/g" "/etc/searxng/settings.yml"
