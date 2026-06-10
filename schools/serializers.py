from rest_framework import serializers
from .models import School, AcademicSession


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['id', 'school', 'title', 'start_date', 'end_date', 'active']


class SchoolSerializer(serializers.ModelSerializer):
    sessions = AcademicSessionSerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'logo', 'address', 'phone', 'email', 'principal_name', 'sessions']
