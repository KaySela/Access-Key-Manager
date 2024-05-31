from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from uuid import uuid4


class School(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self) -> str:
        return self.email
    


class AccessKey(models.Model):
    
    KEY_STATUS = [('active', 'Active'), ('expired', 'Expired'),('revoked', 'Revoked')]
    
    key = models.UUIDField(default=uuid4, editable=False, unique=True)
    status = models.CharField(choices=KEY_STATUS, default='active', max_length=10)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='access_keys')
    procured_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.procured_at + timedelta(days=30)
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return str(self.key)
    
    class Meta:
        ordering = ['-procured_at']