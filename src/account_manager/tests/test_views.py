from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from account_helper.models import Realm
from account_manager.models import LdapUser


# class RealmViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Realm.objects.get_or_create(name="test", ldap_base_dn="ou=test,dc=test,dc=de")
#
#     def setUp(self):
#         self.realm = Realm.objects.get(name="test")
#
#     def tearDown(self):
#         realm = Realm.objects.get(name="test")
#         realm.delete()
#
#     def test_realm_home_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-home'))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_add_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-add'))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_detail_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-detail', args=[self.realm.id]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_update_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-update', args=[self.realm.id]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_delete_confirm_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-delete-confirm', args=[self.realm.id]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_delete__view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-delete', args=[self.realm.id]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_realm_mail_test_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('realm-mail-test', args=[self.realm.id]))
#         self.assertEqual(response.status_code, 302)


class RealmViewWithLoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        realm, _ = Realm.objects.get_or_create(name="test", ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de")
        LdapUser.set_root_dn(realm)
        LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                       password=RealmViewWithLoginTest.get_password(),
                                       first_name="max",
                                       last_name="musterstudent")
        User.objects.get_or_create(username="test", email="test@test.de")

    @classmethod
    def get_password(cls):
        return "12345678"

    def setUp(self):
        self.realm = Realm.objects.get(name="test")
        LdapUser.set_root_dn(self.realm)
        self.ldap_user = LdapUser.objects.get(username="test")
        self.django_user = User.objects.get(username="test")
        self.client.login(username=self.ldap_user.username, password=RealmViewWithLoginTest.get_password())

    def tearDown(self):
        self.realm.delete()
        self.ldap_user.delete()
        self.django_user.delete()

    def test_realm_home_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-home'))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_add_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-add'))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_detail_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-detail', args=[self.realm.id]))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_update_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-update', args=[self.realm.id]))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_delete_confirm_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-delete-confirm', args=[self.realm.id]))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_delete__view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-delete', args=[self.realm.id]))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_mail_test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('realm-mail-test', args=[self.realm.id]))
        response.user = self.django_user
        self.assertEqual(response.status_code, 200)

    def test_realm_add_view_uses_correct_template(self):
        response = self.client.get(reverse('realm-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    # def test_pagination_is_ten(self):
    #     response = self.client.get(reverse('authors'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertTrue(len(response.context['author_list']) == 10)
    #
    # def test_lists_all_authors(self):
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(reverse('authors') + '?page=2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertTrue(len(response.context['author_list']) == 3)
