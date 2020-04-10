from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import raise_errors_on_nested_writes

from account_helper.models import Realm
from account_manager.models import LdapGroup


class LdapGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdapGroup
        fields = ('dn', 'name', 'description', 'members')
        read_only_fields = ('dn',)
        extra_kwargs = {'description': {'required': False}}

    def create(self, validated_data):
        realm_id = self.context["view"].kwargs.get("realm_id")
        realms = Realm.objects.filter(id=realm_id)
        if not realms.exists():
            raise ValidationError(f"Realm with {realm_id} not found")
        return LdapGroup.full_create(realms.first(), **validated_data)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        return instance.full_update(instance, **validated_data)
