#!/usr/bin/env bashio
set -e

# ============================================================
# Asterisk Server Add-on — Entrypoint (Bullseye Stable)
# ============================================================

CONFIG_PATH=/data/options.json

AGENT_PASSWORD=$(bashio::config 'agent_password')
CLIENT_DEFAULT_PASSWORD=$(bashio::config 'client_default_password')
DOMAIN=$(bashio::config 'domain')
CERTFILE=$(bashio::config 'certfile')
KEYFILE=$(bashio::config 'keyfile')

# ---------- TLS Certificates ----------
CERT_DIR="/opt/certs"
if bashio::config.has_value 'certfile' && [ -f "/ssl/${CERTFILE}" ]; then
    bashio::log.info "Using provided TLS certificates"
    cp "/ssl/${CERTFILE}" "${CERT_DIR}/asterisk.crt"
    cp "/ssl/${KEYFILE}" "${CERT_DIR}/asterisk.key"
else
    bashio::log.info "Generating self-signed TLS certificates"
    openssl req -x509 -nodes -newkey rsa:2048 \
        -keyout "${CERT_DIR}/asterisk.key" \
        -out "${CERT_DIR}/asterisk.crt" \
        -days 3650 \
        -subj "/CN=${DOMAIN}" 2>/dev/null
fi

# Combine for Asterisk
cat "${CERT_DIR}/asterisk.crt" "${CERT_DIR}/asterisk.key" > "${CERT_DIR}/asterisk.pem"
chmod 644 "${CERT_DIR}/asterisk.pem" "${CERT_DIR}/asterisk.crt" "${CERT_DIR}/asterisk.key"

# ---------- Template Asterisk Config ----------
sed -i "s|__AGENT_PASSWORD__|${AGENT_PASSWORD}|g" /etc/asterisk/pjsip.conf
sed -i "s|__CLIENT_PASSWORD__|${CLIENT_DEFAULT_PASSWORD}|g" /etc/asterisk/pjsip.conf
sed -i "s|__DOMAIN__|${DOMAIN}|g" /etc/asterisk/pjsip.conf
sed -i "s|__CERT_FILE__|${CERT_DIR}/asterisk.crt|g" /etc/asterisk/pjsip.conf
sed -i "s|__KEY_FILE__|${CERT_DIR}/asterisk.key|g" /etc/asterisk/pjsip.conf
sed -i "s|__CERT_FILE__|${CERT_DIR}/asterisk.crt|g" /etc/asterisk/http.conf
sed -i "s|__KEY_FILE__|${CERT_DIR}/asterisk.key|g" /etc/asterisk/http.conf

# ---------- Start Services ----------

bashio::log.info "Starting Asterisk Web UI Dashboard..."
cd /app
node server.js &

# Start asterisk in the foreground to keep container running
# -U root -G root: Explicitly run as root to avoid capability issues
# -p: Run as pseudo-realtime
exec asterisk -f -vvv -U root -G root -p -C /etc/asterisk/asterisk.conf
