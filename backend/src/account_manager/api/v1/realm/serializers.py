import logging

from django.contrib.auth.models import Group
from rest_framework import serializers

from account_helper.models import Realm
from account_manager.models import LdapGroup

logger = logging.getLogger(__name__)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "permissions")
        read_only_fields = ("id", "permissions")
        extra_kwargs = {
            'name': {'validators': []},
        }


class RealmSerializer(serializers.ModelSerializer):
    admin_group = GroupSerializer(read_only=True)
    default_group = GroupSerializer(read_only=True)

    class Meta:
        model = Realm
        fields = "__all__"
        read_only_fields = ("id", "name", "email", "ldap_base_dn", "admin_group", "default_group")


class RealmUpdateSerializer(serializers.ModelSerializer):
    admin_group = GroupSerializer(default=None, allow_null=True, required=False)
    default_group = GroupSerializer(default=None, allow_null=True, required=False)

    class Meta:
        model = Realm
        fields = ("id", "name", "email", "ldap_base_dn", "admin_group", "default_group")

    def validate_default_group(self, value):
        realm_id = self.context["view"].kwargs.get("realm_id")
        realm = Realm.objects.get(id=realm_id)
        if value and not LdapGroup.group_exists(group_name=value['name'], realm=realm):
            raise serializers.ValidationError("LDAP Group with default group name not found")
        return value

    def validate_admin_group(self, value):
        realm_id = self.context["view"].kwargs.get("realm_id")
        realm = Realm.objects.get(id=realm_id)
        if value and not LdapGroup.group_exists(group_name=value['name'], realm=realm):
            raise serializers.ValidationError("LDAP Group with admin group name not found")
        return value

    def get_django_group(self, realm: Realm, group_name: str) -> Group:
        ldap_default_group = LdapGroup.get_group(group_name=group_name, realm=realm)
        return ldap_default_group.get_django_group()

    def update(self, instance, validated_data):
        # Required because ldapdb did not provide save method
        realm_id = self.context["view"].kwargs.get("realm_id")
        realm = Realm.objects.get(id=realm_id)

        admin_group = validated_data.get("admin_group")
        default_group = validated_data.get("default_group")

        admin_group_name = admin_group['name'] if admin_group else None
        default_group_name = default_group['name'] if admin_group else None

        instance.admin_group = self.get_django_group(realm=realm,
                                                     group_name=admin_group_name) if admin_group_name else instance.admin_group
        instance.default_group = self.get_django_group(realm=realm,
                                                       group_name=default_group_name) if default_group_name else instance.default_group

        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.ldap_base_dn = validated_data.get('ldap_base_dn', instance.ldap_base_dn)
        instance.save()
        return instance


class RealmCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realm
        fields = ("id", "name", "ldap_base_dn")
        read_only_fields = ("id",)


class ExtendedRealmSerializer(serializers.ModelSerializer):
    realm = RealmUpdateSerializer(read_only=True)
    user_count = serializers.IntegerField(read_only=True)
    group_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Realm
        fields = ("realm", "user_count", "group_count")
