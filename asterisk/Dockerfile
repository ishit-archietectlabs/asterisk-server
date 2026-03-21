FROM ghcr.io/home-assistant/base:latest

# Install Asterisk python3 dos2unix pip
RUN apk add --no-cache asterisk python3 dos2unix py3-pip

# Install Flask
RUN pip3 install flask

# Create required directories
RUN mkdir -p /var/lib/asterisk \
    && mkdir -p /etc/asterisk \
    && mkdir -p /var/log/asterisk \
    && mkdir -p /var/spool/asterisk \
    && mkdir -p /opt/certs \
    && mkdir -p /app

# Set permissions
RUN chmod -R 777 /var/lib/asterisk \
    && chmod -R 777 /etc/asterisk \
    && chmod -R 777 /var/log/asterisk \
    && chmod -R 777 /var/spool/asterisk

# Copy s6 service
COPY rootfs/ /

# Fix permissions and line endings
RUN chmod +x /etc/services.d/asterisk/run
RUN chmod +x /etc/services.d/web/run
RUN dos2unix /etc/services.d/asterisk/run
RUN dos2unix /etc/services.d/web/run
