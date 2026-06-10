from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Avg, Q
from accounts.models import User
from schools.models import School
from classes.models import SchoolClass
from subjects.models import Subject
from homework.models import Homework
from submissions.models import Submission
from attendance.models import Attendance
from notifications.models import Notification


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required.'}, status=403)

        return Response({
            'total_schools': School.objects.count(),
            'total_teachers': User.objects.filter(role='teacher').count(),
            'total_students': User.objects.filter(role='student').count(),
            'total_classes': SchoolClass.objects.count(),
            'total_subjects': Subject.objects.count(),
            'total_homework': Homework.objects.count(),
            'homework_by_status': {
                'DRAFT': Homework.objects.filter(status='DRAFT').count(),
                'PUBLISHED': Homework.objects.filter(status='PUBLISHED').count(),
                'CLOSED': Homework.objects.filter(status='CLOSED').count(),
            },
            'total_submissions': Submission.objects.count(),
            'submissions_by_status': {
                'SUBMITTED': Submission.objects.filter(status='SUBMITTED').count(),
                'REVIEWED': Submission.objects.filter(status='REVIEWED').count(),
                'LATE': Submission.objects.filter(status='LATE').count(),
            },
            'recent_users': list(User.objects.order_by('-created_at')[:5].values(
                'id', 'username', 'full_name', 'role', 'created_at'
            )),
        })


class TeacherDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'teacher':
            return Response({'error': 'Teacher access required.'}, status=403)

        teacher = request.user
        homeworks = Homework.objects.filter(teacher=teacher)
        submissions = Submission.objects.filter(homework__teacher=teacher)

        try:
            assigned_classes = teacher.teacher_profile.assigned_classes.all()
        except Exception:
            assigned_classes = SchoolClass.objects.none()

        return Response({
            'total_students': User.objects.filter(
                student_profile__school_class__in=assigned_classes
            ).count(),
            'total_classes': assigned_classes.count(),
            'total_homework': homeworks.count(),
            'homework_by_status': {
                'DRAFT': homeworks.filter(status='DRAFT').count(),
                'PUBLISHED': homeworks.filter(status='PUBLISHED').count(),
                'CLOSED': homeworks.filter(status='CLOSED').count(),
            },
            'pending_reviews': submissions.filter(status='SUBMITTED').count(),
            'total_submissions': submissions.count(),
            'recent_homework': list(homeworks.order_by('-created_at')[:5].values(
                'id', 'title', 'status', 'due_date', 'created_at'
            )),
            'recent_submissions': list(submissions.order_by('-submission_date')[:5].values(
                'id', 'student__username', 'homework__title', 'status', 'submission_date'
            )),
        })


class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student':
            return Response({'error': 'Student access required.'}, status=403)

        student = request.user
        assigned = Homework.objects.filter(assigned_to=student, status='PUBLISHED')
        submissions = Submission.objects.filter(student=student)
        submitted_ids = submissions.values_list('homework_id', flat=True)

        # Attendance stats
        total_attendance = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(student=student, status='PRESENT').count()
        attendance_pct = round((present_count / total_attendance) * 100, 2) if total_attendance > 0 else 0.0

        # Average marks
        graded = submissions.filter(status='REVIEWED').exclude(marks_obtained=None)
        avg_marks = graded.aggregate(avg=Avg('marks_obtained'))['avg'] or 0.0

        pending = assigned.exclude(id__in=submitted_ids)
        unread_notif = Notification.objects.filter(user=student, is_read=False).count()

        return Response({
            'assigned_homework': assigned.count(),
            'submitted_homework': submissions.count(),
            'pending_homework': pending.count(),
            'attendance_percentage': attendance_pct,
            'average_marks': round(avg_marks, 2),
            'unread_notifications': unread_notif,
            'recent_homework': list(assigned.order_by('-due_date')[:5].values(
                'id', 'title', 'due_date', 'status', 'total_marks'
            )),
            'recent_submissions': list(submissions.order_by('-submission_date')[:5].values(
                'id', 'homework__title', 'status', 'marks_obtained', 'submission_date'
            )),
        })
