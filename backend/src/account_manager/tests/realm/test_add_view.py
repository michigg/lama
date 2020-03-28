import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm
from account_manager.tests.utils.utils import get_realm, get_user, clear_realm_user, clear_realm_group, get_password, \
    get_group


class RealmAddViewTest(TestCase):
    databases = ["default", "ldap"]

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
        self.ldap_user_2 = get_user(2, self.realm_1)
        self.ldap_user_realm_1_admin = get_user(1, self.realm_1, admin=True)
        self.ldap_user_realm_2_admin = get_user(2, self.realm_1, admin=True)
        self.ldap_user_multiple_realm_admin = get_user(1, self.realm_1, multiple_admin=True)
        self.ldap_user_super_user = get_user(1, self.realm_1, super_admin=True)
        self.ldap_group_1_realm_1_default = get_group(1, self.realm_1, [self.ldap_user_1, self.ldap_user_realm_1_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_default = get_group(2, self.realm_2, [self.ldap_user_2, self.ldap_user_realm_2_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_1_admin = get_group(3, self.realm_1, [self.ldap_user_realm_1_admin,
                                                                      self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_admin = get_group(4, self.realm_2, [self.ldap_user_realm_2_admin,
                                                                      self.ldap_user_multiple_realm_admin])

        self.realm_1.default_group = self.ldap_group_1_realm_1_default.get_django_group()
        self.realm_1.admin_group = self.ldap_group_1_realm_1_admin.get_django_group()
        self.realm_1.save()
        self.realm_2.default_group = self.ldap_group_1_realm_2_default.get_django_group()
        self.realm_2.admin_group = self.ldap_group_1_realm_2_admin.get_django_group()
        self.realm_2.save()

    def setUp(self):
        self.create_ldap_objects()
        self.django_superuser = User.objects.get(username="test_superuser")

    def tearDown(self):
        self.client.logout()
        self.clear_ldap_objects()
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
        response = self.client.get(reverse('realm-add'))
        self.assertEqual(response.status_code, 302)

    def test_with_login(self):
        self.client.login(username=self.ldap_user_1.username, password=get_password())
        response = self.client.get(reverse('realm-add'))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)

    def test_with_login_and_post_valid_form(self):
        self.client.login(username=self.ldap_user_1.username, password=get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)

    def test_with_super_user_login(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.get(reverse('realm-add'))
        self.assertContains(response, 'Neuen Bereich anlegen', status_code=200)

    def test_with_super_user_login_add_realm(self):
        realm = Realm.objects.get(name=self.realm_1.name)
        realm.delete()
        new_name = 'test_add'
        ldap_dn = 'ou=test_1,dc=test,dc=de'
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': new_name, 'ldap_base_dn': ldap_dn})
        self.assertContains(response, 'Bereich test', status_code=201)
        self.assertTrue(Realm.objects.filter(name=new_name, ldap_base_dn=ldap_dn).exists())

    def test_with_super_user_login_add_extisting_realm(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)

    def test_with_super_user_login_add_extisting_realm_with_different_name(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test_new', 'ldap_base_dn': 'ou=test,ou=fachschaften,dc=test,dc=de'})
        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)

    def test_with_super_user_login_add_realm_with_not_existing_ldap_base_dn(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.post(reverse('realm-add'),
                                    {'name': 'test_not_extisting_ldap_dn',
                                     'ldap_base_dn': 'ou=not_exists,ou=fachschaften,dc=test,dc=de'})

        self.assertContains(response, 'Das hinzufügen des Bereichs ist fehlgeschlagen.', status_code=409)
