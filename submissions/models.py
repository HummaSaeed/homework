from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('REVIEWED', 'Reviewed'),
        ('LATE', 'Late'),
    ]

    homework = models.ForeignKey('homework.Homework', on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    uploaded_file = models.FileField(upload_to='submissions/')
    remarks = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submission_date']
        unique_together = ['homework', 'student']
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return f"{self.homework.title} - {self.student.username}"

    @property
    def is_late_submission(self):
        return self.submission_date > self.homework.due_date
