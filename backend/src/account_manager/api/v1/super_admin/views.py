import logging

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from account_manager.api.v1.super_admin.serializers import UserSerializer

logger = logging.getLogger(__name__)


class SuperAdminUserApi(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
