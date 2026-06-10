from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name or self.username


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    assigned_classes = models.ManyToManyField('classes.SchoolClass', blank=True)
    qualification = models.CharField(max_length=255, blank=True)
    subject_specialization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Teacher: {self.user}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, blank=True)
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    section = models.CharField(max_length=50, blank=True)
    parent_phone = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user}"


class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['phone_number', 'code'])]

    def __str__(self):
        return f"OTP {self.code} for {self.phone_number}"
