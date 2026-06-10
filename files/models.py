from django.db import models
from django.conf import settings


class UploadedFile(models.Model):
    file = models.FileField(upload_to='managed_files/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(help_text="Size in bytes")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} uploaded by {self.uploaded_by.username}"
