FROM fedora:latest
ENTRYPOINT ["/usr/libexec/init-server.sh"]

ARG SEARXNG_GID=1000
ARG SEARXNG_UID=1000

ENV PYTHONIOENCODING utf-8

ENV INSTANCE_NAME=FreaSearch \
    AUTOCOMPLETE= \
    BASE_URL= \
    MORTY_KEY= \
    MORTY_URL= \
    SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml \
    UWSGI_SETTINGS_PATH=/etc/searxng/uwsgi.ini

WORKDIR /var/frea

COPY requirements.txt ./requirements.txt

RUN dnf update -y \
 && dnf install -y \
    ca-certificates \
    python3 \
    python3-pip \
    libxml2 \
    libxslt \
    openssl \
    tini \
    uwsgi \
    uwsgi-plugin-python3 \
    brotli \
    boost \
    mecab-ipadic \
    sqlite \
    git \
 && dnf install -y \
    make automake gcc gcc-c++ \
    python3-setuptools \
    python3-devel \
    libffi-devel \
    libxslt-devel \
    libxml2-devel \
    openssl-devel \
    boost-devel \
    mecab-devel \
    sqlite-devel \
    tar \
    bash \
    
 # Install pip packages
 && cd /var/frea \
 && pip3 install --upgrade pip wheel setuptools \
 && pip3 install --no-cache -r requirements.txt \
 && python3 -m pygeonlp.api setup /usr/pygeonlp_basedata \
 
 # clean up
 && dnf remove -y \
    make automake gcc gcc-c++ \
    python3-setuptools \
    python3-devel \
    libffi-devel \
    libxslt-devel \
    libxml2-devel \
    openssl-devel \
    boost-devel \
    mecab-devel \
    sqlite-devel \
 && dnf autoremove -y \
 && rm -rf /root/.cache /tmp/mecab-[0-9]* /tmp/mecab-ipadic-*

RUN groupadd -g ${SEARXNG_GID} frea && \
    adduser -u ${SEARXNG_UID} -d /var/frea -s /bin/sh -g frea frea
    
COPY --chown=frea:frea . .

ARG VERSION_GITCOMMIT=unknown

RUN su frea -c "/usr/bin/python3 -m compileall -q searx"

RUN mv "/var/frea/dockerfiles/init-server.sh" "/usr/libexec/init-server.sh"
RUN chmod +x "/usr/libexec/init-server.sh"
RUN mkdir /etc/searxng
