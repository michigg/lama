import logging

from _ldap import OBJECT_CLASS_VIOLATION
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404, HttpRequest
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account_helper.models import Realm, DeletedUser
from account_manager.api.v1.permissions import RealmAdminPermission
from account_manager.api.v1.user.serializers import LdapUserSerializer, ExtendedUserSerializer
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.django_user import update_django_user
from account_manager.utils.mail_utils import send_welcome_mail, send_deletion_mail
from account_manager.utils.user_views import get_protocol

logger = logging.getLogger(__name__)


class RealmUsersApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExtendedUserSerializer
        if self.request.method == 'POST':
            return LdapUserSerializer
        return LdapUserSerializer

    def get_queryset(self):
        realm_id = self.kwargs.get('realm_id')
        if not realm_id:
            raise ValidationError("Realm Id is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        realm = realms[0]
        ldap_users = LdapUser.get_users(realm=realm)
        ldap_user_wrappers = [LdapUser.get_extended_user(user) for user in ldap_users]
        return ldap_user_wrappers


class RealmUserApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]
    serializer_class = ExtendedUserSerializer
    queryset = LdapUser.get_users()
    lookup_field = "dn"
    lookup_url_kwarg = "user_dn"

    def get_object(self):
        realm_id = self.kwargs.get('realm_id')
        user_dn = self.kwargs.get('user_dn')

        if not realm_id:
            raise ValidationError("Realm Id is required")
        if not user_dn:
            raise ValidationError("User dn is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        realm = realms[0]
        ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
        if not ldap_user:
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, ldap_user)
        user_wrapper = LdapUser.get_extended_user(ldap_user)
        # TODO: maybe also relevant on user list
        groups = LdapGroup.get_user_groups(realm=realm, ldap_user=ldap_user)
        user_wrapper['groups'] = groups

        return user_wrapper

    def user_delete_controller(self, ldap_user: LdapUser, realm: Realm):
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        try:
            django_user = User.objects.get(username=ldap_user.username)
            try:
                user = DeletedUser.objects.create(user=django_user, ldap_dn=ldap_user.dn)
                logger.warning(user)
                # TODO: more feedback from mail
                send_deletion_mail(realm=realm, user=ldap_user)
                return Response({'msg': 'Nutzer wurde als gelöscht markiert.'}, status=status.HTTP_200_OK)
            except IntegrityError as err:
                logger.error(err)
                return Response({'msg': 'Nutzer ist bereits als gelöscht markiert.'}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist as err:
            logger.error(err)
            return Response({'msg': 'Nutzer existiert nicht.'}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, *args, **kwargs):
        realm_id = self.kwargs.get('realm_id')
        if not realm_id:
            raise ValidationError("Realm Id is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        realm = realms[0]

        ldap_user_wrapper = self.get_object()
        logger.error(ldap_user_wrapper)
        ldap_user = ldap_user_wrapper['user']
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        if ldap_user.is_deleteable_user(realm):
            try:
                if request.query_params.get('force'):
                    username = ldap_user.username
                    ldap_user.delete_complete()
                    return Response({'msg': f'Nutzer {username} wurde erfolgreich gelöscht.'},
                                    status=status.HTTP_200_OK)
                return self.user_delete_controller(ldap_user=ldap_user, realm=realm)
            except OBJECT_CLASS_VIOLATION:
                return Response({'msg': f'Der Nutzer {ldap_user.username} konnte nicht gelöscht werden, '
                                        f'da er der letzte Nutzer einer Gruppe ist. '
                                        f'Bitte lösche die Gruppe zuerst oder trage einen anderen Nutzer '
                                        f'in die Gruppe ein.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': f'Der Nutzer, {ldap_user.username}, gehört anscheinend zu den Admins. '
                                    f'Solange der Nutzer dieser Gruppe angehört kann dieser nicht gelöscht werden. '
                                    f'Bitte trage vorher den Nutzer aus der Admin Gruppe aus.'},
                            status=status.HTTP_400_BAD_REQUEST)


class RealmUserPasswordResetMail(APIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]

    def post(self, request):
        realm_id = self.kwargs.get('realm_id')
        user_dn = self.kwargs.get('user_dn')

        realm = Realm.objects.get(id=realm_id)
        ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
        try:
            if ldap_user.email:
                logger.info(f"Sending email to {ldap_user.email}")
                form = PasswordResetForm({'email': ldap_user.email})
                if form.is_valid():
                    logger.info('CREATE REQUEST')
                    pw_reset_request = HttpRequest()
                    pw_reset_request.META['SERVER_NAME'] = get_current_site(request).domain
                    pw_reset_request.META['SERVER_PORT'] = '80'
                    if request.is_secure():
                        pw_reset_request.META['SERVER_PORT'] = '443'
                    logger.info('form.save')
                    form.save(
                        request=pw_reset_request,
                        use_https=True,
                        from_email=realm.email,
                        email_template_name='registration/password_reset_email.html')
                    return Response({'msg': 'Die Passwort zurücksetzen E-Mail wurde erfolgreich versendet.'},
                                    status=status.HTTP_201_CREATED)
                return Response({'msg': 'Der Nutzer E-Mail Addresse ist ungültig. Es wurde keine E-Mail übermittelt.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg': 'Der Nutzer besitzt keine E-Mail Addresse. '
                                    'Bitte tragen Sie diese nach und probieren es erneut'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logger.error(f'Error: {err}')
            return Response({'msg': 'Die Passwort zurücksetzen E-Mail konnte nicht versendet werden.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class RealmUserWelcomeMail(APIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]

    def post(self, request):
        realm_id = self.kwargs.get('realm_id')
        user_dn = self.kwargs.get('user_dn')

        realm = Realm.objects.get(id=realm_id)
        ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)

        update_django_user(ldap_user)
        current_site = get_current_site(request)
        protocol = get_protocol(request)
        send_welcome_mail(domain=current_site.domain,
                          email=ldap_user.email,
                          protocol=protocol,
                          realm=realm,
                          user=User.objects.get(username=ldap_user.username))
        return Response({'msg': 'Willkommensmail erfolgreich versendet.'}, status=status.HTTP_201_CREATED)


class RealmUserDeleteCancel(APIView):
    permission_classes = [IsAuthenticated, RealmAdminPermission]

    def get(self, request):
        user_dn = self.kwargs.get('user_dn')

        try:
            deleted_user = DeletedUser.objects.get(ldap_dn=user_dn)
            deleted_user.delete()
        except ObjectDoesNotExist:
            return Response({'msg': 'Nutzer ist nicht als gelöscht markiert.'}, status=status.HTTP_409_CONFLICT)
        return Response({'msg': 'Nutzerlöschung wurde abgebrochen.'}, status=status.HTTP_204_NO_CONTENT)
