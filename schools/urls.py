from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, AcademicSessionViewSet

router = DefaultRouter()
router.register('sessions', AcademicSessionViewSet, basename='session')
router.register('', SchoolViewSet, basename='school')

urlpatterns = [
    path('', include(router.urls)),
]
