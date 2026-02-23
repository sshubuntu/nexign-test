FROM registry.redhat.io/ubi9/ubi:9.7 AS builder
RUN dnf -y update && dnf -y install  gcc make pkgconf perl tar gzip wget && dnf clean all
WORKDIR /build
RUN wget -O valkey.tar.gz https://github.com/valkey-io/valkey/archive/refs/tags/9.0.2.tar.gz && tar -xzf valkey.tar.gz && mv valkey-9.0.2 valkey
WORKDIR /build/valkey
RUN make -j$(nproc) && make install

FROM registry.redhat.io/ubi9/ubi-minimal:9.7
EXPOSE 6379
RUN microdnf -y update  && microdnf -y install shadow-utils && microdnf clean all
RUN mkdir -p /data /etc/valkey \
    && groupadd -r -g 1001 valkey \
    && useradd -r -u 1001 -g valkey -s /sbin/nologin valkey
COPY --from=builder --chown=valkey:valkey /usr/local/bin/valkey-server /usr/local/bin/valkey-cli /usr/local/bin/
COPY --chown=valkey:valkey valkey.conf /etc/valkey/valkey.conf
WORKDIR /data
VOLUME /data
USER 1001


CMD ["valkey-server", "/etc/valkey/valkey.conf"]
