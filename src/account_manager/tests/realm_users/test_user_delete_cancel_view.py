import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm, DeletedUser
from account_manager.models import LdapUser, LdapGroup
from account_manager.tests.utils.utils import get_realm, get_user, get_group, get_password, clear_realm_user, \
    clear_realm_group

from django.conf import settings

logger = logging.getLogger(__name__)


class RealmUserDeleteCancelViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User.objects.get_or_create(username="test", email="test@test.de")
        User.objects.create_superuser(
            username='test_superuser',
            password=get_password(),
            email='test@test.de',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def create_ldap_objects(self):
        self.realm_1 = get_realm(1, email=True)
        self.realm_2 = get_realm(2, email=False)
        self.ldap_user_1 = get_user(1, self.realm_1)
        self.ldap_user_2 = get_user(2, self.realm_2)
        self.ldap_user_realm_1_admin = get_user(3, self.realm_1, admin=True)
        self.ldap_user_realm_2_admin = get_user(4, self.realm_2, admin=True)
        self.ldap_user_multiple_realm_admin = get_user(5, self.realm_1, multiple_admin=True)
        self.ldap_user_super_user = get_user(1, self.realm_1, super_admin=True)
        self.ldap_group_1_realm_1_default = get_group(1, self.realm_1, [self.ldap_user_1, self.ldap_user_realm_1_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_default = get_group(2, self.realm_2, [self.ldap_user_2, self.ldap_user_realm_2_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_1_admin = get_group(3, self.realm_2, [self.ldap_user_realm_1_admin,
                                                                      self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_admin = get_group(4, self.realm_2, [self.ldap_user_realm_2_admin,
                                                                      self.ldap_user_multiple_realm_admin])

        logging.disable(logging.DEBUG)
        self.realm_1.default_group = self.ldap_group_1_realm_1_default.get_django_group()
        self.realm_1.admin_group = self.ldap_group_1_realm_1_admin.get_django_group()
        self.realm_1.save()
        self.realm_1.default_group = self.ldap_group_1_realm_2_default.get_django_group()
        self.realm_2.admin_group = self.ldap_group_1_realm_2_admin.get_django_group()
        self.realm_2.save()

    def setUp(self):
        self.create_ldap_objects()
        self.django_superuser = User.objects.get(username="test_superuser")

    def tearDown(self):
        self.client.logout()
        try:
            self.clear_ldap_objects()
        except Exception:
            pass
        self.django_superuser.delete()
        logging.disable(logging.NOTSET)

    def clear_ldap_objects(self):
        clear_realm_user(self.realm_1)
        clear_realm_user(self.realm_2)
        clear_realm_group(self.realm_1)
        clear_realm_group(self.realm_2)
        self.realm_1.delete()
        self.realm_2.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertEqual(response.status_code, 302)

    def test_with_login(self):
        self.client.login(username=self.ldap_user_1.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)

    def test_with_admin_login_wrong_realm(self):
        self.client.login(username=self.ldap_user_realm_2_admin.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)

    def test_with_admin_login(self):
        user = User.objects.get(username=self.ldap_user_1.username)
        DeletedUser.objects.create(user=user, ldap_dn=self.ldap_user_1.dn)
        self.client.login(username=self.ldap_user_realm_1_admin.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, f'Nutzerlöschung wurde abgebrochen', status_code=200)
        self.assertFalse(DeletedUser.objects.filter(ldap_dn=self.ldap_user_1.dn).exists())

    def test_with_admin_login_user_not_deleted(self):
        self.client.login(username=self.ldap_user_realm_1_admin.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, f'Nutzer ist nicht als gelöscht markiert.', status_code=409)

    def test_with_super_user_login(self):
        user = User.objects.get(username=self.ldap_user_1.username)
        DeletedUser.objects.create(user=user, ldap_dn=self.ldap_user_1.dn)
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, f'Nutzerlöschung wurde abgebrochen', status_code=200)
        self.assertFalse(DeletedUser.objects.filter(ldap_dn=self.ldap_user_1.dn).exists())

    def test_with_super_user_login_user_not_deleted(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.get(reverse('realm-user-delete-cancel', args=[self.realm_1.id, self.ldap_user_1.dn, ]))
        self.assertContains(response, f'Nutzer ist nicht als gelöscht markiert.', status_code=409)
