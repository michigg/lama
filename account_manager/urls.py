from django.urls import path
from . import views

urlpatterns = [
    path('user/list/', views.userlist, name='user-list'),
    path('user/get/<str:dn>/', views.userlist, name='user'),
    path('user/add/', views.adduser, name='user-add'),
    path('group/add/', views.addgroup, name='group-add'),
]
