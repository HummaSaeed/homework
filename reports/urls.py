from django.urls import path
from .views import StudentReportView, ClassReportView, SystemReportView

urlpatterns = [
    path('student/<int:student_id>/', StudentReportView.as_view(), name='student-report'),
    path('class/<int:class_id>/', ClassReportView.as_view(), name='class-report'),
    path('system/', SystemReportView.as_view(), name='system-report'),
]
