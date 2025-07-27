from django.urls import path
from . import views

app_name = 'admin_security'

urlpatterns = [
    # Security and health endpoints
    path('security/status/', views.AdminSecurityStatusView.as_view(), name='security-status'),
    path('system/health/', views.AdminSystemHealthView.as_view(), name='system-health'),
    path('audit/logs/', views.AdminAuditLogView.as_view(), name='audit-logs'),
    
    # Dashboard and statistics
    path('dashboard/stats/', views.AdminDashboardStatsView.as_view(), name='dashboard-stats'),
    
    # User management endpoints
    path('users/', views.AdminUsersListView.as_view(), name='users-list'),
    path('users/<str:user_id>/', views.AdminUserDetailView.as_view(), name='user-detail'),
    path('users/<str:user_id>/toggle-active/', views.AdminUserToggleActiveView.as_view(), name='user-toggle-active'),
]