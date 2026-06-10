from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Homework
from .serializers import HomeworkSerializer, HomeworkDetailSerializer
from accounts.permissions import IsAdminRole, IsTeacherRole, IsStudentRole
from notifications.utils import create_notification


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.select_related('subject', 'school_class', 'teacher').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'subject', 'school_class']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'total_marks']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return HomeworkDetailSerializer
        return HomeworkSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish', 'duplicate']:
            return [IsTeacherRole() if not IsAdminRole().has_permission(self.request, self) else IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            # Students only see PUBLISHED homework assigned to them
            return qs.filter(assigned_to=user, status='PUBLISHED')
        elif user.role == 'teacher':
            # Teachers see their own homework
            return qs.filter(teacher=user)
        return qs  # Admins see everything

    def perform_create(self, serializer):
        homework = serializer.save(teacher=self.request.user)
        # Notify assigned students
        for student in homework.assigned_to.all():
            create_notification(
                user=student,
                title="New Homework Assigned",
                message=f"You have been assigned: {homework.title}. Due: {homework.due_date.strftime('%Y-%m-%d')}"
            )

    @action(detail=True, methods=['post'], permission_classes=[IsTeacherRole])
    def publish(self, request, pk=None):
        homework = self.get_object()
        homework.status = 'PUBLISHED'
        homework.save()
        # Notify all assigned students
        for student in homework.assigned_to.all():
            create_notification(
                user=student,
                title="Homework Published",
                message=f"'{homework.title}' has been published. Due: {homework.due_date.strftime('%Y-%m-%d')}"
            )
        return Response({'message': 'Homework published successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[IsTeacherRole])
    def close(self, request, pk=None):
        homework = self.get_object()
        homework.status = 'CLOSED'
        homework.save()
        return Response({'message': 'Homework closed.'})

    @action(detail=True, methods=['post'], permission_classes=[IsTeacherRole])
    def duplicate(self, request, pk=None):
        homework = self.get_object()
        original_assigned = list(homework.assigned_to.all())
        homework.pk = None
        homework.title = f"Copy of {homework.title}"
        homework.status = 'DRAFT'
        homework.save()
        homework.assigned_to.set(original_assigned)
        serializer = HomeworkSerializer(homework, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
