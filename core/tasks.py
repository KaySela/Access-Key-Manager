from celery import shared_task
from django.utils import timezone
from .models import AccessKey
import logging


logger = logging.getLogger(__name__)

@shared_task
def check_expired_keys():
    print('getting all keys')
    keys = AccessKey.objects.all()
    print('Checking for expired keys')
    for key in keys:
        if key.status == 'active' and key.expires_at < timezone.now():
            key.status = 'expired'
            key.save()
            logger.info(f'Key {key.id} has expired')
            print(f'Key {key.id} has expired')
        else:
            print(f'Key {key.id} is still active')
            
    
    