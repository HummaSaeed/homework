from rest_framework import viewsets, permissions
from .models import Subject
from .serializers import SubjectSerializer, SubjectDetailSerializer
from accounts.permissions import IsAdminRole


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    filterset_fields = ['teacher', 'school_class']
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return SubjectDetailSerializer
        return SubjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]
