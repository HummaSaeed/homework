from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Avg, Count, Q
from accounts.models import User
from homework.models import Homework
from submissions.models import Submission
from attendance.models import Attendance
from accounts.permissions import IsAdminRole, IsTeacherRole


class StudentReportView(APIView):
    """Detailed performance report for a single student."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = User.objects.get(pk=student_id, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=404)

        # Permission check: teachers/admins only, or own data
        if request.user.role == 'student' and request.user.pk != student.pk:
            return Response({'error': 'Permission denied.'}, status=403)

        submissions = Submission.objects.filter(student=student)
        graded = submissions.filter(status='REVIEWED').exclude(marks_obtained=None)
        avg_marks = graded.aggregate(avg=Avg('marks_obtained'))['avg'] or 0.0

        total_hw = Homework.objects.filter(assigned_to=student).count()
        submitted_hw = submissions.count()
        completion_rate = round((submitted_hw / total_hw) * 100, 2) if total_hw > 0 else 0.0

        # Attendance
        total_att = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='PRESENT').count()
        att_pct = round((present / total_att) * 100, 2) if total_att > 0 else 0.0

        # Subject-wise performance
        subject_perf = {}
        for sub in graded.values('homework__subject__name').annotate(avg=Avg('marks_obtained')):
            subject_perf[sub['homework__subject__name']] = round(sub['avg'], 2)

        return Response({
            'student': {
                'id': student.pk,
                'full_name': student.full_name,
                'username': student.username,
                'email': student.email,
            },
            'homework_completion_rate': completion_rate,
            'average_marks': round(avg_marks, 2),
            'attendance_percentage': att_pct,
            'subject_performance': subject_perf,
            'total_homework_assigned': total_hw,
            'total_submitted': submitted_hw,
            'total_graded': graded.count(),
        })


class ClassReportView(APIView):
    """Class-wide performance report for teachers/admins."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, class_id):
        if request.user.role == 'student':
            return Response({'error': 'Permission denied.'}, status=403)

        from classes.models import SchoolClass
        try:
            school_class = SchoolClass.objects.get(pk=class_id)
        except SchoolClass.DoesNotExist:
            return Response({'error': 'Class not found.'}, status=404)

        students = User.objects.filter(student_profile__school_class=school_class)
        student_reports = []
        for student in students:
            submissions = Submission.objects.filter(student=student)
            graded = submissions.filter(status='REVIEWED').exclude(marks_obtained=None)
            avg = graded.aggregate(avg=Avg('marks_obtained'))['avg'] or 0.0

            total_att = Attendance.objects.filter(student=student, school_class=school_class).count()
            present = Attendance.objects.filter(student=student, school_class=school_class, status='PRESENT').count()
            att_pct = round((present / total_att) * 100, 2) if total_att > 0 else 0.0

            student_reports.append({
                'student_id': student.pk,
                'student_name': student.full_name or student.username,
                'average_marks': round(avg, 2),
                'attendance_percentage': att_pct,
                'submissions': submissions.count(),
            })

        return Response({
            'class': str(school_class),
            'total_students': students.count(),
            'student_reports': student_reports,
        })


class SystemReportView(APIView):
    """System-wide analytics for admin."""
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({
            'users_by_role': {
                'admin': User.objects.filter(role='admin').count(),
                'teacher': User.objects.filter(role='teacher').count(),
                'student': User.objects.filter(role='student').count(),
            },
            'homework_stats': {
                'total': Homework.objects.count(),
                'published': Homework.objects.filter(status='PUBLISHED').count(),
                'draft': Homework.objects.filter(status='DRAFT').count(),
                'closed': Homework.objects.filter(status='CLOSED').count(),
            },
            'submission_stats': {
                'total': Submission.objects.count(),
                'reviewed': Submission.objects.filter(status='REVIEWED').count(),
                'pending': Submission.objects.filter(status='SUBMITTED').count(),
                'late': Submission.objects.filter(status='LATE').count(),
            },
            'average_marks_overall': Submission.objects.filter(
                status='REVIEWED'
            ).exclude(marks_obtained=None).aggregate(avg=Avg('marks_obtained'))['avg'] or 0.0,
        })
