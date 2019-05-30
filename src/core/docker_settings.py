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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = os.environ['DOMAIN']
SITE_NAME = os.environ['SITE_NAME']
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()
DELETION_WAIT_DAYS = int(os.environ.get('DELETION_WAIT_DAYS', "14"))

# Application definition
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
        'NAME': os.environ['LDAP_SERVER_URI'],
        'USER': os.environ.get('LDAP_ADMIN_USER_NAME', ''),
        'PASSWORD': os.environ.get('LDAP_ADMIN_USER_PASSWORD', ''),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_USER', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
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
# STATIC_ROOT = 'static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

########################################################################################################################
#                                         LDAP Config                                                                  #
########################################################################################################################

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_LDAP_SERVER_URI = os.environ['LDAP_SERVER_URI']
AUTH_LDAP_BIND_DN = os.environ.get('LDAP_ADMIN_USER_NAME', '')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('LDAP_ADMIN_USER_PASSWORD', '')

# AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,ou=fs_wiai,ou=fachschaften,dc=stuve,dc=de"
AUTH_LDAP_USER_SEARCH = LDAPSearch(os.environ['LDAP_USER_ENTRY'], ldap.SCOPE_SUBTREE,
                                   os.environ['LDAP_USER_SELECTOR'])
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    os.environ['LDAP_GROUP_ENTRY'],
    ldap.SCOPE_SUBTREE,
    os.environ['LDAP_GROUP_SELECTOR'],
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr=os.environ['LDAP_GROUP_NAME_ATTR'])
AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'cn',
    'last_name': 'sn',
    'email': 'mail',
}
AUTH_PROFILE_MODULE = 'account_manager.UserProfile'

########################################################################################################################
#                                         EMAIL Config                                                                 #
########################################################################################################################
if 'file' in os.environ['EMAIL_BACKEND']:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_TIMEOUT = 15
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = int(os.environ['EMAIL_PORT'])
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','')
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False') == 'True'
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'

DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
SERVER_EMAIL = os.environ['SERVER_EMAIL']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'realm-home'
PASSWORD_RESET_TIMEOUT_DAYS = 3

########################################################################################################################
#                                         Logging Config                                                               #
########################################################################################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(module)s [%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'account_manager': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'account_helper': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'django_auth_ldap': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django_ldapdb': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        '*': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
