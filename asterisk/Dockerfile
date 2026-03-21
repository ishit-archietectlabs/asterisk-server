# Final Dockerfile for Asterisk SIP Server (Alpine-based)
FROM ghcr.io/home-assistant/base:latest

# Install Asterisk and dependencies
RUN apk add --no-cache \
    asterisk \
    asterisk-sample-config \
    asterisk-sounds-en \
    nodejs \
    npm \
    curl \
    bash \
    jq \
    openssl

# Create required directories
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
