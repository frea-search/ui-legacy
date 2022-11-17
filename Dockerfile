FROM alpine:latest
ENTRYPOINT ["sh", "/usr/libexec/init-server.sh"]

ARG SEARXNG_GID=1000
ARG SEARXNG_UID=1000

ENV POSTGRESQL_HOST=db \
    POSTGRESQL_USER=freasearch \
    POSTGRESQL_PASSWORD=freasearch \
    REDIS_HOST=redis \
    REDIS_PORT=6379

WORKDIR /var/frea

# install packages
RUN echo -e "https://ap.edge.kernel.org/alpine/v3.16/main\nhttps://ap.edge.kernel.org/alpine/v3.16/community" > /etc/apk/repositories
RUN apk upgrade --no-cache \
 && apk add --no-cache -t build-dependencies \
    build-base \
    py3-setuptools \
    python3-dev \
    libffi-dev \
    libxslt-dev \
    libxml2-dev \
    openssl-dev \
    tar \
    git \
 && apk add --no-cache \
    ca-certificates \
    su-exec \
    python3 \
    py3-pip \
    libxml2 \
    libxslt \
    openssl \
    tini \
    uwsgi \
    uwsgi-python3 \
    brotli

# Install pip packages
COPY requirements.txt ./requirements.txt
RUN cd /var/frea \
 && pip3 install --no-cache -r requirements.txt

RUN addgroup -g ${SEARXNG_GID} frea \
 && adduser -u ${SEARXNG_UID} -D -h /var/frea -s /bin/sh -G frea frea

RUN chown -R frea:frea /var/frea

COPY --chown=frea:frea dockerfiles ./dockerfiles
COPY --chown=frea:frea searx ./searx

RUN find /var/frea/searx/static \( -name '*.html' -o -name '*.css' -o -name '*.js' \
    -o -name '*.svg' -o -name '*.eot' \) \
    -type f -exec gzip -9 -k {} \+ -exec brotli --best {} \+

# clean up
RUN apk del build-dependencies \
 && rm -rf /root/.cache ./subsystems/org.freasearch.innocence-force/chk_db ./tools \
 && find /usr/lib/python*/ -name '*.pyc' -delete

RUN mkdir /usr/libexec/
RUN mv "/var/frea/dockerfiles/init-server.sh" "/usr/libexec/init-server.sh"
RUN chmod +x "/usr/libexec/init-server.sh"
RUN mkdir /etc/searxng
