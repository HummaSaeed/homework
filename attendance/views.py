from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceDetailSerializer, BulkAttendanceSerializer
from accounts.permissions import IsTeacherRole, IsAdminRole
from classes.models import SchoolClass
from accounts.models import User


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('student', 'school_class').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school_class', 'date', 'status', 'student']
    search_fields = ['student__full_name', 'student__username']
    ordering_fields = ['date']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return AttendanceDetailSerializer
        return AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_mark']:
            return [IsTeacherRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            return qs.filter(student=user)
        elif user.role == 'teacher':
            # Teachers see attendance for their assigned classes
            try:
                assigned_classes = user.teacher_profile.assigned_classes.all()
                return qs.filter(school_class__in=assigned_classes)
            except Exception:
                return qs.none()
        return qs  # Admin sees all

    @action(detail=False, methods=['post'], permission_classes=[IsTeacherRole])
    def bulk_mark(self, request):
        """Mark attendance for an entire class in one request."""
        serializer = BulkAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            school_class = SchoolClass.objects.get(pk=data['school_class'])
        except SchoolClass.DoesNotExist:
            return Response({'error': 'Class not found.'}, status=status.HTTP_404_NOT_FOUND)

        created, updated = 0, 0
        errors = []
        for record in data['records']:
            try:
                student_id = int(record['student'])
                record_status = record.get('status', 'PRESENT')
                remarks = record.get('remarks', '')
                student = User.objects.get(pk=student_id, role='student')
                obj, was_created = Attendance.objects.update_or_create(
                    student=student,
                    school_class=school_class,
                    date=data['date'],
                    defaults={'status': record_status, 'remarks': remarks}
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
            except User.DoesNotExist:
                errors.append(f"Student {record.get('student')} not found.")
            except Exception as e:
                errors.append(str(e))

        return Response({
            'message': f'Attendance saved. Created: {created}, Updated: {updated}',
            'errors': errors
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def student_report(self, request):
        """Get attendance percentage report for a student."""
        student_id = request.query_params.get('student_id')
        school_class_id = request.query_params.get('school_class_id')
        month = request.query_params.get('month')  # format: YYYY-MM

        if not student_id:
            return Response({'error': 'student_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        qs = Attendance.objects.filter(student_id=student_id)
        if school_class_id:
            qs = qs.filter(school_class_id=school_class_id)
        if month:
            year, m = month.split('-')
            qs = qs.filter(date__year=year, date__month=m)

        total = qs.count()
        present = qs.filter(status='PRESENT').count()
        absent = qs.filter(status='ABSENT').count()
        leave = qs.filter(status='LEAVE').count()
        late = qs.filter(status='LATE').count()
        percentage = round((present / total) * 100, 2) if total > 0 else 0.0

        return Response({
            'student_id': student_id,
            'total_days': total,
            'present_days': present,
            'absent_days': absent,
            'leave_days': leave,
            'late_days': late,
            'attendance_percentage': percentage,
        })
