from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from account_helper.models import Realm
from account_manager.api.v1.group.serializers import LdapGroupSerializer
from account_manager.models import LdapGroup
import logging

logger = logging.getLogger(__name__)


class RealmGroupsApi(generics.ListCreateAPIView):
    serializer_class = LdapGroupSerializer

    # TODO: Extract MIXIN
    def get_realm(self):
        realm_id = self.kwargs.get('realm_id')
        if not realm_id:
            raise ValidationError("Realm Id is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        return realms[0]

    def get_queryset(self):
        realm = self.get_realm()
        ldap_groups = LdapGroup.get_groups(realm=realm)
        return ldap_groups


class RealmGroupApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LdapGroupSerializer
    lookup_field = 'dn'
    lookup_url_kwarg = 'group_dn'

    def get_group(self, realm):
        group_dn = self.kwargs.get('group_dn')
        ldap_group = LdapGroup.get_group(group_dn=group_dn, realm=realm)
        if not ldap_group:
            raise ValidationError("Could not retrieve group")
        return ldap_group

    def get_realm(self):
        realm_id = self.kwargs.get('realm_id')
        if not realm_id:
            raise ValidationError("Realm Id is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        return realms[0]

    def get_object(self):
        return self.get_queryset()

    def get_queryset(self):
        realm = self.get_realm()
        ldap_group = self.get_group(realm)
        logger.error(ldap_group)
        return ldap_group

    def perform_destroy(self, instance):
        realm = self.get_realm()
        instance.full_delete(realm)
