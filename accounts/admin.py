from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherProfile, StudentProfile, PhoneOTP


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Teacher Profile'
    filter_horizontal = ['assigned_classes', 'assigned_subjects']


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'full_name', 'email', 'phone_number', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'full_name', 'email', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone_number', 'profile_image')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'last_login'), 'classes': ['collapse']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'email', 'role', 'password1', 'password2'),
        }),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == 'teacher':
                return [TeacherProfileInline]
            elif obj.role == 'student':
                return [StudentProfileInline]
        return []

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} users activated.')
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} users deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used']
    search_fields = ['phone_number']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
