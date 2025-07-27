import json
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.market.models import Market

@receiver(post_save, sender=Market)
def add_market_url_to_allowed_hosts(sender, instance, created, **kwargs):
    if created:
        pass
    elif not created and instance.status == 'published':
        if not instance.business_id:
            return
        
        # Security: Validate business_id before adding to ALLOWED_HOSTS
        import re
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', instance.business_id):
            return  # Invalid business_id format
            
        domain = (instance.business_id).lower() + '.' + 'asoud.ir'
        if domain in settings.ALLOWED_HOSTS:
            return
        
        # Security: Atomic update with file locking
        new_allowed_hosts = settings.ALLOWED_HOSTS + [domain]
        
        settings.ALLOWED_HOSTS = new_allowed_hosts
        ALLOWED_HOSTS_FILE = os.path.join(settings.BASE_DIR, 'allowed_hosts.json')
        
        # Security: Use file locking for atomic writes
        import fcntl
        try:
            with open(ALLOWED_HOSTS_FILE, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(new_allowed_hosts, f)
        except Exception as e:
            # Log error but don't crash
            import logging
            logging.error(f"Failed to update allowed_hosts.json: {e}")
