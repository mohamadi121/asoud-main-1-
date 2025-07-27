from django.urls import path

from apps.market.views.owner_views import (
    MarketCreateAPIView,
    MarketGetAPIView,
    MarketUpdateAPIView,
    MarketListAPIView,
    MarketLocationCreateAPIView,
    MarketLocationGetAPIView,
    MarketLocationUpdateAPIView,
    MarketContactCreateAPIView,
    MarketContactGetAPIView,
    MarketContactUpdateAPIView,
    MarketInactiveAPIView,
    MarketQueueAPIView,
    MarketLogoAPIView,
    MarketBackgroundAPIView,
    MarketSliderAPIView,
    MarketThemeAPIView,
)

from apps.market.views.market_schedule import (
    MarketScheduleAPIView,
    MarketScheduleListView,
    MarketScheduleUpdateView,
    MarketScheduleDeleteView
)

app_name = 'market_owner'

urlpatterns = [
    # market itself
    path(
        'create/',
        MarketCreateAPIView.as_view(),
        name='create',
    ),
    path(
        'list/',
        MarketListAPIView.as_view(),
        name='list',
    ),
    path(
        '<str:pk>/',
        MarketGetAPIView.as_view(),
        name='get',
    ),
    path(
        'update/<str:pk>/',
        MarketUpdateAPIView.as_view(),
        name='update',
    ),
    
    # market location
    path(
        'location/create/',
        MarketLocationCreateAPIView.as_view(),
        name='location-create',
    ),
    path(
        'location/<str:pk>/',
        MarketLocationGetAPIView.as_view(),
        name='location-get',
    ),
    path(
        'location/update/<str:pk>/',
        MarketLocationUpdateAPIView.as_view(),
        name='location-update',
    ),
    
    # market contact
    path(
        'contact/create/',
        MarketContactCreateAPIView.as_view(),
        name='contact-create',
    ),
    path(
        'contact/<str:pk>/',
        MarketContactGetAPIView.as_view(),
        name='contact-get',
    ),
    path(
        'contact/update/<str:pk>/',
        MarketContactUpdateAPIView.as_view(),
        name='contact-update',
    ),

    # market state
    path(
        'inactive/<str:pk>/',
        MarketInactiveAPIView.as_view(),
        name='inactive',
    ),
    path(
        'queue/<str:pk>/',
        MarketQueueAPIView.as_view(),
        name='queue',
    ),

    # market ui
    path(
        'logo/<str:pk>/',
        MarketLogoAPIView.as_view(),
        name='logo',
    ),
    path(
        'background/<str:pk>/',
        MarketBackgroundAPIView.as_view(),
        name='background',
    ),
    path(
        'slider/<str:pk>/',
        MarketSliderAPIView.as_view(),
        name='slider',
    ),
    path(
        'theme/<str:pk>/',
        MarketThemeAPIView.as_view(),
        name='theme',
    ),

    # schedule
    path(
        'schedules/create/',
        MarketScheduleAPIView.as_view(),
        name='schedule-create',
    ),
    path(
        'schedules/list/',
        MarketScheduleListView.as_view(),
        name='schedule-list',
    ),
    path(
        'schedules/<str:pk>/update/',
        MarketScheduleUpdateView.as_view(),
        name='schedule-update',
    ),
    path(
        'schedules/<str:pk>/delete/',
        MarketScheduleDeleteView.as_view(),
        name='schedule-delete',
    ),
]
