import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm
from account_manager.models import LdapUser


class RealmAddViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        realm, _ = Realm.objects.get_or_create(name="test", ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de")
        LdapUser.set_root_dn(realm)
        LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                       password=RealmAddViewTest.get_password(),
                                       first_name="max",
                                       last_name="musterstudent")
        User.objects.get_or_create(username="test", email="test@test.de")
        logging.disable(logging.DEBUG)

    @classmethod
    def get_password(cls):
        return "12345678"

    def setUp(self):
        self.realm = Realm.objects.get(name="test")
        LdapUser.set_root_dn(self.realm)
        self.ldap_user = LdapUser.objects.get(username="test")
        self.django_user = User.objects.get(username="test")
        self.django_superuser = User.objects.create_superuser(
            username='superuser_test',
            password='test',
            email='test@test.de',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def tearDown(self):
        self.realm.delete()
        self.ldap_user.delete()
        self.django_user.delete()
        logging.disable(logging.NOTSET)

    def test_without_login(self):
        response = self.client.get(reverse('realm-add'))
        self.assertEqual(response.status_code, 302)

    def test_with_login(self):
        self.client.login(username=self.ldap_user.username, password=RealmAddViewTest.get_password())
        response = self.client.get(reverse('realm-add'))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_login_and_post_valid_form(self):
        self.client.login(username=self.ldap_user.username, password=RealmAddViewTest.get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_super_user_login(self):
        self.client.login(username=self.django_superuser.username, password='test')
        response = self.client.get(reverse('realm-add'))
        self.assertContains(response, 'Neuen Bereich anlegen', status_code=200)
        self.client.logout()

    def test_with_super_user_login_add_realm(self):
        realm = Realm.objects.get(name=self.realm.name)
        realm.delete()
        self.client.login(username=self.django_superuser.username, password='test')
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Bereich test', status_code=201)
        self.client.logout()
        self.realm, _ = Realm.objects.get_or_create(name="test", ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de")

    def test_with_super_user_login_add_extisting_realm(self):
        self.client.login(username=self.django_superuser.username, password='test')
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)
        self.client.logout()

    def test_with_super_user_login_add_extisting_realm_with_different_name(self):
        self.client.login(username=self.django_superuser.username, password='test')
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test_new', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)
        self.client.logout()

    def test_with_super_user_login_add_realm_with_not_existing_ldap_base_dn(self):
        self.client.login(username=self.django_superuser.username, password='test')
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test_not_extisting_ldap_dn',
                                     'ldap_base_dn': 'ou=not_exists,ou=fachschaften,dc=test,dc=de'})

        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)
        self.client.logout()