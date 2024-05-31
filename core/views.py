from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


from .models import School, AccessKey
from .serializers import CreateSchoolSerializer, SchoolSerializer, AccessKeySerializer, AccessKeyUpdateSerializer
from .permissions import IsAdminOrPostReadOnly, IsAdminOrReadOnly



class SchoolViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSchoolSerializer
        return SchoolSerializer
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return School.objects.all()
        return School.objects.filter(id=self.request.user.id)
    



class AccessKeyViewSet(ModelViewSet):
    
    http_method_names = ['get','post','patch']
    
    permission_classes = [IsAdminOrPostReadOnly]
    pagination_class = PageNumberPagination
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AccessKey.objects.all()
        return AccessKey.objects.filter(school_id=self.request.user.id)
    
    def get_serializer_context(self):
        return {'school_id': self.request.user.id}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AccessKeySerializer
        if self.request.method == 'PATCH':
            return AccessKeyUpdateSerializer
        return AccessKeySerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        access_key = serializer.save()
        serializer = AccessKeySerializer(access_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        serializer = AccessKeyUpdateSerializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        access_key = serializer.save()
        serializer = AccessKeySerializer(access_key)
        return Response(serializer.data, status=status.HTTP_200_OK) 






