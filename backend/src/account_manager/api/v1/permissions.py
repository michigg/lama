from rest_framework import permissions

from account_helper.models import Realm


class RealmAdminPermission(permissions.BasePermission):
    message = 'Realm Admin permissions required'

    def has_permission(self, request, view):
        realm_id = view.kwargs.get('realm_id', None)
        if realm_id:
            return request.user.is_superuser or len(
                Realm.objects.filter(id=realm_id).filter(
                    admin_group__user__username__contains=request.user.username)) > 0
        else:
            return request.user.is_superuser or len(
                Realm.objects.filter(admin_group__user__username__contains=request.user.username)) > 0


class ManageGroupPermission(permissions.BasePermission):
    message = 'Die angefragte Gruppe gehört einem anderen Bereich an. ' \
              'Gruppen können nur von dem Bereich bearbeitet werden, in dem sie erstellt wurden.'

    def has_permission(self, request, view):
        realm_id = view.kwargs.get('realm_id', None)
        group_dn = view.kwargs.get('group_dn', None)

        return not (realm_id and group_dn and Realm.objects.get(id=realm_id).ldap_base_dn not in group_dn)


class ManageUserPermission(permissions.BasePermission):
    message = 'Der angefragte Nutzer gehört einem anderen Bereich an. ' \
              'Nutzer können nur von dem Bereich bearbeitet werden, in dem sie erstellt wurden.'

    def has_permission(self, request, view):
        realm_id = view.kwargs.get('realm_id', None)
        user_dn = view.kwargs.get('user_dn', None)

        return not (realm_id and user_dn and Realm.objects.get(id=realm_id).ldap_base_dn not in user_dn)
