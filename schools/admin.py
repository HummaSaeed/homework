from django.contrib import admin
from .models import School, AcademicSession


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'principal_name')
    search_fields = ('name', 'principal_name')


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
