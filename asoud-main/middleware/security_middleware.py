from django.http import HttpResponse
from django.core.cache import cache


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip rate limiting for authenticated users with tokens
        if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated') and request.user.is_authenticated:
            return self.get_response(request)
            
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Rate limit key
        cache_key = f'rate_limit_{ip}'
        
        # Check current requests count
        current_requests = cache.get(cache_key, 0)
        
        # Allow 60 requests per minute for anonymous users
        if current_requests >= 60:
            return HttpResponse("Rate limit exceeded", status=429)
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, 60)
        
        response = self.get_response(request)
        return response


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Ruthless security headers - zero performance impact
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['X-Permitted-Cross-Domain-Policies'] = 'none'
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "font-src 'self'; "
            "object-src 'none'; "
            "media-src 'self'; "
            "frame-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'"
        )
        response['Feature-Policy'] = (
            "accelerometer 'none'; "
            "ambient-light-sensor 'none'; "
            "autoplay 'none'; "
            "battery 'none'; "
            "camera 'none'; "
            "display-capture 'none'; "
            "document-domain 'none'; "
            "encrypted-media 'none'; "
            "fullscreen 'none'; "
            "geolocation 'none'; "
            "gyroscope 'none'; "
            "magnetometer 'none'; "
            "microphone 'none'; "
            "midi 'none'; "
            "payment 'none'; "
            "picture-in-picture 'none'; "
            "publickey-credentials-get 'none'; "
            "speaker-selection 'none'; "
            "sync-xhr 'none'; "
            "usb 'none'; "
            "wake-lock 'none'; "
            "xr-spatial-tracking 'none'"
        )
        
        # HSTS only for HTTPS
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
        
        # Remove server identification
        if 'Server' in response:
            del response['Server']
        
        # Anti-fingerprinting
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response