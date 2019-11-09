import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup


class RealmDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User.objects.get_or_create(username="test", email="test@test.de")
        User.objects.create_superuser(
            username='test_superuser',
            password=RealmDeleteViewTest.get_password(),
            email='test@test.de',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def create_ldap_objects(self):
        self.realm_1, _ = Realm.objects.get_or_create(name="test_realm_1",
                                                      ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de",
                                                      email="test.realm@test.de")
        self.realm_2, _ = Realm.objects.get_or_create(name="test_realm_2",
                                                      ldap_base_dn="ou=test2,ou=fachschaften,dc=test,dc=de")
        LdapUser.set_root_dn(self.realm_1)
        self.ldap_user_multiple_admin, _ = LdapUser.objects.get_or_create(username="test_multi_admin",
                                                                          email="test@test.de",
                                                                          password=RealmDeleteViewTest.get_password(),
                                                                          first_name="max",
                                                                          last_name="musterstudent")
        self.ldap_user_admin, _ = LdapUser.objects.get_or_create(username="test_admin", email="test@test.de",
                                                                 password=RealmDeleteViewTest.get_password(),
                                                                 first_name="max",
                                                                 last_name="musterstudent")
        self.ldap_user, _ = LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                                           password=RealmDeleteViewTest.get_password(),
                                                           first_name="max",
                                                           last_name="musterstudent")
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_1_ldap_group = LdapGroup.objects.create(name="test_realm_1_admin_group",
                                                           members=[self.ldap_user_multiple_admin.dn,
                                                                    self.ldap_user_admin.dn])
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_2_ldap_group = LdapGroup.objects.create(name="test_realm_2_admin_group",
                                                           members=[self.ldap_user_multiple_admin.dn])
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_3_ldap_group = LdapGroup.objects.create(name="test_realm_3_admin_group",
                                                           members=[self.ldap_user_admin.dn])
        logging.disable(logging.DEBUG)
        self.realm_1.admin_group = self.realm_1_ldap_group.get_django_group()
        self.realm_1.save()
        self.realm_2.admin_group = self.realm_2_ldap_group.get_django_group()
        self.realm_2.save()
        print("WTF")

    @classmethod
    def get_password(cls):
        return "12345678"

    def setUp(self):
        self.create_ldap_objects()
        self.django_superuser = User.objects.get(username="test_superuser")

    def tearDown(self):
        self.client.logout()
        try:
            self.clear_ldap_objects()
        except Exception as e:
            pass
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
        self.realm_3_ldap_group.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-delete', args=[self.realm_1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Realm.objects.filter(id=self.realm_1.id).exists())

    def test_with_user_login(self):
        self.client.login(username=self.ldap_user.username, password=RealmDeleteViewTest.get_password())
        response = self.client.get(reverse('realm-delete', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.assertTrue(Realm.objects.filter(id=self.realm_1.id).exists())

    def test_with_admin_login(self):
        self.client.login(username=self.ldap_user_admin.username, password=RealmDeleteViewTest.get_password())
        response = self.client.get(reverse('realm-delete', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.assertTrue(Realm.objects.filter(id=self.realm_1.id).exists())

    def test_with_superuser_login(self):
        self.client.login(username=self.django_superuser.username, password=RealmDeleteViewTest.get_password())
        response = self.client.get(reverse('realm-delete', args=[self.realm_1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Realm.objects.filter(id=self.realm_1.id).exists())

    def test_with_superuser_login_info_screen_no_deletion(self):
        self.client.login(username=self.django_superuser.username, password=RealmDeleteViewTest.get_password())
        response = self.client.get(reverse('realm-delete-confirm', args=[self.realm_1.id]))
        self.assertContains(response, '<h1>Löschen des Bereichs', status_code=200)
        delete_link = reverse('realm-delete', args=[self.realm_1.id])
        self.assertContains(response, f'<a href="{delete_link}" class="btn btn-danger p-2">Bereich löschen</a>')
        cancel_link = reverse('realm-detail', args=[self.realm_1.id])
        self.assertContains(response, f'<a href="{cancel_link}" class="btn btn-secondary mr-auto p-2">Abbrechen</a>')

        self.assertTrue(Realm.objects.filter(id=self.realm_1.id).exists())
