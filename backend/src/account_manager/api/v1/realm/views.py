import logging
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
from socket import timeout

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account_helper.models import Realm
from account_manager.api.v1.permissions import RealmAdminPermission
from account_manager.utils.mail_utils import realm_send_mail
from account_manager.utils.main_views import get_group_user_count_wrapper
from .serializers import ExtendedRealmSerializer, RealmUpdateSerializer, RealmCreateSerializer

logger = logging.getLogger(__name__)


class RealmsApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]
    serializer_class = ExtendedRealmSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExtendedRealmSerializer
        if self.request.method == 'POST':
            return RealmCreateSerializer
        return ExtendedRealmSerializer

    def get_queryset(self):
        django_user = self.request.user
        if django_user.is_superuser:
            realms = Realm.objects.order_by('name').all()
        else:
            realms = Realm.objects.filter(admin_group__user__username__contains=django_user.username).order_by('name')
        if realms:
            return [get_group_user_count_wrapper(realm) for realm in realms]
        return realms

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise ValidationError("Realm creation requires super user privileges")
        return super().create(request, args, kwargs)


class RealmApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Realm.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "realm_id"
    serializer_class = RealmUpdateSerializer


class MailTestingApi(APIView):
    def post(self, request):
        realm_id = self.kwargs.get('realm_id')
        realm = Realm.objects.get(id=realm_id)
        test_msg = f'Du hast die Mail Konfiguration für {realm.name} erfolgreich abgeschlossen.'
        success_msg = 'Test erfolgreich'
        error_msg_auth = f'Mail konnte nicht versendet werden, Anmeldedaten inkorrekt.'
        error_msg_connect = f'Mail konnte nicht versendet werden. Verbindungsaufbau abgelehnt. ' \
                            f'Bitte überprüfen sie die Server Addresse und den Port'
        error_msg_timeout = f'Mail konnte nicht versendet werden. Zeitüberschreitung beim Verbindungsaufbau. ' \
                            f'Bitte überprüfen sie die Server Addresse und den Port'
        error_msg_smtp = f'Mail konnte nicht versendet werden. Bitte kontaktieren sie den Administrator'
        try:
            realm_send_mail(realm, realm.email, f'{realm.name} Test Mail', test_msg)
        except SMTPAuthenticationError:
            return Response({'msg': error_msg_auth}, status=status.HTTP_401_UNAUTHORIZED)
        except SMTPConnectError:
            return Response({'msg': error_msg_connect}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except timeout:
            return Response({'msg': error_msg_timeout}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except SMTPException:
            return Response({'msg': error_msg_smtp}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': success_msg}, status=status.HTTP_201_CREATED)
