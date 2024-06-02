from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from .models import School, AccessKey
from .serializers import CreateSchoolSerializer, SchoolSerializer, AccessKeySerializer, AccessKeyUpdateSerializer, SchoolEmailSerializer
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
    
    @method_decorator(cache_page(60*15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @method_decorator(cache_page(60*15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



class AccessKeyViewSet(ModelViewSet):
    
    http_method_names = ['get','post']
    
    permission_classes = [IsAdminOrPostReadOnly]
    pagination_class = PageNumberPagination
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            school_id = self.kwargs.get('school_pk', None)
            if school_id:
                return AccessKey.objects.select_related('school').filter(school_id=self.kwargs['school_pk'])
            return AccessKey.objects.select_related('school').all()
        return AccessKey.objects.select_related('school').filter(school_id=self.request.user.id)
    
    def get_serializer_context(self):
        school_id = self.kwargs.get('school_pk', None)
        if school_id:
            return {'school_id': school_id}
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
    
    
    @action(detail=True, methods=['post'], url_path='revoke', url_name='revoke', permission_classes=[IsAdminUser])
    def revoke_key(self, request, pk=None, school_pk=None):
        access_key = self.get_object()
        serializer = AccessKeyUpdateSerializer(access_key, data={'status':'revoked'}, partial=True)
        serializer.is_valid(raise_exception=True)
        revoked_key = serializer.save()
        serializer = AccessKeySerializer(revoked_key)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @method_decorator(cache_page(60*15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @method_decorator(cache_page(60*15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    

class SchoolActiveKeyView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAdminUser]
    
    def post(self, request, format=None):
        serializer = SchoolEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            school = School.objects.select_related('school').filter(email=email).first()
            if school:
                active_key = AccessKey.objects.select_related('school').filter(school=school, status='active').first()
                if not active_key:
                    return Response({'error':'No active key found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = AccessKeySerializer(active_key)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'School not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


