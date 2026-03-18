#!/usr/bin/env bash
set -e

# ============================================================
# Asterisk Server Add-on — Entrypoint
# Reads HA options, generates TLS certs, templates configs,
# and starts Asterisk in the foreground.
# ============================================================

CONFIG_PATH=/data/options.json

AGENT_PASSWORD=$(jq -r '.agent_password' $CONFIG_PATH)
CLIENT_DEFAULT_PASSWORD=$(jq -r '.client_default_password' $CONFIG_PATH)
DOMAIN=$(jq -r '.domain' $CONFIG_PATH)
CERTFILE=$(jq -r '.certfile' $CONFIG_PATH)
KEYFILE=$(jq -r '.keyfile' $CONFIG_PATH)

# ---------- TLS Certificates ----------
CERT_DIR="/opt/certs"
if [ -n "$CERTFILE" ] && [ -f "/ssl/$CERTFILE" ]; then
    echo "[INFO] Using provided TLS certificates"
    cp "/ssl/$CERTFILE" "$CERT_DIR/asterisk.crt"
    cp "/ssl/$KEYFILE" "$CERT_DIR/asterisk.key"
else
    echo "[INFO] Generating self-signed TLS certificates"
    openssl req -x509 -nodes -newkey rsa:2048 \
        -keyout "$CERT_DIR/asterisk.key" \
        -out "$CERT_DIR/asterisk.crt" \
        -days 3650 \
        -subj "/CN=$DOMAIN" 2>/dev/null
fi

# Combine for Asterisk
cat "$CERT_DIR/asterisk.crt" "$CERT_DIR/asterisk.key" > "$CERT_DIR/asterisk.pem"
chmod 644 "$CERT_DIR/asterisk.pem" "$CERT_DIR/asterisk.crt" "$CERT_DIR/asterisk.key"

# ---------- Template Asterisk Config ----------
# Replace placeholders in pjsip.conf
sed -i "s|__AGENT_PASSWORD__|${AGENT_PASSWORD}|g" /etc/asterisk/pjsip.conf
sed -i "s|__CLIENT_PASSWORD__|${CLIENT_DEFAULT_PASSWORD}|g" /etc/asterisk/pjsip.conf
sed -i "s|__DOMAIN__|${DOMAIN}|g" /etc/asterisk/pjsip.conf
sed -i "s|__CERT_FILE__|${CERT_DIR}/asterisk.crt|g" /etc/asterisk/pjsip.conf
sed -i "s|__KEY_FILE__|${CERT_DIR}/asterisk.key|g" /etc/asterisk/pjsip.conf
sed -i "s|__CERT_FILE__|${CERT_DIR}/asterisk.crt|g" /etc/asterisk/http.conf
sed -i "s|__KEY_FILE__|${CERT_DIR}/asterisk.key|g" /etc/asterisk/http.conf

echo "[INFO] Starting Asterisk PBX..."
exec asterisk -f -vvv -C /etc/asterisk/asterisk.conf
