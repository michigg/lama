import logging

from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account_helper.models import DeletedUser, Realm
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.user_views import get_protocol

logger = logging.getLogger(__name__)


class LdapGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdapGroup
        fields = '__all__'


class LdapUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdapUser
        fields = (
            'dn', 'email', 'username', 'display_name', 'first_name', 'last_name', 'phone', 'mobile_phone',
            'last_login')
        read_only_fields = ('dn', 'password', 'last_login', 'display_name')
        extra_kwargs = {'username': {'validators': []}}

    def create(self, validated_data):
        request = self.context["request"]
        realm_id = self.context["view"].kwargs.get("realm_id")
        if not realm_id:
            raise ValidationError("Realm id is required")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")

        current_site = get_current_site(request)
        protocol = get_protocol(request=request)

        return LdapUser.create_with_django_user_creation_and_welcome_mail(realm=realms[0],
                                                                          protocol=protocol,
                                                                          domain=current_site.domain,
                                                                          username=validated_data.get('username'),
                                                                          email=validated_data.get('email'))


class DeletedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedUser
        fields = '__all__'


class ExtendedUserSerializer(serializers.Serializer):
    user = LdapUserSerializer()
    deleted_user = DeletedUserSerializer(read_only=True)
    groups = LdapGroupSerializer(read_only=True, many=True)
    active = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        ldap_user = instance['user']
        user_validated_data = validated_data['user']

        LdapUser.update_user(ldap_user, user_validated_data)
        return instance
