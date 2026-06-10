"""Models for homework management app."""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator


class Subject(models.Model):
    """Model for academic subjects."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class Homework(models.Model):
    """Model for homework assignments."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('graded', 'Graded'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_homeworks')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_to_homeworks', blank=True)
    
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    
    points = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])
    attachments = models.FileField(upload_to='homework_attachments/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date

    @property
    def days_remaining(self):
        if self.is_overdue:
            return 0
        delta = self.due_date - timezone.now()
        return delta.days


class Submission(models.Model):
    """Model for homework submissions."""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    score = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, 
                                  blank=True, related_name='graded_submissions')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['homework', 'student']
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return f"{self.homework.title} - {self.student.username}"

    @property
    def is_late(self):
        return self.submitted_at > self.homework.due_date

    @property
    def is_graded(self):
        return self.status == 'graded'
