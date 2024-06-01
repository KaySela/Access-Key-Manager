from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('schools', views.SchoolViewSet, basename='users')
router.register('keys', views.AccessKeyViewSet, basename='keys')

school_router = routers.NestedSimpleRouter(router, 'schools', lookup='school')
school_router.register('keys', views.AccessKeyViewSet, basename='school-keys')

urlpatterns = [
    
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(school_router.urls)),
    path('api/v1/activekey/<str:email>/', views.SchoolActiveKeyView.as_view(), name='school-active-key'),
    
]
