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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenRefreshView
from account_manager.api.v1.authentication.views import LamaTokenObtainPairView

from account_manager.forms import LdapPasswordResetForm
from account_manager.views.user_views import LdapPasswordChangeView
from .views import about

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

schema_view = get_schema_view(
    openapi.Info(
        title="LAMa API",
        default_version='0.1.0',
        description="API for Ldap Account Manager",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="michael-guenther.goetz@stud.uni-bamberg.de"),
        license=openapi.License(name="AGPL License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

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

    # API
    # path('api/auth/', include('rest_framework.urls')),
    # path('api/auth/token/', views.obtain_auth_token),
    path('api/', include('account_manager.api.v1.urls')),
    # Simple jwt
    path('api/auth/token/', LamaTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # drf yasg
    re_path(r'api/docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
