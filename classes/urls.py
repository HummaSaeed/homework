from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolClassViewSet

router = DefaultRouter()
router.register('', SchoolClassViewSet, basename='class')

urlpatterns = [
    path('', include(router.urls)),
]
