import logging

from django.contrib.auth.models import User, Group
from django.test import TestCase
# Create your tests here.
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


class RealmDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User.objects.get_or_create(username="test", email="test@test.de")
        User.objects.create_superuser(
            username='test_superuser',
            password=RealmDetailViewTest.get_password(),
            email='test@test.de',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def create_ldap_objects(self):
        self.realm_1, _ = Realm.objects.get_or_create(name="test_realm_1",
                                                      ldap_base_dn="ou=test,ou=fachschaften,dc=test,dc=de")

        LdapUser.set_root_dn(self.realm_1)
        self.ldap_user_admin, _ = LdapUser.objects.get_or_create(username="test_admin", email="test@test.de",
                                                                 password=RealmDetailViewTest.get_password(),
                                                                 first_name="max",
                                                                 last_name="musterstudent")
        self.ldap_user, _ = LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                                           password=RealmDetailViewTest.get_password(),
                                                           first_name="max",
                                                           last_name="musterstudent")
        LdapGroup.set_root_dn(self.realm_1)
        self.realm_1_ldap_group = LdapGroup.objects.create(name="test_realm_1_admin_group",
                                                           members=[self.ldap_user_admin.dn])

        logging.disable(logging.DEBUG)
        self.realm_1.admin_group = self.realm_1_ldap_group.get_django_group()
        self.realm_1.save()

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
        self.ldap_user_admin.delete()
        self.ldap_user.delete()
        self.realm_1_ldap_group.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-detail', args=[self.realm_1.id]))
        self.assertEqual(response.status_code, 302)

    def test_with_user_login(self):
        self.client.login(username=self.ldap_user.username, password=RealmDetailViewTest.get_password())
        response = self.client.get(reverse('realm-detail', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_admin_login(self):
        self.client.login(username=self.ldap_user_admin.username, password=RealmDetailViewTest.get_password())
        response = self.client.get(reverse('realm-detail', args=[self.realm_1.id]))
        self.assertContains(response, 'Bereich ', status_code=200)
        self.client.logout()

    def test_with_superuser_login(self):
        self.client.login(username=self.django_superuser.username, password=RealmDetailViewTest.get_password())
        response = self.client.get(reverse('realm-detail', args=[self.realm_1.id]))
        self.assertContains(response, 'Bereich', status_code=200)
        self.client.logout()


class RealmUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User.objects.get_or_create(username="test", email="test@test.de")
        User.objects.create_superuser(
            username='test_superuser',
            password=RealmUpdateViewTest.get_password(),
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
                                                                          password=RealmUpdateViewTest.get_password(),
                                                                          first_name="max",
                                                                          last_name="musterstudent")
        self.ldap_user_admin, _ = LdapUser.objects.get_or_create(username="test_admin", email="test@test.de",
                                                                 password=RealmUpdateViewTest.get_password(),
                                                                 first_name="max",
                                                                 last_name="musterstudent")
        self.ldap_user, _ = LdapUser.objects.get_or_create(username="test", email="test@test.de",
                                                           password=RealmUpdateViewTest.get_password(),
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
        self.realm_3_ldap_group.delete()

    def test_without_login(self):
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertEqual(response.status_code, 302)

    def test_with_user_login(self):
        self.client.login(username=self.ldap_user.username, password=RealmUpdateViewTest.get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_admin_login(self):
        self.client.login(username=self.ldap_user_admin.username, password=RealmUpdateViewTest.get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, 'Leider hast du keine Rechte', status_code=403)
        self.client.logout()

    def test_with_superuser_login(self):
        self.client.login(username=self.django_superuser.username, password=RealmUpdateViewTest.get_password())
        response = self.client.get(reverse('realm-update', args=[self.realm_1.id]))
        self.assertContains(response, '<label for="id_name">Bereichsname</label>', status_code=200)
        self.client.logout()

    def test_with_superuser_login_post_single_changes(self):
        self.client.login(username=self.django_superuser.username, password=RealmUpdateViewTest.get_password())
        new_name = "new test realm"
        new_email = "newtest@test.de"
        new_admin_group = self.realm_1_ldap_group
        new_default_group = self.realm_3_ldap_group
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
        self.client.login(username=self.django_superuser.username, password=RealmUpdateViewTest.get_password())
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
