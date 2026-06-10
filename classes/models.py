from django.db import models


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=50, blank=True)
    class_teacher = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher_of')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='classes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        unique_together = ('class_name', 'section', 'school')

    def __str__(self):
        return f"{self.class_name} {self.section}" if self.section else self.class_name
