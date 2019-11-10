import logging

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup
from account_manager.tests.utils.utils import get_user, get_group, get_realm, get_password


class RealmUpdateViewTest(TestCase):

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
        self.ldap_group_1_realm_1_default_new = get_group(2, self.realm_1, [self.ldap_user_1, self.ldap_user_realm_1_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_default = get_group(3, self.realm_2, [self.ldap_user_2, self.ldap_user_realm_2_admin,
                                                                        self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_1_admin = get_group(4, self.realm_1, [self.ldap_user_realm_1_admin,
                                                                      self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_1_admin_new = get_group(5, self.realm_1, [self.ldap_user_realm_1_admin,
                                                                      self.ldap_user_multiple_realm_admin])
        self.ldap_group_1_realm_2_admin = get_group(6, self.realm_2, [self.ldap_user_realm_2_admin,
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
        self.clear_ldap_objects()
        self.django_superuser.delete()
        logging.disable(logging.NOTSET)

    def clear_ldap_objects(self):
        self.realm_1.delete()
        self.realm_2.delete()
        self.ldap_user_1.delete()
        self.ldap_user_2.delete()
        self.ldap_user_realm_1_admin.delete()
        self.ldap_user_realm_2_admin.delete()
        self.ldap_user_multiple_realm_admin.delete()
        self.ldap_user_super_user.delete()
        self.ldap_group_1_realm_1_default.delete()
        self.ldap_group_1_realm_2_default.delete()
        self.ldap_group_1_realm_1_admin.delete()
        self.ldap_group_1_realm_2_admin.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertEqual(response.status_code, 302)

    def test_with_user_login(self):
        self.client.login(username=self.ldap_user_1.username, password=get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_admin_login(self):
        self.client.login(username=self.ldap_user_realm_1_admin.username, password=get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_superuser_login(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=200)
        self.client.logout()

    def test_with_superuser_login_post_single_changes(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        new_name = "new test realm"
        new_email = "newtest@test.de"
        new_admin_group = self.ldap_group_1_realm_1_admin_new
        new_default_group = self.ldap_group_1_realm_1_default_new
        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name, 'email': new_email,
                                     'ldap_base_dn': self.realm_1.ldap_base_dn})
        self.assertContains(response, 'Nutzeranzahl', status_code=200)
        self.realm_1.refresh_from_db()
        self.assertEqual(self.realm_1.name, new_name)
        self.assertEqual(self.realm_1.email, new_email)

        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name, 'email': new_email,
                                     'ldap_base_dn': self.realm_1.ldap_base_dn, 'admin_group': new_admin_group.name})
        self.assertContains(response, 'Nutzeranzahl', status_code=200)
        self.realm_1.refresh_from_db()
        django_group = Group.objects.get(name=new_admin_group.name)
        self.assertEqual(self.realm_1.admin_group, django_group)

        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name, 'email': new_email,
                                     'ldap_base_dn': self.realm_1.ldap_base_dn,
                                     'default_group': new_default_group.name})
        self.assertContains(response, 'Nutzeranzahl', status_code=200)
        self.realm_1.refresh_from_db()
        django_group = Group.objects.get(name=new_default_group.name)
        self.assertEqual(self.realm_1.default_group, django_group)

        self.client.logout()

    def test_with_superuser_login_post_with_missing_data(self):
        self.client.login(username=self.django_superuser.username, password=get_password())
        new_name = "new test realm"
        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name,
                                     'ldap_base_dn': self.realm_1.ldap_base_dn})
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=422)

        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'email': "test@test.de",
                                     'ldap_base_dn': self.realm_1.ldap_base_dn})
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=422)

        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name, 'email': "test@test.de"})
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=422)

        response = self.client.post(reverse('realm-update', args=[self.realm_1.id]),
                                    {'name': new_name, 'email': "abc",
                                     'ldap_base_dn': self.realm_1.ldap_base_dn})
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=422)

        self.client.logout()
