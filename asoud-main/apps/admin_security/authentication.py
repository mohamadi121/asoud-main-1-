"""
Custom admin authentication using JWT tokens instead of Django's default admin
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from apps.users.models import User

User = get_user_model()


class AdminTokenAuthentication(TokenAuthentication):
    """
    Secure admin authentication using existing app tokens
    Only allows superuser access
    """
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')
            
        # Additional security: Only superusers can access admin
        if not token.user.is_superuser:
            raise AuthenticationFailed('Admin access denied.')

        return (token.user, token)