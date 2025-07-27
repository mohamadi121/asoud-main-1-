from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from utils.response import ApiResponse
import logging
import traceback

logger = logging.getLogger('asoud')


def custom_exception_handler(exc, context):
    """
    Ruthless secure exception handler - zero information disclosure
    """
    # Get the standard error response first
    response = drf_exception_handler(exc, context)
    
    # Handle Django core exceptions
    if isinstance(exc, ValidationError):
        response = Response(ApiResponse(
            success=False,
            code=400,
            error={
                'code': 'validation_error',
                'detail': 'Input validation failed'
            }
        ), status=400)
    
    elif isinstance(exc, PermissionDenied):
        response = Response(ApiResponse(
            success=False,
            code=403,
            error={
                'code': 'permission_denied',
                'detail': 'Access forbidden'
            }
        ), status=403)
    
    elif isinstance(exc, Http404):
        response = Response(ApiResponse(
            success=False,
            code=404,
            error={
                'code': 'not_found',
                'detail': 'Resource not found'
            }
        ), status=404)
    
    if response is not None:
        # Secure logging without sensitive data exposure
        request = context.get('request')
        if request:
            safe_path = request.path if hasattr(request, 'path') else 'unknown'
            safe_method = request.method if hasattr(request, 'method') else 'unknown'
            safe_ip = request.META.get('REMOTE_ADDR', 'unknown')[:10]  # Truncate IP
            
            logger.error(
                f"API_ERROR: {exc.__class__.__name__} | PATH: {safe_path} | METHOD: {safe_method} | IP: {safe_ip}... | STATUS: {response.status_code}",
                extra={
                    'error_type': exc.__class__.__name__,
                    'status_code': response.status_code,
                    'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
                }
            )
        
        # Standardize all error responses using ApiResponse
        status_code = response.status_code
        error_messages = {
            400: 'Request validation failed',
            401: 'Authentication required', 
            403: 'Access forbidden',
            404: 'Resource not found',
            405: 'Method not allowed',
            429: 'Rate limit exceeded',
            500: 'Server error occurred',
        }
        
        error_codes = {
            400: 'validation_error',
            401: 'authentication_required',
            403: 'permission_denied', 
            404: 'not_found',
            405: 'method_not_allowed',
            429: 'rate_limit_exceeded',
            500: 'server_error',
        }
        
        response.data = ApiResponse(
            success=False,
            code=status_code,
            error={
                'code': error_codes.get(status_code, 'server_error'),
                'detail': error_messages.get(status_code, 'An error occurred'),
            }
        )
    
    else:
        # Handle unexpected exceptions
        from django.conf import settings
        logger.error(
            f"UNHANDLED_EXCEPTION: {exc.__class__.__name__}: {str(exc)[:100]}",
            extra={'error_type': exc.__class__.__name__}
        )
        
        response = Response(ApiResponse(
            success=False,
            code=500,
            error={
                'code': 'server_error',
                'detail': 'Server error occurred'
            }
        ), status=500)
    
    return response
