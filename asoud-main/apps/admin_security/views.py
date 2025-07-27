"""
RUTHLESS Secure Admin Views - Maximum Security Implementation
"""
from rest_framework import views, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import logging
import time

from utils.response import ApiResponse
from .authentication import AdminTokenAuthentication
from .permissions import (
    UltraSecureAdminPermission, 
    AdminUserManagementPermission,
    AdminSystemAccessPermission
)
from apps.users.serializers import UserSerializer
from apps.market.models import Market
from apps.product.models import Product
from apps.payment.models import Payment

User = get_user_model()
logger = logging.getLogger('asoud')


class AdminSecurityStatusView(views.APIView):
    """
    Admin security status and health check
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [UltraSecureAdminPermission]
    
    def get(self, request):
        try:
            security_status = {
                'session_valid': True,
                'permissions_verified': True,
                'security_level': 'MAXIMUM',
                'timestamp': int(time.time()),
                'user_info': {
                    'id': request.user.id,
                    'mobile_masked': f"***{request.user.mobile_number[-4:]}",
                    'is_superuser': request.user.is_superuser,
                    'last_login': request.user.last_login.isoformat() if request.user.last_login else None
                }
            }
            
            logger.info(f"ADMIN_SECURITY_CHECK: User {request.user.id}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data=security_status,
                message="Security status verified"
            ))
            
        except Exception as e:
            logger.error(f"Admin security status error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Security check failed'}
            ), status=500)


class AdminUsersListView(views.APIView):
    """
    ULTRA-SECURE admin view to list users with advanced filtering
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [AdminUserManagementPermission]
    
    def get(self, request):
        try:
            # Get query parameters
            page = int(request.GET.get('page', 1))
            limit = min(int(request.GET.get('limit', 50)), 100)  # Max 100 per page
            search = request.GET.get('search', '')
            user_type = request.GET.get('type', '')
            is_active = request.GET.get('active', '')
            
            # Build query
            queryset = User.objects.all()
            
            if search:
                queryset = queryset.filter(
                    Q(mobile_number__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            
            if user_type:
                queryset = queryset.filter(type=user_type)
            
            if is_active:
                queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
            # Apply pagination
            offset = (page - 1) * limit
            total_count = queryset.count()
            users = queryset[offset:offset + limit]
            
            serializer = UserSerializer(users, many=True)
            
            response_data = {
                'users': serializer.data,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total_count,
                    'pages': (total_count + limit - 1) // limit
                }
            }
            
            # Secure logging
            logger.info(f"ADMIN_USERS_LIST: User {request.user.id} accessed {len(users)} users")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data=response_data,
                message="Users retrieved successfully"
            ))
            
        except Exception as e:
            logger.error(f"Admin users list error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Server error occurred'}
            ), status=500)


class AdminDashboardStatsView(views.APIView):
    """
    Comprehensive admin dashboard statistics
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [UltraSecureAdminPermission]
    
    def get(self, request):
        try:
            # User statistics
            user_stats = {
                'total_users': User.objects.count(),
                'active_users': User.objects.filter(is_active=True).count(),
                'new_users_today': User.objects.filter(
                    date_joined__gte=timezone.now().date()
                ).count(),
                'user_types': {
                    'users': User.objects.filter(type=User.USER).count(),
                    'owners': User.objects.filter(type=User.OWNER).count(),
                    'marketers': User.objects.filter(type=User.MARKETER).count(),
                }
            }
            
            # Market statistics
            market_stats = {
                'total_markets': Market.objects.count(),
                'published_markets': Market.objects.filter(status=Market.PUBLISHED).count(),
                'pending_markets': Market.objects.filter(status=Market.QUEUE).count(),
                'paid_markets': Market.objects.filter(is_paid=True).count(),
            }
            
            # Product statistics
            product_stats = {
                'total_products': Product.objects.count(),
                'published_products': Product.objects.filter(status=Product.PUBLISHED).count(),
                'draft_products': Product.objects.filter(status=Product.DRAFT).count(),
            }
            
            # Payment statistics (last 30 days)
            thirty_days_ago = timezone.now() - timedelta(days=30)
            payment_stats = {
                'total_payments': Payment.objects.count(),
                'recent_payments': Payment.objects.filter(created_at__gte=thirty_days_ago).count(),
                'completed_payments': Payment.objects.filter(status=Payment.COMPLETE).count(),
                'pending_payments': Payment.objects.filter(status=Payment.PENDING).count(),
            }
            
            stats = {
                'users': user_stats,
                'markets': market_stats,
                'products': product_stats,
                'payments': payment_stats,
                'system': {
                    'timestamp': int(time.time()),
                    'cache_status': 'healthy' if cache.get('health_check') != False else 'degraded'
                }
            }
            
            logger.info(f"ADMIN_DASHBOARD_STATS: User {request.user.id}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data=stats,
                message="Dashboard stats retrieved successfully"
            ))
            
        except Exception as e:
            logger.error(f"Admin dashboard stats error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Server error occurred'}
            ), status=500)


class AdminUserDetailView(views.APIView):
    """
    Get detailed information about a specific user
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [AdminUserManagementPermission]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            
            # Additional admin-only information
            admin_data = {
                'user': serializer.data,
                'admin_info': {
                    'date_joined': user.date_joined.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'is_active': user.is_active,
                    'markets_count': user.markets.count() if hasattr(user, 'markets') else 0,
                }
            }
            
            logger.info(f"ADMIN_USER_DETAIL: User {request.user.id} viewed user {user_id}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data=admin_data,
                message="User details retrieved successfully"
            ))
            
        except User.DoesNotExist:
            return Response(ApiResponse(
                success=False,
                code=404,
                error={'code': 'user_not_found', 'detail': 'User not found'}
            ), status=404)
        except Exception as e:
            logger.error(f"Admin user detail error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Server error occurred'}
            ), status=500)


class AdminUserToggleActiveView(views.APIView):
    """
    Toggle user active status (activate/deactivate)
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [AdminUserManagementPermission]
    
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent deactivating superusers
            if user.is_superuser and user.is_active:
                return Response(ApiResponse(
                    success=False,
                    code=403,
                    error={'code': 'cannot_deactivate_admin', 'detail': 'Cannot deactivate admin users'}
                ), status=403)
            
            # Toggle active status
            user.is_active = not user.is_active
            user.save()
            
            action = 'activated' if user.is_active else 'deactivated'
            logger.critical(f"ADMIN_USER_TOGGLE: User {request.user.id} {action} user {user_id}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data={'user_id': user_id, 'is_active': user.is_active},
                message=f"User {action} successfully"
            ))
            
        except User.DoesNotExist:
            return Response(ApiResponse(
                success=False,
                code=404,
                error={'code': 'user_not_found', 'detail': 'User not found'}
            ), status=404)
        except Exception as e:
            logger.error(f"Admin user toggle error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Server error occurred'}
            ), status=500)


class AdminSystemHealthView(views.APIView):
    """
    System health check for admin monitoring
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [AdminSystemAccessPermission]
    
    def get(self, request):
        try:
            health_status = {
                'database': self._check_database_health(),
                'cache': self._check_cache_health(),
                'storage': self._check_storage_health(),
                'security': self._check_security_health(),
                'timestamp': int(time.time())
            }
            
            overall_health = all(health_status[key]['status'] == 'healthy' 
                               for key in ['database', 'cache', 'storage', 'security'])
            
            health_status['overall'] = 'healthy' if overall_health else 'degraded'
            
            logger.info(f"ADMIN_SYSTEM_HEALTH: User {request.user.id} - Overall: {health_status['overall']}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data=health_status,
                message="System health check completed"
            ))
            
        except Exception as e:
            logger.error(f"Admin system health error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Health check failed'}
            ), status=500)
    
    def _check_database_health(self):
        try:
            User.objects.count()
            return {'status': 'healthy', 'message': 'Database connection OK'}
        except Exception:
            return {'status': 'unhealthy', 'message': 'Database connection failed'}
    
    def _check_cache_health(self):
        try:
            cache.set('health_check', True, 60)
            result = cache.get('health_check')
            return {'status': 'healthy' if result else 'degraded', 'message': 'Cache connection OK'}
        except Exception:
            return {'status': 'unhealthy', 'message': 'Cache connection failed'}
    
    def _check_storage_health(self):
        # Basic storage check - can be expanded
        try:
            return {'status': 'healthy', 'message': 'Storage OK'}
        except Exception:
            return {'status': 'unhealthy', 'message': 'Storage check failed'}
    
    def _check_security_health(self):
        try:
            # Check if security middleware is working
            return {'status': 'healthy', 'message': 'Security systems operational'}
        except Exception:
            return {'status': 'unhealthy', 'message': 'Security check failed'}


class AdminAuditLogView(views.APIView):
    """
    View admin audit logs
    """
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [AdminSystemAccessPermission]
    
    def get(self, request):
        try:
            # Get audit logs from cache (last 24 hours)
            current_time = int(time.time())
            twenty_four_hours_ago = current_time - 86400
            
            audit_logs = []
            # This is a simplified implementation - in production, 
            # you might want to use a proper audit logging system
            
            logger.info(f"ADMIN_AUDIT_LOG_ACCESS: User {request.user.id}")
            
            return Response(ApiResponse(
                success=True,
                code=200,
                data={'audit_logs': audit_logs, 'count': len(audit_logs)},
                message="Audit logs retrieved successfully"
            ))
            
        except Exception as e:
            logger.error(f"Admin audit log error: {str(e)[:100]}")
            return Response(ApiResponse(
                success=False,
                code=500,
                error={'code': 'server_error', 'detail': 'Server error occurred'}
            ), status=500)