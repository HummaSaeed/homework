from django.db import models
from django.conf import settings


class StudentProgress(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Percentage, e.g. 95.50
    average_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Percentage, e.g. 88.20
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # e.g. 98.00
    subject_performance = models.JSONField(default=dict, blank=True)  # e.g. {"Math": 85, "Science": 90}
    monthly_progress = models.JSONField(default=dict, blank=True)  # e.g. {"Jan": 80, "Feb": 85}
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress Records'

    def __str__(self):
        return f"Progress for {self.student.username}"
