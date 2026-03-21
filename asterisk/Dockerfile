FROM ghcr.io/home-assistant/base:latest

RUN apk add --no-cache asterisk python3 dos2unix

# Copy s6 service
COPY rootfs/ /

# Fix permissions and line endings
RUN chmod +x /etc/services.d/asterisk/run
RUN chmod +x /etc/services.d/web/run
RUN dos2unix /etc/services.d/asterisk/run
RUN dos2unix /etc/services.d/web/run
