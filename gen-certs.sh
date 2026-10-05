#!/usr/bin/env sh
set -eu

CERT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/nginx/certs"
mkdir -p "$CERT_DIR"

openssl req \
  -x509 \
  -nodes \
  -newkey rsa:2048 \
  -sha256 \
  -days 365 \
  -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.crt" \
  -subj "/C=RU/ST=Local/L=Local/O=Local Dev/OU=DevOps/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 600 "$CERT_DIR/server.key"
printf 'Certificate generated:\n  %s\n  %s\n' "$CERT_DIR/server.crt" "$CERT_DIR/server.key"
