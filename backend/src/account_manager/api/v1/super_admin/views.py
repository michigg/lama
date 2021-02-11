import logging

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from account_manager.api.v1.super_admin.serializers import UserSerializer, MailSerializer
from account_manager.utils.mail_utils import WelcomeMailTemplateController, DeletionMailTemplateController

logger = logging.getLogger(__name__)


class SuperAdminUsersApi(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('username')


class SuperAdminUserApi(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'


class WelcomeMail(generics.RetrieveUpdateAPIView):
    serializer_class = MailSerializer

    def retrieve(self, request, *args, **kwargs):
        welcome_mail = WelcomeMailTemplateController()
        template = welcome_mail.get_template()
        # TODO: implement subject
        subject = "Test"
        data = {'subject': subject, 'template': template}
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        welcome_mail = WelcomeMailTemplateController()
        welcome_mail.save_template(serializer.data.get('template'))
        return Response(serializer.data)


class DeletionMail(generics.RetrieveUpdateAPIView):
    serializer_class = MailSerializer

    def retrieve(self, request, *args, **kwargs):
        deletion_mail = DeletionMailTemplateController()
        template = deletion_mail.get_template()
        subject = "Test"
        data = {'subject': subject, 'template': template}
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deletion_mail = DeletionMailTemplateController()
        deletion_mail.save_template(serializer.data.get('template'))
        return Response(serializer.data)
