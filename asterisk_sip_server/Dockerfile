ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install Asterisk, Node.js, and dependencies (Debian/Ubuntu)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asterisk \
        asterisk-core-sounds-en \
        asterisk-moh-opsound \
        nodejs \
        npm \
        openssl \
        curl \
        bash \
        jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create required Asterisk and app directories
RUN mkdir -p /etc/asterisk \
    /var/run/asterisk \
    /var/lib/asterisk \
    /var/log/asterisk \
    /var/spool/asterisk \
    /opt/certs \
    /app

WORKDIR /app

# Copy Asterisk configuration templates
COPY asterisk/ /etc/asterisk/

# Copy Node.js application files
COPY package.json server.js ./
COPY public/ ./public/

# Install Node.js dependencies
RUN if [ -f package.json ]; then npm install --production; fi

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

CMD ["/run.sh"]
