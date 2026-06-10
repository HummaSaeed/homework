from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at', 'file_name', 'file_type', 'file_size']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'file_name', 'file_type', 'file_size']

    def create(self, validated_data):
        uploaded_file = validated_data['file']
        validated_data['uploaded_by'] = self.context['request'].user
        validated_data['file_name'] = uploaded_file.name
        validated_data['file_type'] = uploaded_file.content_type or ''
        validated_data['file_size'] = uploaded_file.size
        return super().create(validated_data)
