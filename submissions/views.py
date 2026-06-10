from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionDetailSerializer, GradeSubmissionSerializer
from accounts.permissions import IsTeacherRole, IsStudentRole
from notifications.utils import create_notification


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related('homework', 'student').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'homework']
    search_fields = ['student__full_name', 'homework__title']
    ordering_fields = ['submission_date', 'marks_obtained']
    ordering = ['-submission_date']
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return SubmissionDetailSerializer
        return SubmissionSerializer

    def get_permissions(self):
        if self.action in ['grade']:
            return [IsTeacherRole()]
        if self.action in ['create', 'update', 'partial_update']:
            return [IsStudentRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            return qs.filter(student=user)
        elif user.role == 'teacher':
            return qs.filter(homework__teacher=user)
        return qs  # Admin sees all

    def perform_create(self, serializer):
        homework = serializer.validated_data['homework']
        existing = Submission.objects.filter(homework=homework, student=self.request.user).first()
        
        if existing:
            # Resubmit: update existing submission
            existing.uploaded_file = serializer.validated_data['uploaded_file']
            existing.remarks = serializer.validated_data.get('remarks', '')
            existing.status = 'SUBMITTED'
            existing.save()
        else:
            submission = serializer.save(student=self.request.user)
            # Notify teacher
            create_notification(
                user=homework.teacher,
                title="New Homework Submission",
                message=f"{self.request.user.full_name or self.request.user.username} submitted '{homework.title}'"
            )

    @action(detail=True, methods=['post'], permission_classes=[IsTeacherRole])
    def grade(self, request, pk=None):
        submission = self.get_object()
        serializer = GradeSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            marks = serializer.validated_data['marks_obtained']
            feedback = serializer.validated_data.get('feedback', '')
            if marks > submission.homework.total_marks:
                return Response(
                    {'error': f'Marks cannot exceed total marks ({submission.homework.total_marks})'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            submission.marks_obtained = marks
            submission.feedback = feedback
            submission.status = 'REVIEWED'
            submission.save()
            # Notify student
            create_notification(
                user=submission.student,
                title="Homework Graded",
                message=f"Your submission for '{submission.homework.title}' has been graded. Score: {marks}/{submission.homework.total_marks}"
            )
            return Response({'message': 'Submission graded successfully.', 'marks_obtained': marks})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
