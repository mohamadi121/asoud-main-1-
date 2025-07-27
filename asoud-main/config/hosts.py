from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    #host(r'', 'config.urls', name='main'),
    host(r'app', 'config.app_urls', name='app'),
    host(r'(?P<market_id>[a-zA-Z0-9_-]{3,20})', 'config.market_urls', name='market'),  # Security: Strict validation
    host(r'', 'config.urls', name='main'),
)
