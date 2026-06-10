from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='schools/logos/', null=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    principal_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Schools'

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='sessions')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.school.name} - {self.name}"
