from rest_framework import serializers
from .models import Homework
from subjects.serializers import SubjectDetailSerializer
from classes.serializers import SchoolClassSerializer
from accounts.serializers import UserSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Homework
        fields = [
            'id', 'title', 'description', 'instructions', 'category',
            'subject', 'school_class', 'teacher', 'assigned_to',
            'due_date', 'total_marks', 'attachment', 'status',
            'is_overdue', 'days_remaining', 'created_at', 'updated_at',
        ]
        read_only_fields = ['teacher', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        assigned_to = validated_data.pop('assigned_to', [])
        homework = Homework.objects.create(**validated_data)
        if assigned_to:
            homework.assigned_to.set(assigned_to)
        return homework


class HomeworkDetailSerializer(serializers.ModelSerializer):
    subject = SubjectDetailSerializer(read_only=True)
    school_class = SchoolClassSerializer(read_only=True)
    teacher = UserSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Homework
        fields = [
            'id', 'title', 'description', 'instructions', 'category',
            'subject', 'school_class', 'teacher', 'assigned_to',
            'due_date', 'total_marks', 'attachment', 'status',
            'is_overdue', 'days_remaining', 'created_at', 'updated_at',
        ]
