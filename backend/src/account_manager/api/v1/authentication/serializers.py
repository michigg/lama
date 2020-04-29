from django.contrib.auth.models import User, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import logging

logger = logging.getLogger(__name__)


class LamaTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        if user.is_superuser:
            permissions = Permission.objects.all()
        else:
            permissions = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        perm_tuple = [LamaTokenObtainPairSerializer._get_casl_dict(x.codename, x.name) for x in permissions]

        logger.error(Permission.objects.all())
        logger.error(user.user_permissions.all())
        # Add custom claims
        token['user'] = {'username': user.username, 'email': user.email, 'rules': perm_tuple}
        # ...

        return token

    @staticmethod
    def _get_casl_dict(codename: str, description: str):
        splitted_codename = codename.split('_')
        subject = splitted_codename[-1]
        subject = subject.capitalize()
        action = "_".join(splitted_codename[0:-2]) if len(splitted_codename) > 2 else splitted_codename[0]

        return {'action': action, 'subject': subject, 'description': description}
