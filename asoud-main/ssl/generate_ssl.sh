#!/bin/bash

# RUTHLESS SSL Certificate Generation Script
# Maximum Security Implementation

set -euo pipefail

echo "🔐 ASOUD SSL Certificate Generation - MAXIMUM SECURITY MODE"
echo "========================================================"

# Configuration
DOMAIN="asoud.ir"
DAYS=365
KEY_SIZE=4096
SSL_DIR="/etc/ssl"
CERT_DIR="$SSL_DIR/certs"
PRIVATE_DIR="$SSL_DIR/private"

# Create directories
sudo mkdir -p "$CERT_DIR" "$PRIVATE_DIR"
sudo chmod 755 "$CERT_DIR"
sudo chmod 700 "$PRIVATE_DIR"

echo "🔥 Generating ultra-secure DH parameters (4096-bit)..."
sudo openssl dhparam -out "$CERT_DIR/dhparam.pem" 4096

echo "🛡️ Generating private key (4096-bit RSA)..."
sudo openssl genrsa -out "$PRIVATE_DIR/asoud.key" $KEY_SIZE
sudo chmod 600 "$PRIVATE_DIR/asoud.key"

echo "📝 Creating certificate signing request..."
sudo openssl req -new -key "$PRIVATE_DIR/asoud.key" -out "$CERT_DIR/asoud.csr" -subj "/C=IR/ST=Tehran/L=Tehran/O=ASOUD/OU=IT/CN=$DOMAIN/emailAddress=admin@$DOMAIN" -config <(
cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = IR
ST = Tehran
L = Tehran
O = ASOUD
OU = IT Department
CN = $DOMAIN
emailAddress = admin@$DOMAIN

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = *.$DOMAIN
DNS.3 = www.$DOMAIN
DNS.4 = app.$DOMAIN
DNS.5 = api.$DOMAIN
DNS.6 = admin.$DOMAIN
EOF
)

echo "🔐 Generating self-signed certificate (for development)..."
sudo openssl x509 -req -in "$CERT_DIR/asoud.csr" -signkey "$PRIVATE_DIR/asoud.key" -out "$CERT_DIR/asoud.crt" -days $DAYS -extensions v3_req -extfile <(
cat <<EOF
[v3_req]
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = *.$DOMAIN
DNS.3 = www.$DOMAIN
DNS.4 = app.$DOMAIN
DNS.5 = api.$DOMAIN
DNS.6 = admin.$DOMAIN
EOF
)

echo "📋 Creating certificate chain..."
sudo cp "$CERT_DIR/asoud.crt" "$CERT_DIR/asoud-chain.pem"

echo "🔒 Setting ultra-secure permissions..."
sudo chmod 644 "$CERT_DIR/asoud.crt"
sudo chmod 644 "$CERT_DIR/asoud-chain.pem"
sudo chmod 644 "$CERT_DIR/dhparam.pem"
sudo chmod 600 "$PRIVATE_DIR/asoud.key"
sudo chown root:root "$CERT_DIR"/* "$PRIVATE_DIR"/*

echo "✅ SSL certificates generated successfully!"
echo ""
echo "📊 Certificate Information:"
sudo openssl x509 -in "$CERT_DIR/asoud.crt" -text -noout | grep -E "(Subject:|DNS:|Not Before:|Not After:)"

echo ""
echo "🔥 SECURITY CHECKLIST:"
echo "✅ 4096-bit RSA key generated"
echo "✅ DH parameters for Perfect Forward Secrecy"
echo "✅ Multi-domain SAN certificate"
echo "✅ Secure file permissions set"
echo "✅ Certificate chain created"

echo ""
echo "⚠️  PRODUCTION NOTES:"
echo "   - Replace self-signed certificate with CA-signed certificate for production"
echo "   - Consider using Let's Encrypt for automated certificate renewal"
echo "   - Test SSL configuration: https://www.ssllabs.com/ssltest/"

echo ""
echo "🚀 SSL setup completed! Your ASOUD platform is now ULTRA-SECURE!"