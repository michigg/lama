from django.urls import path
from . import views

urlpatterns = [
    path('realm/', views.realm, name='realm-home'),
    path('realm/<int:id>/', views.realm_detail, name='realm-detail'),
    path('user/list/', views.userlist, name='user-list'),
    path('user/get/<str:dn>/', views.user_detail, name='user'),

    path('user/add/', views.adduser, name='user-add'),
    path('group/add/', views.addgroup, name='group-add'),
    path('group/get/<str:dn>/', views.group_detail, name='group'),
]
