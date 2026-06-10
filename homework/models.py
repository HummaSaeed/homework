from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator


class Homework(models.Model):
    CATEGORY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('SUMMER_VACATION', 'Summer Vacation'),
        ('PROJECT', 'Project'),
        ('QUIZ', 'Quiz'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='DAILY')
    
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='homeworks')
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_homeworks')
    
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_to_homeworks', blank=True)
    
    due_date = models.DateTimeField()
    total_marks = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])
    attachment = models.FileField(upload_to='homework_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
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
