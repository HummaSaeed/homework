from django.contrib import admin
from .models import SchoolClass


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'school', 'class_teacher')
    search_fields = ('class_name', 'section')
    list_filter = ('school',)
