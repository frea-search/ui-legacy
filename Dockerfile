FROM clearlinux:base
ENTRYPOINT ["/usr/libexec/init"]

ARG SEARXNG_GID=1000
ARG SEARXNG_UID=1000

ENV POSTGRESQL_HOST=db \
    POSTGRESQL_USER=freasearch \
    POSTGRESQL_PASSWORD=freasearch \
    COUNT_USERS=true

WORKDIR /var/frea

COPY requirements.txt ./requirements.txt

# install packages
RUN swupd bundle-add uwsgi python3-basic openssl runtime-libs-boost git sqlite \
 && swupd bundle-add make devpkg-libffi devpkg-libxslt devpkg-libxml2 devpkg-boost devpkg-openssl devpkg-sqlite-autoconf devpkg-postgresql python-basic-dev c-basic rust-basic dnf 
 
# install rpm packages
COPY ./prebuilts/* /tmp/
RUN rpm -U --nodeps /tmp/*.rpm \
 && rm -r /tmp/*.rpm
 
# Install pip packages
RUN cd /var/frea \
 && pip3 install --upgrade pip wheel setuptools \
 && pip3 install --no-cache -r requirements.txt \
 && python3 -m pygeonlp.api setup /usr/pygeonlp_basedata

RUN groupadd -g ${SEARXNG_GID} frea && \
    useradd -u ${SEARXNG_UID} -d /var/frea -s /bin/sh -g frea frea
    
COPY --chown=frea:frea . .
RUN rm -r ./prebuilts

ARG VERSION_GITCOMMIT=unknown

RUN su frea -c "/usr/bin/python3 -m compileall -q searx"
 
RUN cd ./tools/init \
 && cargo build --release \
 && cd /var/frea \
 && mv ./tools/init/target/release/init /usr/libexec/init

# clean up
RUN rpm -e mecab-devel \
 && swupd bundle-remove -R devpkg-libffi devpkg-libxslt devpkg-libxml2 devpkg-sqlite-autoconf  python-basic-dev rust-basic dnf \
 && rm -rf /root/.cache ./subsystems/org.freasearch.innocence-force/chk_db ./tools/init

RUN mv "/var/frea/dockerfiles/init-server.sh" "/usr/libexec/init-server.sh"
RUN chmod +x "/usr/libexec/init-server.sh"
RUN mkdir /etc/searxng
