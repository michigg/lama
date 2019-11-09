import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup


class RealmHomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User.objects.get_or_create(username="test", email="test@test.de")
        User.objects.create_superuser(
            username='test_superuser',
            password=RealmHomeViewTest.get_password(),
            email='test@test.de',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def create_ldap_objects(self):
        self.realm_1, _ = Realm.objects.get_or_create(name="test_realm_1",
                                                      ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de")
        self.realm_2, _ = Realm.objects.get_or_create(name="test_realm_2",
                                                      ldap_base_dn="ou=test2,ou=fachschaften,dc=test,dc=de")
        LdapUser.set_root_dn(self.realm_1)
        self.ldap_user_multiple_admin, _ = LdapUser.objects.get_or_create(username="test_multi_admin",
                                                                          email="test@test.de",
                                                                          password=RealmHomeViewTest.get_password(),
                                                                          first_name="max",
                                                                          last_name="musterstudent")
        self.ldap_user_admin, _ = LdapUser.objects.get_or_create(username="test_admin", email="test@test.de",
                                                                 password=RealmHomeViewTest.get_password(),
                                                                 first_name="max",
                                                                 last_name="musterstudent")
        self.ldap_user, _ = LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                                           password=RealmHomeViewTest.get_password(),
                                                           first_name="max",
                                                           last_name="musterstudent")
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_1_ldap_group = LdapGroup.objects.create(name="test_realm_1_admin_group",
                                                           members=[self.ldap_user_multiple_admin.dn,
                                                                    self.ldap_user_admin.dn])
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_2_ldap_group = LdapGroup.objects.create(name="test_realm_2_admin_group",
                                                           members=[self.ldap_user_multiple_admin.dn])
        logging.disable(logging.DEBUG)
        self.realm_1.admin_group = self.realm_1_ldap_group.get_django_group()
        self.realm_1.save()
        self.realm_2.admin_group = self.realm_2_ldap_group.get_django_group()
        self.realm_2.save()

    @classmethod
    def get_password(cls):
        return "12345678"

    def setUp(self):
        self.create_ldap_objects()
        self.django_superuser = User.objects.get(username="test_superuser")

    def tearDown(self):
        self.clear_ldap_objects()
        self.django_superuser.delete()
        logging.disable(logging.NOTSET)

    def clear_ldap_objects(self):
        self.realm_1.delete()
        self.realm_2.delete()
        self.ldap_user_multiple_admin.delete()
        self.ldap_user_admin.delete()
        self.ldap_user.delete()
        self.realm_1_ldap_group.delete()
        self.realm_2_ldap_group.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-home'))
        self.assertEqual(response.status_code, 302)

    def test_with_user_login(self):
        self.client.login(username=self.ldap_user.username, password=RealmHomeViewTest.get_password())
        response = self.client.get(reverse('realm-home'))
        self.assertContains(response, 'Profil löschen', status_code=200)
        self.client.logout()

    def test_with_admin_login(self):
        self.client.login(username=self.ldap_user_admin.username, password=RealmHomeViewTest.get_password())
        response = self.client.get(reverse('realm-home'))
        self.assertContains(response, 'Bereich ', status_code=200)
        self.client.logout()

    def test_with_admin_multiple_realms_login(self):
        self.client.login(username=self.ldap_user_multiple_admin.username, password=RealmHomeViewTest.get_password())
        response = self.client.get(reverse('realm-home'))
        self.assertContains(response, 'Bereiche', status_code=200)
        self.client.logout()

    def test_with_superuser_login(self):
        self.client.login(username=self.django_superuser.username, password=RealmHomeViewTest.get_password())
        response = self.client.get(reverse('realm-home'))
        self.assertContains(response, 'Bereiche', status_code=200)
        self.client.logout()