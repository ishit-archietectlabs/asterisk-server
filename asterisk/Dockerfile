FROM ghcr.io/home-assistant/base:latest

# Install Asterisk
RUN apk add --no-cache asterisk

# Copy run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh
