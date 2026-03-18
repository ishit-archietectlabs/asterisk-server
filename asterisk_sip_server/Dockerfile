ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install Asterisk and dependencies
RUN apk add --no-cache \
    asterisk \
    asterisk-pjsip \
    asterisk-srtp \
    asterisk-sounds-en \
    asterisk-sounds-moh \
    openssl \
    curl \
    bash \
    jq

# Create directories
RUN mkdir -p /etc/asterisk \
    /var/run/asterisk \
    /var/lib/asterisk \
    /var/log/asterisk \
    /var/spool/asterisk \
    /opt/certs

# Copy Asterisk configuration templates
COPY asterisk/ /etc/asterisk/

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

CMD ["/run.sh"]
