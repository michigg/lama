"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from account_manager.forms import LdapPasswordResetForm
from account_manager.views.user_views import LdapPasswordChangeView
from .views import about

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    path('', include('account_manager.urls')),
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html',
                                              form_class=LdapPasswordResetForm),
         name='password_reset'),

    path('accounts/', include('django.contrib.auth.urls')),
]
