"""
Django project settings.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import logging
import logging.config
import os
import sys

from armory.environ import env

# -----------------------------------------------------------------------------
# the DEBUG var is used to determine the value of a number of further vars

DEBUG = env('DEBUG', False, cast=bool, boolmap=True)


def ifdebug(debug_true, normal=None):
    """ Returns a value based on the DEBUG variable """
    return debug_true if DEBUG is True else normal


# -----------------------------------------------------------------------------
# logging configuration

LOGGING_LEVEL = env('LOGGING_LEVEL', 'INFO')
DB_LOGGING_LEVEL = env('DB_LOGGING_LEVEL', 'WARNING')
TEMPLATE_LOGGING_LEVEL = env('TEMPLATE_LOGGING_LEVEL', LOGGING_LEVEL)
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(message)s',
        },
        'levelname': {
            'format': '[%(levelname)s] %(message)s',
        },
        'normal': {
            'format': '[%(levelname)s] %(name)s:%(lineno)d  %(message)s',
        },
        'verbose': {
            'format': (
                '[%(levelname)s] %(name)s:%(funcName)s:%(lineno)d  %(message)s'
            ),
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'levelname',
        },
        'console_normal': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'normal',
        },
        'admin_emails': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        '': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': DB_LOGGING_LEVEL,
            'handlers': ['console_normal'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['admin_emails'],
            'propagate': True,
        },
        'django.template': {
            'level': TEMPLATE_LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'elasticsearch.trace': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
logging.config.dictConfig(LOGGING)


# -----------------------------------------------------------------------------
# secret key settings

if DEBUG is True:
    SECRET_KEY = env(
        'SECRET_KEY',
        '%9+*7wr09e-(+_-b8#_z0_5*2ahy^==*@2+eo2c$vyiesj*$ku'
    )
else:
    SECRET_KEY = env('SECRET_KEY')


# -----------------------------------------------------------------------------
# core settings

# Build paths inside the settings via os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADMINS = (
    ('Site Admin', 'kraken@neuroticnerd.com'),
)
ALLOWED_HOSTS = env('ALLOWED_HOSTS', [])
APPEND_SLASH = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ROOT_URLCONF = 'hyperion.urls'
WSGI_APPLICATION = 'hyperion.wsgi.application'
# AUTH_USER_MODEL = 'accounts.User'


# -----------------------------------------------------------------------------
# django-allauth settings

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'  # 'username_email'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = False
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
# ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = ifdebug('none', 'mandatory')
# ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Site] '
ACCOUNT_DEFAULT_HTTP_PROTOCOL = ifdebug('http', 'https')
ACCOUNT_FORMS = {
    'login': 'hyperion.main.forms.CrispyLoginForm',
}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = ifdebug(None, 3)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
# ACCOUNT_LOGOUT_ON_GET = False
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# ACCOUNT_SIGNUP_FORM_CLASS = None
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ACCOUNT_USERNAME_BLACKLIST = []
# ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = env('USERNAME_MIN_LENGTH', 3)
# ACCOUNT_USERNAME_REQUIRED = True

# SOCIALACCOUNT_ADAPTER = default
# SOCIALACCOUNT_FORMS = {}
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ('email', 'profile'),
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    # 'facebook': {
    #     'SCOPE': ['email', 'publish_stream'],
    #     'METHOD': 'js_sdk',
    # },
}
# SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
# SOCIALACCOUNT_STORE_TOKENS = True


# -----------------------------------------------------------------------------
# authentication and password settings

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = ifdebug([], (
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
))


# -----------------------------------------------------------------------------
# SSL/TSL security and sessions settings

SECURE_SSL_REDIRECT = env(
    'SECURE_SSL_REDIRECT', ifdebug(False, True), cast=bool, boolmap=True
)
SECURE_BROWSER_XSS_FILTER = env(
    'SECURE_BROWSER_XSS_FILTER', True, cast=bool, boolmap=True
)
SECURE_CONTENT_TYPE_NOSNIFF = env(
    'SECURE_CONTENT_TYPE_NOSNIFF', True, cast=bool, boolmap=True
)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = False
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS', 'DENY')

if SECURE_SSL_REDIRECT:
    SESSION_COOKIE_SECURE = env(
        'SESSION_COOKIE_SECURE', True, cast=bool, boolmap=True
    )
    SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS', 3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env(
        'SECURE_HSTS_INCLUDE_SUBDOMAINS', True, cast=bool, boolmap=True
    )
    CSRF_COOKIE_SECURE = env(
        'CSRF_COOKIE_SECURE', True, cast=bool, boolmap=True
    )
else:
    SESSION_COOKIE_SECURE = env(
        'SESSION_COOKIE_SECURE', False, cast=bool, boolmap=True
    )
    SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS', 0)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env(
        'SECURE_HSTS_INCLUDE_SUBDOMAINS', False, cast=bool, boolmap=True
    )
    CSRF_COOKIE_SECURE = env(
        'CSRF_COOKIE_SECURE', False, cast=bool, boolmap=True
    )

SESSION_CACHE_ALIAS = env('SESSION_CACHE_ALIAS', 'default')
SESSION_COOKIE_AGE = env('SESSION_COOKIE_AGE', 3600, int)
SESSION_COOKIE_DOMAIN = env('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = env(
    'SESSION_ENGINE',
    'django.contrib.sessions.backends.cached_db'
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = env(
    'SESSION_EXPIRE_AT_BROWSER_CLOSE',
    False,
    cast=bool,
    boolmap=True
)
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# -----------------------------------------------------------------------------
# site-specific configuration

SITE_ID = env('SITE_ID', 1, int)


# -----------------------------------------------------------------------------
# utilized apps and middleware

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'hyperion',
    'hyperion.main',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.dropbox_oauth2',
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.digitalocean',
    # 'allauth.socialaccount.providers.facebook',

    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]


# -----------------------------------------------------------------------------
# templates configuration

DJANGO_TEMPLATES_CONFIG = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(BASE_DIR, 'templates')
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': (
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'hyperion.main.context_processors.login_context',
        ),
        'debug': env('TEMPLATE_DEBUG', DEBUG),
    },
}
if DEBUG is False:
    # cannot use the 'APP_DIRS' setting with cached loader
    DJANGO_TEMPLATES_CONFIG['APP_DIRS'] = False
    DJANGO_TEMPLATES_CONFIG['OPTIONS']['loaders'] = (
        # Further info and important caveats available at:
        # https://docs.djangoproject.com/en/1.10/ref/
        #     templates/api/#django.template.loaders.cached.Loader
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    )
TEMPLATES = [
    # {
    #     'BACKEND': 'django_jinja.backend.Jinja2',
    #     'DIRS': [path('jinja2')],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         # Use jinja2/ for jinja templates
    #         'app_dirname': 'jinja2',
    #         # Don't figure out which template loader to use based on
    #         # file extension
    #         'match_extension': '',
    #         'newstyle_gettext': True,
    #         'context_processors': _CONTEXT_PROCESSORS,
    #         'undefined': 'jinja2.Undefined',
    #         'extensions': [
    #             'jinja2.ext.do',
    #             'jinja2.ext.loopcontrols',
    #             'jinja2.ext.with_',
    #             'jinja2.ext.i18n',
    #             'jinja2.ext.autoescape',
    #             'puente.ext.i18n',
    #             'django_jinja.builtins.extensions.CsrfExtension',
    #             'django_jinja.builtins.extensions.CacheExtension',
    #             'django_jinja.builtins.extensions.TimezoneExtension',
    #             'django_jinja.builtins.extensions.UrlsExtension',
    #             'django_jinja.builtins.extensions.StaticFilesExtension',
    #             'django_jinja.builtins.extensions.DjangoFiltersExtension',
    #             'pipeline.jinja2.PipelineExtension',
    #             'waffle.jinja.WaffleExtension',
    #         ],
    #     }
    # },
    DJANGO_TEMPLATES_CONFIG,
]


# -----------------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}


# -----------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
ENABLE_TRANSLATION = env('ENABLE_TRANSLATION', False, cast=bool, boolmap=True)
DEFAULT_LANGUAGE = 'en'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images) and Media
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = env('STATIC_ROOT', 'static')
STATIC_URL = env('STATIC_URL', '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Special value, unique per deploy/code-revision, which is used to guarantee
# correct static file referencing.
# STATICFILES_VERSION = env('STATICFILES_VERSION', 1)

MEDIA_ROOT = env('MEDIA_ROOT', 'media')
MEDIA_URL = env('MEDIA_URL', '/media/')


# -----------------------------------------------------------------------------
# django-crispy-forms

CRISPY_TEMPLATE_PACK = 'bootstrap3'
