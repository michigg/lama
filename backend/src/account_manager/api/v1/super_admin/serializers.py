from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
            'date_joined', 'groups', 'user_permissions')
        read_only_fields = (
            'id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'is_active',
            'date_joined', 'groups', 'user_permissions')


class MailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    template = serializers.CharField(max_length=32000)
