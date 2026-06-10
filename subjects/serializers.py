from rest_framework import serializers
from .models import Subject
from accounts.serializers import UserSerializer
from classes.serializers import SchoolClassSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'teacher', 'school_class', 'created_at', 'updated_at']


class SubjectDetailSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    school_class = SchoolClassSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'teacher', 'school_class', 'created_at', 'updated_at']
