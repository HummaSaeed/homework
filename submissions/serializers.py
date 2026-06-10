from rest_framework import serializers
from .models import Submission
from accounts.serializers import UserSerializer
from homework.serializers import HomeworkSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    is_late_submission = serializers.ReadOnlyField()

    class Meta:
        model = Submission
        fields = [
            'id', 'homework', 'student', 'uploaded_file', 'remarks',
            'submission_date', 'marks_obtained', 'feedback', 'status',
            'is_late_submission', 'created_at', 'updated_at',
        ]
        read_only_fields = ['student', 'submission_date', 'marks_obtained', 'feedback', 'status', 'created_at', 'updated_at']


class SubmissionDetailSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    homework = HomeworkSerializer(read_only=True)
    is_late_submission = serializers.ReadOnlyField()

    class Meta:
        model = Submission
        fields = [
            'id', 'homework', 'student', 'uploaded_file', 'remarks',
            'submission_date', 'marks_obtained', 'feedback', 'status',
            'is_late_submission', 'created_at', 'updated_at',
        ]


class GradeSubmissionSerializer(serializers.Serializer):
    marks_obtained = serializers.IntegerField(min_value=0)
    feedback = serializers.CharField(required=False, allow_blank=True)
