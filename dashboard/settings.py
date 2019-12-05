"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json

from debug_toolbar import settings as dt_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPLICATION_DIR = os.path.dirname(globals()['__file__'])

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

USER_ENV = os.environ
try:
    with open(os.getenv("ENV_FILE", "/secrets/env.json")) as f:
        DEFAULT_ENV = json.load(f)
except FileNotFoundError as fnfe:
        print("Default config file or one defined in environment variable ENV_FILE not found. This is normal for the build, should define for operation")
        # Set ENV so collectstatic will still run in the build
        DEFAULT_ENV = os.environ

LOGOUT_URL = '/accounts/logout'
LOGIN_URL = '/accounts/login'

# Google Analytics ID
if 'GA_ID' not in USER_ENV:
    GA_ID = DEFAULT_ENV.get('GA_ID', '')
else:
    GA_ID = USER_ENV.get('GA_ID')

# Resource values from env
if 'RESOURCE_VALUES' not in USER_ENV:
    RESOURCE_VALUES = DEFAULT_ENV.get("RESOURCE_VALUES", {"files": ["canvas"]})
else:
    RESOURCE_VALUES = USER_ENV.get("RESOURCE_VALUES")

if 'RESOURCE_URLS' not in USER_ENV:
    RESOURCE_URLS = DEFAULT_ENV.get("RESOURCE_URLS", {"canvas": {"prefix": "https://demo.instructure.com/files/", "postfix": "/download?download_frd=1"}})
else:
    RESOURCE_URLS = USER_ENV.get("RESOURCE_URLS")

# This is required by flatpages flow. For Example Copyright information in the footer populated from flatpages
SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if 'DJANGO_SECRET_KEY' not in USER_ENV:
    SECRET_KEY = DEFAULT_ENV.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = USER_ENV.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if 'DJANGO_DEBUG' not in USER_ENV:
    DEBUG = DEFAULT_ENV.get('DJANGO_DEBUG', True)
else:
    DEBUG = USER_ENV.get('DJANGO_DEBUG')

if 'ALLOWED_HOSTS' not in USER_ENV:
    ALLOWED_HOSTS = DEFAULT_ENV.get("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])
else:
    ALLOWED_HOSTS = USER_ENV.get("ALLOWED_HOSTS")

if 'DJANGO_WATCHMAN_TOKEN' not in USER_ENV:
    WATCHMAN_TOKEN = DEFAULT_ENV.get('DJANGO_WATCHMAN_TOKEN', None)
else:
    WATCHMAN_TOKEN = USER_ENV.get('DJANGO_WATCHMAN_TOKEN')

if 'DJANGO_WATCHMAN_TOKEN_NAME' not in USER_ENV:
    WATCHMAN_TOKEN_NAME = DEFAULT_ENV.get('DJANGO_WATCHMAN_TOKEN_NAME', 'token')
else:
    WATCHMAN_TOKEN_NAME = USER_ENV.get('DJANGO_WATCHMAN_TOKEN_NAME')

# Only report on the default database
WATCHMAN_DATABASES = ('default',)

# courses_enabled api
if 'COURSES_ENABLED' not in USER_ENV:
    COURSES_ENABLED = DEFAULT_ENV.get('COURSES_ENABLED', False)
else:
    COURSES_ENABLED = USER_ENV.get('COURSES_ENABLED')

# Defaults for PTVSD
if 'PTVSD_ENABLE' not in USER_ENV:
    PTVSD_ENABLE = DEFAULT_ENV.get("PTVSD_ENABLE", False)
else:
    PTVSD_ENABLE = USER_ENV.get("PTVSD_ENABLE")

if 'PTVSD_REMOTE_ADDRESS' not in USER_ENV:
    PTVSD_REMOTE_ADDRESS = DEFAULT_ENV.get("PTVSD_REMOTE_ADDRESS", "0.0.0.0")
else:
    PTVSD_REMOTE_ADDRESS = USER_ENV.get("PTVSD_REMOTE_ADDRESS")

if 'PTVSD_REMOTE_PORT' not in USER_ENV:
    PTVSD_REMOTE_PORT = DEFAULT_ENV.get("PTVSD_REMOTE_PORT", 3000)
else:
    PTVSD_REMOTE_PORT = USER_ENV.get("PTVSD_REMOTE_PORT")

if 'PTVSD_WAIT_FOR_ATTACH' not in USER_ENV:
    PTVSD_WAIT_FOR_ATTACH = DEFAULT_ENV.get("PTVSD_WAIT_FOR_ATTACH", False)
else:
    PTVSD_WAIT_FOR_ATTACH = USER_ENV.get("PTVSD_WAIT_FOR_ATTACH")

# Application definition

INSTALLED_APPS = [
    'dashboard',
    'django_ptvsd',
    'django_su',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_cron',
    'watchman',
    'macros',
    'debug_toolbar',
    'pinax.eventlog',
    'webpack_loader',
    'rules.apps.AutodiscoverRulesConfig',
]

CONSTANCE_CONFIG = {
    
}

# The order of this is important. It says DebugToolbar should be on top but
# The tips has it on the bottom
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CRON_CLASSES = [
    "dashboard.cron.DashboardCronJob",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if 'DJANGO_TEMPLATE_DEBUG' not in USER_ENV:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(APPLICATION_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'debug': DEFAULT_ENV.get('DJANGO_TEMPLATE_DEBUG', DEBUG),
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                    'django_su.context_processors.is_su',
                    'django_settings_export.settings_export',
                    'dashboard.context_processors.last_updated',
                    'dashboard.context_processors.get_git_version_info',
                ],
            },
        },
    ]
else:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(APPLICATION_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'debug': USER_ENV.get('DJANGO_TEMPLATE_DEBUG', DEBUG),
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                    'django_su.context_processors.is_su',
                    'django_settings_export.settings_export',
                    'dashboard.context_processors.last_updated',
                    'dashboard.context_processors.get_git_version_info',
                ],
            },
        },
    ]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

NPM_FILE_PATTERNS = {
    'bootstrap': ['dist/css/*'],
    'jquery': ['dist/jquery.min.js']
}

ROOT_URLCONF = 'dashboard.urls'

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': USER_ENV.get('MYSQL_ENGINE', 'django.db.backends.mysql'),
        'NAME': USER_ENV.get('MYSQL_DATABASE', 'student_dashboard'),  # your mysql database name
        'USER': USER_ENV.get('MYSQL_USER', 'student_dashboard_user'), # your mysql user for the database
        'PASSWORD': USER_ENV.get('MYSQL_PASSWORD', 'student_dashboard_password'), # password for user
        'HOST': USER_ENV.get('MYSQL_HOST', 'localhost'),
        'PORT': USER_ENV.get('MYSQL_PORT', 3306),
    },
    'DATA_WAREHOUSE': {
        'ENGINE': USER_ENV.get('DATA_WAREHOUSE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': USER_ENV.get('DATA_WAREHOUSE_DATABASE', ''),
        'USER': USER_ENV.get('DATA_WAREHOUSE_USER', ''),
        'PASSWORD': USER_ENV.get('DATA_WAREHOUSE_PASSWORD', ''),
        'HOST': USER_ENV.get('DATA_WAREHOUSE_HOST', ''),
        'PORT': USER_ENV.get('DATA_WAREHOUSE_PORT', 5432),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = USER_ENV.get("TIME_ZONE", USER_ENV.get("TZ", "America/Detroit"))

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

NPM_ROOT_PATH = BASE_DIR

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # Gunicorns logging format https://github.com/benoitc/gunicorn/blob/19.x/gunicorn/glogging.py
    'formatters': {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': USER_ENV.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'rules': {
            'handlers': ['console'],
            'propagate': False,
            'level': USER_ENV.get('RULES_LOG_LEVEL', 'INFO'),
        },
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },

    },
    'root': {
        'level': USER_ENV.get('ROOT_LOG_LEVEL', 'INFO'),
        'handlers': ['console']
    },
}


# IMPORT LOCAL ENV
# =====================
try:
    from settings_local import *
except ImportError:
    pass

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django_su.backends.SuBackend',
)

#Shib

# Give an opportunity to disable SAML
if USER_ENV.get('STUDENT_DASHBOARD_SAML'):
    import saml2

    SAML2_URL_PATH = '/accounts/'
    # modify to use port request comes
    SAML2_URL_BASE = USER_ENV.get('DJANGO_SAML2_URL_BASE', '/accounts/')
    SAML2_DEFAULT_IDP = USER_ENV.get('DJANGO_SAML2_DEFAULT_IDP', '')
    # Append the query parameter for idp to the default if it's set, otherwise do nothing
    if SAML2_DEFAULT_IDP:
        SAML2_DEFAULT_IDP = '?idp=%s' % SAML2_DEFAULT_IDP

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS += (
        'djangosaml2.backends.Saml2Backend',
    )
    LOGIN_URL = '%slogin/%s' % (SAML2_URL_PATH, SAML2_DEFAULT_IDP)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    SAML2_FILES_BASE = USER_ENV.get('SAML2_FILES_BASE', '/saml/')
    SAML2_REMOTE_METADATA = USER_ENV.get('SAML2_REMOTE_METADATA', '')
    SAML2_REMOTE_PEM_FILE = USER_ENV.get('SAML2_REMOTE_PEM_FILE', '')

    SAML_CONFIG = {
        'xmlsec_binary': '/usr/bin/xmlsec1',
        'entityid': '%smetadata/' % SAML2_URL_BASE,

        # directory with attribute mapping
        # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
        'name': 'Student Dashboard',
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                'name': 'Student Dashboard',
                'name_id_format': ('urn:oasis:names:tc:SAML:2.0:'
                                   'nameid-format:transient'),
                'authn_requests_signed': 'true',
                'allow_unsolicited': True,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        ('%sacs/' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view+

                    # do not change the binding or service name
                    'single_logout_service': [
                        ('%sls/' % SAML2_URL_BASE, saml2.BINDING_HTTP_REDIRECT),
                        ('%sls/post' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                },

                # attributes that this project need to identify a user
                'required_attributes': ['uid'],

                # attributes that may be useful to have but not required
                'optional_attributes': ['eduPersonAffiliation'],
            },
        },

        # where the remote metadata is stored
        'metadata': [{
            "class": "saml2.mdstore.MetaDataExtern",
            "metadata": [
                (SAML2_REMOTE_METADATA, SAML2_REMOTE_PEM_FILE)]
            }
        ],

        # set to 1 to output debugging information
        'debug': DEBUG,

        # certificate
        'key_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.key'),  'cert_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.pem'),
    }

    ACS_DEFAULT_REDIRECT_URL = USER_ENV.get('DJANGO_ACS_DEFAULT_REDIRECT', '/')
    LOGIN_REDIRECT_URL = USER_ENV.get('DJANGO_LOGIN_REDIRECT_URL', '/')

    LOGOUT_REDIRECT_URL = USER_ENV.get('DJANGO_LOGOUT_REDIRECT_URL', '/')

    SAML_CREATE_UNKNOWN_USER = True

    SAML_ATTRIBUTE_MAPPING = {
        'uid': ('username', ),
        'mail': ('email', ),
        'givenName': ('first_name', ),
        'sn': ('last_name', ),
    }
elif DEFAULT_ENV.get('STUDENT_DASHBOARD_SAML', True):
    import saml2

    SAML2_URL_PATH = '/accounts/'
    # modify to use port request comes
    SAML2_URL_BASE = DEFAULT_ENV.get('DJANGO_SAML2_URL_BASE', '/accounts/')
    SAML2_DEFAULT_IDP = DEFAULT_ENV.get('DJANGO_SAML2_DEFAULT_IDP', '')
    # Append the query parameter for idp to the default if it's set, otherwise do nothing
    if SAML2_DEFAULT_IDP:
        SAML2_DEFAULT_IDP = '?idp=%s' % SAML2_DEFAULT_IDP

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS += (
        'djangosaml2.backends.Saml2Backend',
    )
    LOGIN_URL = '%slogin/%s' % (SAML2_URL_PATH, SAML2_DEFAULT_IDP)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    SAML2_FILES_BASE = DEFAULT_ENV.get('SAML2_FILES_BASE', '/saml/')
    SAML2_REMOTE_METADATA = DEFAULT_ENV.get('SAML2_REMOTE_METADATA', '')
    SAML2_REMOTE_PEM_FILE = DEFAULT_ENV.get('SAML2_REMOTE_PEM_FILE', '')

    SAML_CONFIG = {
        'xmlsec_binary': '/usr/bin/xmlsec1',
        'entityid': '%smetadata/' % SAML2_URL_BASE,

        # directory with attribute mapping
        # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
        'name': 'Student Dashboard',
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                'name': 'Student Dashboard',
                'name_id_format': ('urn:oasis:names:tc:SAML:2.0:'
                                   'nameid-format:transient'),
                'authn_requests_signed': 'true',
                'allow_unsolicited': True,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        ('%sacs/' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view+

                    # do not change the binding or service name
                    'single_logout_service': [
                        ('%sls/' % SAML2_URL_BASE, saml2.BINDING_HTTP_REDIRECT),
                        ('%sls/post' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                },

                # attributes that this project need to identify a user
                'required_attributes': ['uid'],

                # attributes that may be useful to have but not required
                'optional_attributes': ['eduPersonAffiliation'],
            },
        },

        # where the remote metadata is stored
        'metadata': [{
            "class": "saml2.mdstore.MetaDataExtern",
            "metadata": [
                (SAML2_REMOTE_METADATA, SAML2_REMOTE_PEM_FILE)]
            }
        ],

        # set to 1 to output debugging information
        'debug': DEBUG,

        # certificate
        'key_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.key'),  'cert_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.pem'),
    }

    ACS_DEFAULT_REDIRECT_URL = DEFAULT_ENV.get('DJANGO_ACS_DEFAULT_REDIRECT', '/')
    LOGIN_REDIRECT_URL = DEFAULT_ENV.get('DJANGO_LOGIN_REDIRECT_URL', '/')

    LOGOUT_REDIRECT_URL = DEFAULT_ENV.get('DJANGO_LOGOUT_REDIRECT_URL', '/')

    SAML_CREATE_UNKNOWN_USER = True

    SAML_ATTRIBUTE_MAPPING = {
        'uid': ('username', ),
        'mail': ('email', ),
        'givenName': ('first_name', ),
        'sn': ('last_name', ),
    }
else:
    AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL='/'

# Give an opportunity to disable LTI
if USER_ENV.get('STUDENT_DASHBOARD_LTI'):
    INSTALLED_APPS += ('django_lti_auth',)
    if not 'django.contrib.auth.backends.ModelBackend' in AUTHENTICATION_BACKENDS:
        AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)

    PYLTI_CONFIG = {
        "consumers": USER_ENV.get("PYLTI_CONFIG_CONSUMERS", {}),
        "method_hooks":{
            "valid_lti_request": "dashboard.lti.valid_lti_request",
            "invalid_lti_request": "dashboard.lti.invalid_lti_request"
        },
        "next_url": "home"
    }
    LTI_PERSON_SOURCED_ID_FIELD = USER_ENV.get('LTI_PERSON_SOURCED_ID_FIELD',
        "custom_canvas_user_login_id")
    LTI_EMAIL_FIELD = USER_ENV.get('LTI_EMAIL_FIELD',
        "lis_person_contact_email_primary")
    LTI_CANVAS_COURSE_ID_FIELD = USER_ENV.get('LTI_CANVAS_COURSE_ID_FIELD',
        "custom_canvas_course_id")
    LTI_FIRST_NAME = USER_ENV.get('LTI_FIRST_NAME',
        "lis_person_name_given")
    LTI_LAST_NAME = USER_ENV.get('LTI_LAST_NAME',
        "lis_person_name_family")
elif DEFAULT_ENV.get('STUDENT_DASHBOARD_LTI', False):
    INSTALLED_APPS += ('django_lti_auth',)
    if not 'django.contrib.auth.backends.ModelBackend' in AUTHENTICATION_BACKENDS:
        AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)

    PYLTI_CONFIG = {
        "consumers": DEFAULT_ENV.get("PYLTI_CONFIG_CONSUMERS", {}),
        "method_hooks":{
            "valid_lti_request": "dashboard.lti.valid_lti_request",
            "invalid_lti_request": "dashboard.lti.invalid_lti_request"
        },
        "next_url": "home"
    }
    LTI_PERSON_SOURCED_ID_FIELD = DEFAULT_ENV.get('LTI_PERSON_SOURCED_ID_FIELD',
        "custom_canvas_user_login_id")
    LTI_EMAIL_FIELD = DEFAULT_ENV.get('LTI_EMAIL_FIELD',
        "lis_person_contact_email_primary")
    LTI_CANVAS_COURSE_ID_FIELD = DEFAULT_ENV.get('LTI_CANVAS_COURSE_ID_FIELD',
        "custom_canvas_course_id")
    LTI_FIRST_NAME = DEFAULT_ENV.get('LTI_FIRST_NAME',
        "lis_person_name_given")
    LTI_LAST_NAME = DEFAULT_ENV.get('LTI_LAST_NAME',
        "lis_person_name_family")
    
# controls whether Unizin specific features/data is available from the Canvas Data source
if 'DATA_WAREHOUSE_IS_UNIZIN' not in USER_ENV:
    DATA_WAREHOUSE_IS_UNIZIN = DEFAULT_ENV.get("DATA_WAREHOUSE_IS_UNIZIN", True)
else:
    DATA_WAREHOUSE_IS_UNIZIN = USER_ENV.get("DATA_WAREHOUSE_IS_UNIZIN")

# This is used to fix ids from Canvas Data which are incremented by some large number
if 'CANVAS_DATA_ID_INCREMENT' not in USER_ENV:
    CANVAS_DATA_ID_INCREMENT = DEFAULT_ENV.get("CANVAS_DATA_ID_INCREMENT", 17700000000000000)
else:
    CANVAS_DATA_ID_INCREMENT = USER_ENV.get("CANVAS_DATA_ID_INCREMENT")

# Allow enabling/disabling the View options globally
if 'VIEWS_DISABLED' not in USER_ENV:
    VIEWS_DISABLED = DEFAULT_ENV.get('VIEWS_DISABLED', [])
else:
    VIEWS_DISABLED = USER_ENV.get('VIEWS_DISABLED')

# Time to run cron
if 'RUN_AT_TIMES' not in USER_ENV:
    RUN_AT_TIMES = DEFAULT_ENV.get('RUN_AT_TIMES', [])
else:
    RUN_AT_TIMES = USER_ENV.get('RUN_AT_TIMES')

# Add any settings you need to be available to templates in this array
SETTINGS_EXPORT = ['LOGIN_URL','LOGOUT_URL','DEBUG', 'GA_ID', 'RESOURCE_VALUES']

# Method to show the user, if they're authenticated and superuser
def show_debug_toolbar(request):
    return DEBUG and request.user and request.user.is_authenticated and request.user.is_superuser

DEBUG_TOOLBAR_PANELS = dt_settings.PANELS_DEFAULTS

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_debug_toolbar,
}

# Number of weeks max to allow by default. some begin/end dates in Canvas aren't correct
if 'MAX_DEFAULT_WEEKS' not in USER_ENV:
    MAX_DEFAULT_WEEKS = DEFAULT_ENV.get("MAX_DEFAULT_WEEKS", 16)
else:
    MAX_DEFAULT_WEEKS = USER_ENV.get("MAX_DEFAULT_WEEKS")

if 'CLIENT_CACHE_TIME' not in USER_ENV:
    CLIENT_CACHE_TIME = DEFAULT_ENV.get("CLIENT_CACHE_TIME", 3600)
else:
    CLIENT_CACHE_TIME = USER_ENV.get("CLIENT_CACHE_TIME")

if 'CRON_BQ_IN_LIMIT' not in USER_ENV:
    CRON_BQ_IN_LIMIT = DEFAULT_ENV.get("CRON_BQ_IN_LIMIT", 20)
else:
    CRON_BQ_IN_LIMIT = USER_ENV.get("CRON_BQ_IN_LIMIT")

if 'CANVAS_FILE_PREFIX' not in USER_ENV:
    CANVAS_FILE_PREFIX = DEFAULT_ENV.get("CANVAS_FILE_PREFIX", "")
else:
    CANVAS_FILE_PREFIX = USER_ENV.get("CANVAS_FILE_PREFIX")

if 'CANVAS_FILE_POSTFIX' not in USER_ENV:
    CANVAS_FILE_POSTFIX = DEFAULT_ENV.get("CANVAS_FILE_POSTFIX", "")
else:
    CANVAS_FILE_POSTFIX = USER_ENV.get("CANVAS_FILE_POSTFIX")

# strings for construct file download url

CANVAS_FILE_ID_NAME_SEPARATOR = "|"

if 'RESOURCE_ACCESS_CONFIG' not in USER_ENV:
    RESOURCE_ACCESS_CONFIG = DEFAULT_ENV.get("RESOURCE_ACCESS_CONFIG", {})
else:
    RESOURCE_ACCESS_CONFIG = USER_ENV.get("RESOURCE_ACCESS_CONFIG")

# Git info settings
SHA_ABBREV_LENGTH = 7

# Django CSP Settings, load up from file if set
if "CSP" in DEFAULT_ENV:
    MIDDLEWARE += ['csp.middleware.CSPMiddleware',]
    for csp_key, csp_val in DEFAULT_ENV.get("CSP").items():
        # If there's a value set for this CSP config, set it as a global
        if (csp_val):
            globals()["CSP_"+csp_key] = csp_val
elif "CSP" in USER_ENV:
    MIDDLEWARE += ['csp.middleware.CSPMiddleware',]
    for csp_key, csp_val in USER_ENV.get("CSP").items():
        # If there's a value set for this CSP config, set it as a global
        if (csp_val):
            globals()["CSP_"+csp_key] = csp_val
# If CSP not set, add in XFrameOptionsMiddleware
else:
    MIDDLEWARE += ['django.middleware.clickjacking.XFrameOptionsMiddleware',]

# These are mostly needed by Canvas but it should also be in on general 
if 'CSRF_COOKIE_SECURE' not in USER_ENV:
    CSRF_COOKIE_SECURE = DEFAULT_ENV.get("CSRF_COOKIE_SECURE", False)
else:
    CSRF_COOKIE_SECURE = USER_ENV.get("CSRF_COOKIE_SECURE")

if CSRF_COOKIE_SECURE:
    if 'CSRF_TRUSTED_ORIGINS' not in USER_ENV:
        CSRF_TRUSTED_ORIGINS = DEFAULT_ENV.get("CSRF_TRUSTED_ORIGINS", [])
    else:
        CSRF_TRUSTED_ORIGINS = USER_ENV.get("CSRF_TRUSTED_ORIGINS")

    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# IMPORT LOCAL ENV
# =====================
try:
    from settings_local import *
except ImportError:
    pass
