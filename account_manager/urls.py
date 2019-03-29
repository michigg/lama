from django.urls import path
from . import views

urlpatterns = [
    # Realm
    path('realm/', views.realm_home, name='realm-home'),
    path('realm/<int:realm_id>/', views.realm_detail, name='realm-detail'),
    path('realm/<int:realm_id>/update/', views.realm_update, name='realm-update'),
    path('realm/<int:realm_id>/delete/', views.realm_delete, name='realm-delete'),

    # Realm User
    path('realm/<int:realm_id>/users/', views.realm_user, name='realm-user-list'),
    path('realm/<int:realm_id>/users/add/', views.user_add, name='realm-user-add'),
    path('realm/<int:realm_id>/user/<str:user_dn>/', views.user_detail, name='realm-user-detail'),
    path('realm/<int:realm_id>/user/<str:user_dn>/update/', views.user_update, name='realm-user-update'),
    path('realm/<int:realm_id>/user/<str:user_dn>/delete/', views.user_delete, name='realm-user-delete'),

    # Realm Group
    path('realm/<int:realm_id>/groups/', views.realm_groups, name='realm-group-list'),
    path('realm/<int:realm_id>/group/', views.user_add, name='realm-group-detail'),
    path('realm/<int:realm_id>/group/add/', views.group_add, name='realm-group-add'),
    path('realm/<int:realm_id>/user/<int:group_dn>/delete/', views.user_add, name='realm-group-delete'),

    # Permission Info
    path('permission-denied', views.permission_denied, name='permission-denied')
]
