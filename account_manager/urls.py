from django.urls import path
from . import views

urlpatterns = [
    # Realm
    path('realm/', views.realm_home, name='realm-home'),
    path('realm/<int:id>/', views.realm_detail, name='realm-detail'),
    path('realm/<int:id>/users/', views.realm_user, name='realm-user-list'),
    path('realm/<int:id>/groups/', views.realm_groups, name='realm-group-list'),
    path('realm/<int:id>/update/', views.realm_update, name='realm-update'),
    path('realm/<int:realm_id>/delete/', views.realm_delete, name='realm-delete'),

    # Realm User
    path('realm/<int:realm_id>/user/', views.user_add, name='realm-user-detail'),
    path('realm/<int:realm_id>/user/add/', views.user_add, name='realm-user-add'),
    path('realm/<int:realm_id>/user/<int:user_dn>/delete/', views.user_add, name='realm-user-delete'),

    # Realm Group
    path('realm/<int:realm_id>/group/', views.user_add, name='realm-group-detail'),
    path('realm/<int:realm_id>/group/add/', views.group_add, name='realm-group-add'),
    path('realm/<int:realm_id>/user/<int:group_dn>/delete/', views.user_add, name='realm-group-delete'),

    path('permission-denied', views.permission_denied, name='permission-denied')
]
