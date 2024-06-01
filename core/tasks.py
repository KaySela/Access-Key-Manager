from celery import shared_task
from django.utils import timezone
from .models import AccessKey



@shared_task
def check_expired_keys():
    keys = AccessKey.objects.all()
    for key in keys:
        if key.status == 'active' and key.expires_at < timezone.now():
            key.status = 'expired'
            key.save()
    