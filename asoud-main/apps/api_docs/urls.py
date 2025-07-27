from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIEndpointsView.as_view(), name='api-docs'),
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
]