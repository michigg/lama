from django.urls import path

from . import main_views
from account_manager.views import user_views
from account_manager.views import group_views

urlpatterns = [
    # Realm
    path('', main_views.realm_list, name='realm-home'),
    path('realm/add/', main_views.realm_add, name='realm-add'),
    path('realm/<int:realm_id>/', main_views.realm_detail, name='realm-detail'),
    path('realm/<int:realm_id>/update/', main_views.realm_update, name='realm-update'),
    path('realm/<int:realm_id>/delete/confirm/', main_views.realm_delete_confirm, name='realm-delete-confirm'),
    path('realm/<int:realm_id>/delete/', main_views.realm_delete, name='realm-delete'),
    path('realm/<int:realm_id>/mail/test/', main_views.realm_email_test, name='realm-mail-test'),

    # Realm User
    path('realm/<int:realm_id>/users/', user_views.realm_user, name='realm-user-list'),
    path('realm/<int:realm_id>/users/add/', user_views.user_add, name='realm-user-add'),
    path('realm/<int:realm_id>/user/<str:user_dn>/', user_views.realm_user_detail,
         name='realm-user-detail'),
    path('realm/<int:realm_id>/user/<str:user_dn>/update/', user_views.realm_user_update,
         name='realm-user-update'),
    path('realm/<int:realm_id>/user/<str:user_dn>/group/update/',
         user_views.realm_user_group_update,
         name='realm-user-group-update'),
    path('realm/<int:realm_id>/user/<str:user_dn>/group/update/add/',
         user_views.realm_user_group_update_add,
         name='realm-user-group-update-add'),
    path('realm/<int:realm_id>/user/<str:user_dn>/group/update/delete/',
         user_views.realm_user_group_update_delete,
         name='realm-user-group-update-delete'),
    path('realm/<int:realm_id>/user/delete/single/<str:user_dn>/confirm/',
         user_views.realm_user_delete_confirm,
         name='realm-user-delete-confirm'),
    path('realm/<int:realm_id>/user/delete/single/<str:user_dn>/',
         user_views.realm_user_delete,
         name='realm-user-delete'),
    path('realm/<int:realm_id>/user/delete/multiple/confirm/',
         user_views.realm_multiple_user_delete_confirm,
         name='realm-multiple-user-delete-confirm'),
    path('realm/<int:realm_id>/user/delete/multiple/', user_views.realm_multiple_user_delete,
         name='realm-multiple-user-delete'),

    # Realm Group
    path('realm/<int:realm_id>/groups/', group_views.realm_groups, name='realm-group-list'),
    path('realm/<int:realm_id>/groups/add/', group_views.group_add, name='realm-group-add'),
    path('realm/<int:realm_id>/group/<str:group_dn>/', group_views.group_detail,
         name='realm-group-detail'),
    path('realm/<int:realm_id>/group/<str:group_dn>/update/', group_views.group_update,
         name='realm-group-update'),
    path('realm/<int:realm_id>/group/<str:group_dn>/delete/confirm/', group_views.group_delete_confirm,
         name='realm-group-delete-confirm'),
    path('realm/<int:realm_id>/group/<str:group_dn>/delete/', group_views.group_delete,
         name='realm-group-delete'),

    # User
    path('user/<str:user_dn>/update/realm/<int:realm_id>/', user_views.user_update,
         name='user-update'),
    path('user/<str:user_dn>/delete/realm/<int:realm_id>/confirm/',
         user_views.user_delete_confirm,
         name='user-delete-confirm'),
    path('user/<str:user_dn>/delete/realm/<int:realm_id>/', user_views.user_delete,
         name='user-delete'),
    path('accounts/reset/<uidb64>/<token>/', user_views.LdapPasswordResetConfirmView.as_view(),
         name='ldap_password_reset_confirm'),
    path('accounts/password_change/', user_views.LdapPasswordChangeView.as_view(),
         name='password_change'),

    # Extra
    path('permission-denied/', main_views.permission_denied, name='permission-denied'),
    path('accounts/deleted/<int:realm_id>/', user_views.user_deleted, name='account-deleted'),
]
