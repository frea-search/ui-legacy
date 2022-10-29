FROM fedora:latest
ENTRYPOINT ["/usr/libexec/init"]

ARG SEARXNG_GID=1000
ARG SEARXNG_UID=1000

ENV POSTGRESQL_HOST=db \
    POSTGRESQL_USER=freasearch \
    POSTGRESQL_PASSWORD=freasearch \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    TURNSTILE_SITE_KEY=CHANGEME \
    TURNSTILE_SECRET_KEY=CHANGEME

WORKDIR /var/frea

COPY requirements.txt ./requirements.txt

# install packages
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
    libpq \
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
    libpq-devel \
    tar \
    bash \
    cargo \
    git

 
# Install pip packages
RUN cd /var/frea \
 && pip3 install --upgrade pip wheel setuptools \
 && pip3 install --no-cache -r requirements.txt

RUN groupadd -g ${SEARXNG_GID} frea && \
    useradd -u ${SEARXNG_UID} -d /var/frea -s /bin/sh -g frea frea

RUN chown -R frea:frea /var/frea && \
    su frea -c "python3 -m pygeonlp.api setup /usr/pygeonlp_basedata"

COPY --chown=frea:frea . .

ARG VERSION_GITCOMMIT=unknown

RUN su frea -c "/usr/bin/python3 -m compileall -q searx"

RUN cd ./tools/init \
 && cargo build --release \
 && cd /var/frea \
 && mv ./tools/init/target/release/init /usr/libexec/init

# clean up
RUN dnf remove -y \
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
    libpq-devel \
    cargo \
    git \
 && dnf autoremove -y \
 && rm -rf /root/.cache ./subsystems/org.freasearch.innocence-force/chk_db ./tools/init

RUN mv "/var/frea/dockerfiles/init-server.sh" "/usr/libexec/init-server.sh"
RUN chmod +x "/usr/libexec/init-server.sh"
RUN mkdir /etc/searxng
