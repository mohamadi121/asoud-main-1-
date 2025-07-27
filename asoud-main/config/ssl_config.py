"""
RUTHLESS SSL Configuration - Maximum Security Implementation
"""
import os
import ssl
from pathlib import Path


class SSLConfigManager:
    """
    Ultra-secure SSL configuration manager
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.ssl_dir = self.base_dir / 'ssl'
        
    def get_ssl_context(self):
        """
        Create ultra-secure SSL context
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        # Ruthless security settings
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        # Disable weak ciphers
        context.set_ciphers([
            'ECDHE+AESGCM',
            'ECDHE+CHACHA20',
            'DHE+AESGCM',
            'DHE+CHACHA20',
            '!aNULL',
            '!MD5',
            '!DSS'
        ])
        
        # Perfect Forward Secrecy
        context.options |= ssl.OP_SINGLE_ECDH_USE
        context.options |= ssl.OP_SINGLE_DH_USE
        context.options |= ssl.OP_NO_COMPRESSION
        context.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
        
        return context
    
    def get_nginx_ssl_config(self):
        """
        Generate ultra-secure nginx SSL configuration
        """
        return {
            'ssl_protocols': 'TLSv1.2 TLSv1.3',
            'ssl_ciphers': 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384',
            'ssl_prefer_server_ciphers': 'off',
            'ssl_session_cache': 'shared:SSL:10m',
            'ssl_session_timeout': '10m',
            'ssl_session_tickets': 'off',
            'ssl_stapling': 'on',
            'ssl_stapling_verify': 'on',
            'ssl_dhparam': '/etc/ssl/certs/dhparam.pem',
        }
    
    def generate_security_headers(self):
        """
        Generate comprehensive security headers
        """
        return {
            'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' wss: https:; "
                "font-src 'self'; "
                "object-src 'none'; "
                "media-src 'self'; "
                "frame-src 'none'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            ),
            'Permissions-Policy': (
                "accelerometer=(), "
                "ambient-light-sensor=(), "
                "autoplay=(), "
                "battery=(), "
                "camera=(), "
                "cross-origin-isolated=(), "
                "display-capture=(), "
                "document-domain=(), "
                "encrypted-media=(), "
                "execution-while-not-rendered=(), "
                "execution-while-out-of-viewport=(), "
                "fullscreen=(), "
                "geolocation=(), "
                "gyroscope=(), "
                "magnetometer=(), "
                "microphone=(), "
                "midi=(), "
                "navigation-override=(), "
                "payment=(), "
                "picture-in-picture=(), "
                "publickey-credentials-get=(), "
                "screen-wake-lock=(), "
                "sync-xhr=(), "
                "usb=(), "
                "web-share=(), "
                "xr-spatial-tracking=()"
            )
        }


# SSL Configuration Constants
SSL_CONFIG = SSLConfigManager()