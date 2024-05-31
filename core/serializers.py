from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers

from .models import School, AccessKey




class CreateSchoolSerializer(UserCreateSerializer):
    
    class Meta(UserCreateSerializer.Meta):
        fields = ['id','email','password']
        
        
    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        self.instance = School.objects.create(**self.validated_data)
        self.instance.save()
        return self.instance
    


class SchoolSerializer(UserSerializer):
    
    class Meta(UserSerializer.Meta):
        fields = ['id','email']




class AccessKeySerializer(serializers.ModelSerializer):
    
    key = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    school = SchoolSerializer(read_only=True)    
    procured_at = serializers.DateTimeField(read_only=True)
    revoked_at = serializers.DateTimeField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    
    
    class Meta:
        model = AccessKey
        fields = ['id','key','school','status','procured_at','revoked_at','expires_at']
        
    def create(self, validated_data):
        school_id = self.context['school_id']
        
        if AccessKey.objects.filter(school_id=school_id, status='active').exists():
            raise serializers.ValidationError('School already has an active key')
        key = AccessKey.objects.create(school_id=school_id, **validated_data)
        return key
        

class AccessKeyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = ['status']
        
        
    def validate_status(self, value):
        if value not in ['expired','revoked']:
            raise serializers.ValidationError('Invalid status')
        return value
    
    
    def update(self, instance, validated_data):
        if validated_data['status'] == 'revoked':
            instance.revoked_at = timezone.now()
        instance.status = validated_data['status']
        instance.save()
        return instance
        