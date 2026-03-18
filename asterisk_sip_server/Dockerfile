ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install Asterisk, Node.js, and dependencies
RUN apk add --no-cache \
    asterisk \
    asterisk-pjsip \
    asterisk-srtp \
    asterisk-sounds-en \
    asterisk-sounds-moh \
    nodejs \
    npm \
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
    /opt/certs \
    /app

WORKDIR /app

# Copy Asterisk configuration templates
COPY asterisk/ /etc/asterisk/

# Copy Node.js application files
COPY package.json server.js ./
COPY public/ ./public/

# Install Node.js dependencies
RUN npm install --production

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

CMD ["/run.sh"]
