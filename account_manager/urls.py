from django.urls import path

import account_manager.views.group_views
import account_manager.views.user_views
from . import main_views

urlpatterns = [
    # Realm
    path('realm/', main_views.realm_list, name='realm-home'),
    path('realm/<int:realm_id>/', main_views.realm_detail, name='realm-detail'),
    path('realm/<int:realm_id>/update/', main_views.realm_update, name='realm-update'),
    path('realm/<int:realm_id>/delete/', main_views.realm_delete, name='realm-delete'),

    # Realm User
    path('realm/<int:realm_id>/users/', account_manager.views.user_views.realm_user, name='realm-user-list'),
    path('realm/<int:realm_id>/users/add/', account_manager.views.user_views.user_add, name='realm-user-add'),
    path('realm/<int:realm_id>/user/<str:user_dn>/', account_manager.views.user_views.user_detail, name='realm-user-detail'),
    path('realm/<int:realm_id>/user/<str:user_dn>/update/', account_manager.views.user_views.user_update, name='realm-user-update'),
    path('realm/<int:realm_id>/user/<str:user_dn>/delete/', account_manager.views.user_views.user_delete, name='realm-user-delete'),

    # Realm Group
    path('realm/<int:realm_id>/groups/', account_manager.views.group_views.realm_groups, name='realm-group-list'),
    path('realm/<int:realm_id>/groups/add/', account_manager.views.group_views.group_add, name='realm-group-add'),
    path('realm/<int:realm_id>/group/<str:group_dn>/', account_manager.views.group_views.group_detail, name='realm-group-detail'),
    path('realm/<int:realm_id>/group/<str:group_dn>/update/', account_manager.views.group_views.group_update, name='realm-group-update'),
    path('realm/<int:realm_id>/group/<str:group_dn>/delete/', account_manager.views.group_views.group_delete, name='realm-group-delete'),

    # Permission Info
    path('permission-denied', main_views.permission_denied, name='permission-denied')
]
