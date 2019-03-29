from django.urls import path
from . import views

urlpatterns = [
    path('realm/', views.realm, name='realm-home'),
    path('realm/<int:id>/', views.realm_detail, name='realm-detail'),
    path('realm/<int:id>/users/', views.realm_user, name='realm-user-list'),
    path('realm/<int:id>/groups/', views.realm_groups, name='realm-group-list'),
    path('realm/<int:id>/update/', views.realm_update, name='realm-update'),

    path('realm/<int:realm_id>/user/', views.user_add, name='realm-user-add'),
    path('realm/<int:realm_id>/group/', views.group_add, name='realm-group-add'),

    path('user/list/', views.userlist, name='user-list'),
    path('user/get/<str:dn>/', views.user_detail, name='user'),

    path('user/add/', views.user_add, name='user-add'),
    path('group/add/', views.group_add, name='group-add'),
    path('group/get/<str:dn>/', views.group_detail, name='group'),

    path('permission-denied', views.permission_denied, name='permission-denied')
]
