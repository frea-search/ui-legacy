FROM fedora:latest
ENTRYPOINT ["/usr/libexec/init"]

ARG SEARXNG_GID=1000
ARG SEARXNG_UID=1000

ENV POSTGRESQL_HOST=db \
    POSTGRESQL_USER=freasearch \
    POSTGRESQL_PASSWORD=freasearch \
    REDIS_HOST=redis \
    REDIS_PORT=6379

WORKDIR /var/frea

# install packages
RUN dnf update -y \
 && dnf install -y \
    ca-certificates \
    mailcap \
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
COPY requirements.txt ./requirements.txt
RUN cd /var/frea \
 && pip3 install --no-cache -r requirements.txt

RUN groupadd -g ${SEARXNG_GID} frea \
 && useradd -u ${SEARXNG_UID} -d /var/frea -s /bin/sh -g frea frea

RUN chown -R frea:frea /var/frea \
 && su frea -c "python3 -m pygeonlp.api setup /usr/pygeonlp_basedata"

COPY --chown=frea:frea dockerfiles ./dockerfiles
COPY --chown=frea:frea searx ./searx
COPY --chown=frea:frea subsystems ./subsystems
COPY --chown=frea:frea tools ./tools

RUN find /var/frea/searx/static \( -name '*.html' -o -name '*.css' -o -name '*.js' \
    -o -name '*.svg' -o -name '*.eot' \) \
    -type f -exec gzip -9 -k {} \+ -exec brotli --best {} \+

ARG VERSION_GITCOMMIT=unknown



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
 && rm -rf /root/.cache ./subsystems/org.freasearch.innocence-force/chk_db ./tools \
 && find /usr/lib/python*/ -name '*.pyc' -delete

RUN mv "/var/frea/dockerfiles/init-server.sh" "/usr/libexec/init-server.sh"
RUN chmod +x "/usr/libexec/init-server.sh"
RUN mkdir /etc/searxng
