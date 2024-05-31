from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('schools', views.SchoolViewSet, basename='users')
router.register('keys', views.AccessKeyViewSet, basename='keys')

urlpatterns = [
    
    path('api/v1/', include(router.urls)),
    
]