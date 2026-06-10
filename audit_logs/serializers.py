from rest_framework import serializers
from .models import AuditLog
from accounts.serializers import UserSerializer


class AuditLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'timestamp', 'ip_address']
