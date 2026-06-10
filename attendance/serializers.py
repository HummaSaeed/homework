from rest_framework import serializers
from .models import Attendance
from accounts.serializers import UserSerializer
from classes.serializers import SchoolClassSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'school_class', 'date', 'status', 'remarks', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AttendanceDetailSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    school_class = SchoolClassSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'school_class', 'date', 'status', 'remarks', 'created_at', 'updated_at']


class BulkAttendanceSerializer(serializers.Serializer):
    school_class = serializers.IntegerField()
    date = serializers.DateField()
    records = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        allow_empty=False
    )
    # records = [{"student": <id>, "status": "PRESENT", "remarks": ""}, ...]


class AttendanceReportSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    leave_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
