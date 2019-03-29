"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r$_n!+7(w&jo3obu!1f#pu3nfs0s56@58y((6c9*tr(r2u*3vd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'realm-home'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account_manager',
    'account_helper',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'core.jinja2.environment'
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/admin', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': 'ldap://localhost:1389',
        'USER': 'cn=admin,dc=stuve,dc=de',
        'PASSWORD': 'secret',
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASE_ROUTERS = ['ldapdb.router.Router']
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

########################################################################################################################
#                                         LDAP Config                                                                  #
########################################################################################################################

AUTHENTICATION_BACKENDS = [
    'multiple_ldap_backends.ldap.LDAPBackend1',
    'multiple_ldap_backends.ldap.LDAPBackend2',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_LDAP_1_SERVER_URI = "ldap://localhost:1389"
AUTH_LDAP_1_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,ou=fs_wiai,ou=fachschaften,dc=stuve,dc=de"
AUTH_LDAP_1_GROUP_SEARCH = LDAPSearch("dc=stuve,dc=de",
                                    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
                                    )
AUTH_LDAP_1_GROUP_TYPE = GroupOfNamesType(name_attr='cn')
AUTH_LDAP_1_MIRROR_GROUPS = True

AUTH_LDAP_2_SERVER_URI = "ldap://localhost:1389"
AUTH_LDAP_2_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,ou=fs_sowi,ou=fachschaften,dc=stuve,dc=de"
AUTH_LDAP_2_GROUP_SEARCH = LDAPSearch("dc=stuve,dc=de",
                                    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
                                    )
AUTH_LDAP_2_GROUP_TYPE = GroupOfNamesType(name_attr='cn')
AUTH_LDAP_2_MIRROR_GROUPS = True

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'cn',
    'last_name': 'sn',
    'email': 'mail',
}
AUTH_PROFILE_MODULE = 'account_manager.UserProfile'
