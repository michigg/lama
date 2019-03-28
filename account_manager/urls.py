from django.urls import path
from . import views

urlpatterns = [
    path('user-list/', views.userlist, name='userlist'),
    path('user/<str:dn>', views.userlist, name='user'),
]
