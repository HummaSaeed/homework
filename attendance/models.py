from django.db import models
from django.conf import settings


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LEAVE', 'Leave'),
        ('LATE', 'Late'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'school_class', 'date']
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.student.username} - {self.school_class.name} - {self.date}: {self.status}"
