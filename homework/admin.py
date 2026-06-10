"""Admin configuration for homework management app."""

from django.contrib import admin
from .models import Subject, Homework, Submission


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'assigned_by', 'due_date', 'status')
    search_fields = ('title', 'subject__name')
    list_filter = ('status', 'subject', 'due_date')
    readonly_fields = ('assigned_date', 'created_at', 'updated_at')
    filter_horizontal = ('assigned_to',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject')
        }),
        ('Assignment Details', {
            'fields': ('assigned_by', 'assigned_to', 'due_date', 'points')
        }),
        ('Files', {
            'fields': ('attachments',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('assigned_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submitted_at', 'status', 'score')
    search_fields = ('homework__title', 'student__username')
    list_filter = ('status', 'submitted_at')
    readonly_fields = ('submitted_at', 'created_at', 'updated_at')
    fieldsets = (
        ('Submission', {
            'fields': ('homework', 'student', 'submission_file')
        }),
        ('Grading', {
            'fields': ('score', 'feedback', 'graded_by', 'status')
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'graded_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
