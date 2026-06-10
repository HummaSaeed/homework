from rest_framework import viewsets, permissions
from .models import SchoolClass
from .serializers import SchoolClassSerializer, SchoolClassDetailSerializer
from accounts.permissions import IsAdminRole


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    filterset_fields = ['school', 'session']
    search_fields = ['name', 'section']

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return SchoolClassDetailSerializer
        return SchoolClassSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]
