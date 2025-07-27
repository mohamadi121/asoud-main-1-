"""
RUTHLESS Admin Security Middleware - Maximum Security Implementation
"""
import time
import hashlib
import hmac
import logging
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from utils.response import ApiResponse

User = get_user_model()
logger = logging.getLogger('asoud')


class AdminSecurityMiddleware(MiddlewareMixin):
    """
    RUTHLESS Admin Security Middleware
    - Brute force protection
    - Session hijacking prevention
    - Advanced threat detection
    - Zero-tolerance security policy
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Only apply to admin endpoints
        if not request.path.startswith('/api/v1/secure-admin/'):
            return None
            
        # 1. IP-based brute force protection
        if self._is_ip_blocked(request):
            logger.critical(f"BLOCKED_IP_ADMIN_ACCESS: {self._get_client_ip(request)}")
            return JsonResponse(ApiResponse(
                success=False,
                code=429,
                error={'code': 'ip_blocked', 'detail': 'IP temporarily blocked'}
            ), status=429)
        
        # 2. Advanced session security validation
        if hasattr(request, 'user') and request.user.is_authenticated:
            if not self._validate_session_security(request):
                logger.critical(f"SESSION_HIJACKING_ATTEMPT: User {request.user.id}")
                return JsonResponse(ApiResponse(
                    success=False,
                    code=403,
                    error={'code': 'session_invalid', 'detail': 'Session security validation failed'}
                ), status=403)
        
        # 3. Request fingerprinting for anomaly detection
        self._track_request_fingerprint(request)
        
        return None
    
    def process_response(self, request, response):
        # Only apply to admin endpoints
        if not request.path.startswith('/api/v1/secure-admin/'):
            return response
            
        # Add ultra-secure headers for admin endpoints
        response['X-Admin-Security'] = 'MAXIMUM'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        # Track failed attempts
        if response.status_code >= 400:
            self._record_failed_attempt(request)
        
        return response
    
    def _is_ip_blocked(self, request):
        """Check if IP is temporarily blocked due to failed attempts"""
        ip = self._get_client_ip(request)
        failed_attempts = cache.get(f'admin_failed_{ip}', 0)
        
        # Block after 3 failed attempts for 1 hour
        if failed_attempts >= 3:
            return True
        return False
    
    def _get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _validate_session_security(self, request):
        """Advanced session security validation"""
        user = request.user
        if not user.is_superuser:
            return False
            
        # Session fingerprint validation
        current_fingerprint = self._generate_session_fingerprint(request)
        stored_fingerprint = cache.get(f'admin_session_{user.id}')
        
        if stored_fingerprint and stored_fingerprint != current_fingerprint:
            logger.warning(f"Session fingerprint mismatch for user {user.id}")
            return False
        
        # Store/update fingerprint
        cache.set(f'admin_session_{user.id}', current_fingerprint, 3600)
        return True
    
    def _generate_session_fingerprint(self, request):
        """Generate unique session fingerprint"""
        components = [
            request.META.get('HTTP_USER_AGENT', ''),
            request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
            self._get_client_ip(request),
        ]
        fingerprint_data = '|'.join(components)
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def _track_request_fingerprint(self, request):
        """Track request patterns for anomaly detection"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_id = request.user.id
            current_time = int(time.time())
            
            # Track request frequency
            cache_key = f'admin_requests_{user_id}'
            requests_count = cache.get(cache_key, 0)
            cache.set(cache_key, requests_count + 1, 300)  # 5 minutes window
            
            # Alert on suspicious activity (>50 requests in 5 minutes)
            if requests_count > 50:
                logger.critical(f"SUSPICIOUS_ADMIN_ACTIVITY: User {user_id} - {requests_count} requests")
    
    def _record_failed_attempt(self, request):
        """Record failed admin access attempt"""
        ip = self._get_client_ip(request)
        cache_key = f'admin_failed_{ip}'
        failed_count = cache.get(cache_key, 0)
        cache.set(cache_key, failed_count + 1, 3600)  # 1 hour
        
        logger.warning(f"ADMIN_FAILED_ATTEMPT: IP {ip} - Attempt #{failed_count + 1}")


class AdminAuditMiddleware(MiddlewareMixin):
    """
    Comprehensive Admin Audit Logging
    """
    
    def process_response(self, request, response):
        if not request.path.startswith('/api/v1/secure-admin/'):
            return response
            
        # Log all admin actions
        if hasattr(request, 'user') and request.user.is_authenticated:
            audit_data = {
                'user_id': request.user.id,
                'mobile_last_4': request.user.mobile_number[-4:] if request.user.mobile_number else 'N/A',
                'action': request.path,
                'method': request.method,
                'ip': self._get_client_ip(request),
                'status': response.status_code,
                'timestamp': time.time()
            }
            
            # Store in cache for audit trail
            cache_key = f'admin_audit_{request.user.id}_{int(time.time())}'
            cache.set(cache_key, audit_data, 86400 * 7)  # Keep for 7 days
            
            logger.info(f"ADMIN_AUDIT: {audit_data}")
        
        return response
    
    def _get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip