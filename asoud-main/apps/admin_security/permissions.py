"""
RUTHLESS Admin Permissions - Maximum Security
"""
import time
import logging
from rest_framework.permissions import BasePermission
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger('asoud')


class UltraSecureAdminPermission(BasePermission):
    """
    Ultra-secure admin permission with multiple security layers
    """
    
    def has_permission(self, request, view):
        # Layer 1: Basic authentication check
        if not request.user or not request.user.is_authenticated:
            logger.warning(f"ADMIN_ACCESS_DENIED: Unauthenticated request from {self._get_client_ip(request)}")
            return False
        
        # Layer 2: Superuser requirement
        if not request.user.is_superuser:
            logger.warning(f"ADMIN_ACCESS_DENIED: Non-superuser {request.user.id} attempted access")
            return False
        
        # Layer 3: Active user requirement
        if not request.user.is_active:
            logger.warning(f"ADMIN_ACCESS_DENIED: Inactive user {request.user.id}")
            return False
        
        # Layer 4: Time-based access control (optional - can be configured)
        if not self._check_time_based_access():
            logger.warning(f"ADMIN_ACCESS_DENIED: Outside allowed time window for user {request.user.id}")
            return False
        
        # Layer 5: Rate limiting per user
        if not self._check_user_rate_limit(request.user):
            logger.warning(f"ADMIN_ACCESS_DENIED: Rate limit exceeded for user {request.user.id}")
            return False
        
        # Layer 6: Session validation
        if not self._validate_admin_session(request):
            logger.warning(f"ADMIN_ACCESS_DENIED: Invalid session for user {request.user.id}")
            return False
        
        # All checks passed
        logger.info(f"ADMIN_ACCESS_GRANTED: User {request.user.id} from {self._get_client_ip(request)}")
        return True
    
    def _check_time_based_access(self):
        """
        Optional: Restrict admin access to specific hours
        Can be configured via environment variables
        """
        restricted_hours = getattr(settings, 'ADMIN_RESTRICTED_HOURS', None)
        if not restricted_hours:
            return True
        
        current_hour = time.localtime().tm_hour
        start_hour, end_hour = restricted_hours
        
        if start_hour <= end_hour:
            return start_hour <= current_hour <= end_hour
        else:  # Overnight restriction (e.g., 22 to 6)
            return current_hour >= start_hour or current_hour <= end_hour
    
    def _check_user_rate_limit(self, user):
        """
        Per-user rate limiting for admin actions
        """
        cache_key = f'admin_rate_limit_{user.id}'
        current_requests = cache.get(cache_key, 0)
        
        # Allow 100 admin requests per hour per user
        max_requests = getattr(settings, 'ADMIN_RATE_LIMIT_PER_HOUR', 100)
        
        if current_requests >= max_requests:
            return False
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, 3600)
        return True
    
    def _validate_admin_session(self, request):
        """
        Additional session validation for admin users
        """
        user = request.user
        session_key = f'admin_session_valid_{user.id}'
        
        # Check if session is explicitly invalidated
        if cache.get(f'admin_session_invalidated_{user.id}'):
            return False
        
        # Refresh session validity
        cache.set(session_key, True, 1800)  # 30 minutes
        return True
    
    def _get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AdminMarketAccessPermission(BasePermission):
    """
    Permission for admin to access market-related endpoints
    """
    
    def has_permission(self, request, view):
        # Must pass basic admin permission first
        if not UltraSecureAdminPermission().has_permission(request, view):
            return False
        
        # Additional market-specific checks can be added here
        return True


class AdminUserManagementPermission(BasePermission):
    """
    Permission for admin user management operations
    """
    
    def has_permission(self, request, view):
        # Must pass basic admin permission first
        if not UltraSecureAdminPermission().has_permission(request, view):
            return False
        
        # Log sensitive user management operations
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logger.critical(f"ADMIN_USER_MANAGEMENT: User {request.user.id} performing {request.method} on {request.path}")
        
        return True


class AdminSystemAccessPermission(BasePermission):
    """
    Permission for admin system-level operations
    """
    
    def has_permission(self, request, view):
        # Must pass basic admin permission first
        if not UltraSecureAdminPermission().has_permission(request, view):
            return False
        
        # Extra validation for system-level operations
        user = request.user
        
        # Check if user has system admin role (can be extended)
        if not getattr(user, 'is_system_admin', True):  # Default to True for now
            logger.critical(f"ADMIN_SYSTEM_ACCESS_DENIED: User {user.id} lacks system admin privileges")
            return False
        
        return True