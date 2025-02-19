"""
Settings for Tethys Platform

***************************************************************************
*
*   WARNING!!!!
*
*   The settings.py file should no longer be edited to customize your local
*   settings. All portal configuration should now happen in the portal_config.yml
*   file (See docs/tethys_portal/configuration.rst).
*
***************************************************************************

This file contains default Django and other settings for the Tethys Platform.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# Build paths inside the project like this: BASE_DIR / '...'
import os
import sys
import yaml
import logging
import datetime as dt
from pathlib import Path
from importlib import import_module
from importlib.machinery import SourceFileLoader

from django.contrib.messages import constants as message_constants

from tethys_apps.utilities import relative_to_tethys_home
from tethys_utils import deprecation_warning
from tethys_cli.gen_commands import generate_secret_key
from tethys_portal.optional_dependencies import optional_import, has_module

# optional imports
bokeh_settings = optional_import("settings", from_module="bokeh.settings")
bokeh_django = optional_import("bokeh_django")

log = logging.getLogger(__name__)
this_module = sys.modules[__name__]

BASE_DIR = Path(__file__).parent

portal_config_settings = {}
try:
    with relative_to_tethys_home("portal_config.yml").open() as portal_yaml:
        portal_config_settings = yaml.safe_load(portal_yaml).get("settings", {}) or {}
except FileNotFoundError:
    log.info(
        "Could not find the portal_config.yml file. To generate a new portal_config.yml run the command "
        '"tethys gen portal_config"'
    )
except Exception:
    log.exception(
        "There was an error while attempting to read the settings from the portal_config.yml file."
    )

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = portal_config_settings.pop("SECRET_KEY", generate_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = portal_config_settings.pop("DEBUG", True)

ALLOWED_HOSTS = portal_config_settings.pop("ALLOWED_HOSTS", [])

# List those who should be notified of an error when DEBUG = False as a tuple of (name, email address).
# i.e.: ADMINS = (('John', 'john@example.com'), ('Mary', 'mary@example.com'))
ADMINS = portal_config_settings.pop("ADMINS", ())

TETHYS_PORTAL_CONFIG = portal_config_settings.pop("TETHYS_PORTAL_CONFIG", {})
# Use this setting to bypass the home page
BYPASS_TETHYS_HOME_PAGE = TETHYS_PORTAL_CONFIG.pop("BYPASS_TETHYS_HOME_PAGE", False)

# Use this setting to disable open account signup
ENABLE_OPEN_SIGNUP = TETHYS_PORTAL_CONFIG.pop("ENABLE_OPEN_SIGNUP", False)

# Set to True to allow Open Portal mode. This mode supersedes any specific user/group app access permissions
ENABLE_OPEN_PORTAL = TETHYS_PORTAL_CONFIG.pop("ENABLE_OPEN_PORTAL", False)

# Set to True to allow Open Portal mode. This mode supersedes any specific user/group app access permissions
ENABLE_RESTRICTED_APP_ACCESS = TETHYS_PORTAL_CONFIG.pop(
    "ENABLE_RESTRICTED_APP_ACCESS", False
)

REGISTER_CONTROLLER = TETHYS_PORTAL_CONFIG.pop("REGISTER_CONTROLLER", None)

MULTIPLE_APP_MODE = TETHYS_PORTAL_CONFIG.pop("MULTIPLE_APP_MODE", True)
STANDALONE_APP = TETHYS_PORTAL_CONFIG.pop("STANDALONE_APP", None)
if not MULTIPLE_APP_MODE:
    BYPASS_TETHYS_HOME_PAGE = True

ADDITIONAL_URLPATTERNS = TETHYS_PORTAL_CONFIG.pop("ADDITIONAL_URLPATTERNS", [])

SESSION_CONFIG = portal_config_settings.pop("SESSION_CONFIG", {})
# Force user logout once the browser has been closed.
# If changed, delete all django_session table entries from the tethys_default database to ensure updated behavior
SESSION_EXPIRE_AT_BROWSER_CLOSE = SESSION_CONFIG.pop(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", True
)

# Warn user of forced logout after indicated number of seconds
SESSION_SECURITY_WARN_AFTER = SESSION_CONFIG.pop("SESSION_SECURITY_WARN_AFTER", 840)

# Force user logout after a certain number of seconds
SESSION_SECURITY_EXPIRE_AFTER = SESSION_CONFIG.pop("SESSION_SECURITY_EXPIRE_AFTER", 900)

# add any additional SESSION_CONFIG settings
for setting, value in SESSION_CONFIG.items():
    setattr(this_module, setting, value)

DATABASES = portal_config_settings.pop("DATABASES", {})
DATABASES.setdefault("default", {})
DEFAULT_DB = DATABASES["default"]

# ###########
# backwards compatibility logic
# TODO remove compatibility code with Tethys 5.0
warning_message = (
    "{intro}\n"
    "The default database engine is changing from postgresql to sqlite3.\n"
    "To continue using postgresql in the future you will need to configure the "
    '{properties} of the "default" database.\n'
    "This can be done with the following command:\n\n"
    "tethys settings {command_options}\n\n"
)
if bool(DEFAULT_DB):
    # check if default DB is configured with postgres keys, but doesn't specify the "ENGINE"
    if "ENGINE" not in DEFAULT_DB:
        if {"DIR", "USER", "PASSWORD", "HOST", "PORT"}.intersection(
            set(DEFAULT_DB.keys())
        ):
            DEFAULT_DB["ENGINE"] = "django.db.backends.postgresql"
            deprecation_warning(
                version="5.0",
                feature="Using postgresql as the default database engine",
                message=warning_message.format(
                    intro="",
                    properties='"ENGINE" property',
                    command_options="--set DATABASES.default.ENGINE django.db.backends.postgresql",
                ),
            )
else:
    # check if default local database exists
    db_dir = relative_to_tethys_home("psql")
    if db_dir.exists():
        DEFAULT_DB["DIR"] = "psql"
        deprecation_warning(
            version="5.0",
            feature="Using postgresql as the default database engine",
            message=warning_message.format(
                intro="WARNING!!!\nIt appears that you have a local PostgreSQL database that was configured by Tethys.",
                properties='"ENGINE" and "DIR" properties',
                command_options="--set DATABASES.default.ENGINE django.db.backends.postgresql "
                "--set DATABASES.default.DIR psql",
            ),
        )

# end compatibility code
# ###########

DEFAULT_DB.setdefault("ENGINE", "django.db.backends.sqlite3")

if "sqlite" in DEFAULT_DB["ENGINE"]:
    DEFAULT_DB.setdefault(
        "NAME", relative_to_tethys_home("tethys_platform.sqlite", as_str=True)
    )
else:
    DEFAULT_DB.setdefault("NAME", "tethys_platform")
    DEFAULT_DB.setdefault("USER", "tethys_default")
    DEFAULT_DB.setdefault("PASSWORD", "pass")
    DEFAULT_DB.setdefault("HOST", "localhost")
    DEFAULT_DB.setdefault("PORT", 5436)


# See https://docs.djangoproject.com/en/3.2/ref/settings/#logging-config for more logging configuration options.
LOGGING = portal_config_settings.pop("LOGGING", {})
LOGGING.setdefault("version", 1)
LOGGING.setdefault("disable_existing_loggers", False)
LOGGING.setdefault(
    "formatters",
    {
        "verbose": {"format": "%(levelname)s:%(name)s:%(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
)
LOGGING.setdefault(
    "handlers",
    {
        "console_simple": {"class": "logging.StreamHandler", "formatter": "simple"},
        "console_verbose": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
)
LOGGING.setdefault("loggers", {})
LOGGERS = LOGGING["loggers"]
LOGGERS.setdefault(
    "django",
    {
        "handlers": ["console_simple"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "WARNING"),
    },
)
LOGGERS.setdefault(
    "tethys",
    {
        "handlers": ["console_verbose"],
        "level": "INFO",
    },
)
LOGGERS.setdefault(
    "tethysapp",
    {
        "handlers": ["console_verbose"],
        "level": "INFO",
    },
)

default_installed_apps = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "tethys_apps",
    "tethys_compute",
    "tethys_config",
    "tethys_gizmos",
    "tethys_layouts",
    "tethys_sdk",
    "tethys_services",
    "tethys_quotas",
    "guardian",
]

for module in [
    "analytical",
    "axes",
    "captcha",
    "corsheaders",
    "django_gravatar",
    "django_json_widget",
    "mfa",
    "oauth2_provider",
    "rest_framework",
    "rest_framework.authtoken",
    "session_security",
    "django_recaptcha",
    "social_django",
    "termsandconditions",
]:
    if has_module(module):
        default_installed_apps.append(module)


INSTALLED_APPS = portal_config_settings.pop(
    "INSTALLED_APPS_OVERRIDE",
    default_installed_apps,
)

INSTALLED_APPS = tuple(
    INSTALLED_APPS + portal_config_settings.pop("INSTALLED_APPS", [])
)

MIDDLEWARE = portal_config_settings.pop(
    "MIDDLEWARE_OVERRIDE",
    [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "tethys_portal.middleware.TethysMfaRequiredMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "tethys_portal.middleware.TethysAppAccessMiddleware",
    ],
)
if has_module("corsheaders"):
    MIDDLEWARE.insert(
        MIDDLEWARE.index(
            "django.middleware.common.CommonMiddleware"
        ),  # insert right before
        "corsheaders.middleware.CorsMiddleware",
    )
if has_module("social_django"):
    MIDDLEWARE.append("tethys_portal.middleware.TethysSocialAuthExceptionMiddleware")
if has_module("session_security"):
    MIDDLEWARE.append(
        "session_security.middleware.SessionSecurityMiddleware"
    )  # TODO: Templates need to be upgraded
if has_module("axes"):
    MIDDLEWARE.append("axes.middleware.AxesMiddleware")

MIDDLEWARE = tuple(MIDDLEWARE + portal_config_settings.pop("MIDDLEWARE", []))

default_authentication_backends = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

if has_module("axes"):
    default_authentication_backends.insert(0, "axes.backends.AxesBackend")

AUTHENTICATION_BACKENDS = portal_config_settings.pop(
    "AUTHENTICATION_BACKENDS_OVERRIDE",
    default_authentication_backends,
)
AUTHENTICATION_BACKENDS = tuple(
    portal_config_settings.pop("AUTHENTICATION_BACKENDS", []) + AUTHENTICATION_BACKENDS
)

RESOURCE_QUOTA_HANDLERS = portal_config_settings.pop(
    "RESOURCE_QUOTA_HANDLERS_OVERRIDE",
    [
        "tethys_quotas.handlers.workspace.WorkspaceQuotaHandler",
    ],
)
RESOURCE_QUOTA_HANDLERS = tuple(
    RESOURCE_QUOTA_HANDLERS + portal_config_settings.pop("RESOURCE_QUOTA_HANDLERS", [])
)

SUPPRESS_QUOTA_WARNINGS = portal_config_settings.pop(
    "SUPPRESS_QUOTA_WARNINGS", ["user_workspace_quota", "app_workspace_quota"]
)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# Terms and conditions settings
ACCEPT_TERMS_PATH = "/terms/accept/"
TERMS_EXCLUDE_URL_PREFIX_LIST = {
    "/admin/",
    "/oauth2/",
    "/handoff/",
    "/accounts/",
    "/terms/",
}
TERMS_EXCLUDE_URL_LIST = {"/"}
TERMS_BASE_TEMPLATE = "termsandconditions_base.html"

ROOT_URLCONF = "tethys_portal.urls"

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

default_context_processors = [
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.template.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    # "social_django.context_processors.backends",
    # "social_django.context_processors.login_redirect",
    "tethys_config.context_processors.tethys_global_settings_context",
    "tethys_apps.context_processors.tethys_apps_context",
    "tethys_gizmos.context_processors.tethys_gizmos_context",
    "tethys_portal.context_processors.tethys_portal_context",
]
if has_module("social_django"):
    default_context_processors.extend(
        [
            "social_django.context_processors.backends",
            "social_django.context_processors.login_redirect",
        ]
    )

# Templates

ADDITIONAL_TEMPLATE_DIRS = [
    import_module(d).__path__[0]
    for d in TETHYS_PORTAL_CONFIG.get("ADDITIONAL_TEMPLATE_DIRS", [])
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            *ADDITIONAL_TEMPLATE_DIRS,
            BASE_DIR / "templates",
        ],
        "OPTIONS": {
            "context_processors": default_context_processors,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "tethys_apps.template_loaders.TethysTemplateLoader",
            ],
            "debug": DEBUG,
        },
    }
]


# Static files (CSS, JavaScript, Images)
STATIC_URL = portal_config_settings.pop("STATIC_URL", "/static/")


STATICFILES_DIRS = [
    BASE_DIR / "static",
]
if has_module(bokeh_settings):
    try:
        bokeh_js_dir = bokeh_settings.bokehjs_path()
    except AttributeError:
        # support bokeh versions < 3.4
        bokeh_js_dir = bokeh_settings.bokehjsdir()
    STATICFILES_DIRS.append(bokeh_js_dir)

STATICFILES_USE_NPM = TETHYS_PORTAL_CONFIG.pop("STATICFILES_USE_NPM", False)
if STATICFILES_USE_NPM:
    STATICFILES_DIRS.append(BASE_DIR / "static" / "node_modules")

if has_module(bokeh_settings):
    bokeh_settings.resources = portal_config_settings.pop(
        "BOKEH_RESOURCES", "server" if STATICFILES_USE_NPM else "cdn"
    )

STATICFILES_FINDERS = portal_config_settings.pop(
    "STATICFILES_FINDERS_OVERRIDE",
    [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "tethys_apps.static_finders.TethysStaticFinder",
    ],
)
if has_module(bokeh_django):
    STATICFILES_FINDERS.append("bokeh_django.static.BokehExtensionFinder")

STATICFILES_FINDERS = (
    *STATICFILES_FINDERS,
    *portal_config_settings.pop("STATICFILES_FINDERS", []),
)

STATIC_ROOT = TETHYS_PORTAL_CONFIG.pop(
    "STATIC_ROOT", relative_to_tethys_home("static", as_str=True)
)

TETHYS_WORKSPACES_ROOT = TETHYS_PORTAL_CONFIG.pop(
    "TETHYS_WORKSPACES_ROOT", relative_to_tethys_home("workspaces", as_str=True)
)

MEDIA_URL = portal_config_settings.pop("MEDIA_URL", "/media/")
MEDIA_ROOT = portal_config_settings.pop(
    "MEDIA_ROOT", relative_to_tethys_home("media", as_str=True)
)

# add any additional TETHYS_PORTAL_CONFIG settings
for setting, value in TETHYS_PORTAL_CONFIG.items():
    setattr(this_module, setting, value)

# Messaging settings
MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-danger",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger",
}

# Email Configuration
EMAIL_CONFIG = portal_config_settings.pop("EMAIL_CONFIG", {})
EMAIL_FROM = portal_config_settings.pop("EMAIL_FROM", "")
for setting, value in EMAIL_CONFIG.items():
    setattr(this_module, setting, value)

# Gravatar Settings
GRAVATAR_URL = "http://www.gravatar.com/"
GRAVATAR_SECURE_URL = "https://secure.gravatar.com/"
GRAVATAR_DEFAULT_SIZE = "80"
GRAVATAR_DEFAULT_IMAGE = "retro"
GRAVATAR_DEFAULT_RATING = "g"
GRAVATAR_DEFAULT_SECURE = True

# OAuth Settings
# http://psa.matiasaguirre.net/docs/configuration/index.html
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ["username", "first_name", "email"]
SOCIAL_AUTH_SLUGIFY_USERNAMES = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/apps/"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/accounts/login/"
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ["tenant"]

# OAuth Providers
OAUTH_CONFIG = portal_config_settings.pop("OAUTH_CONFIG", {})
for setting, value in OAUTH_CONFIG.items():
    setattr(this_module, setting, value)

OAUTH2_PROVIDER_URL_NAMESPACE = OAUTH_CONFIG.get(
    "OAUTH2_PROVIDER", portal_config_settings.get("OAUTH2_PROVIDER", {})
).pop("URL_NAMESPACE", "o")

# MFA Settings
# See: https://github.com/mkalioby/django-mfa2
# Methods that shouldn't be allowed for the user, U2F, FIDO2, TOTP, Trusted_Devices, Email
MFA_REQUIRED = False  # Require all users to set up MFA
SSO_MFA_REQUIRED = (
    False  # Require users logged in with SSO to set up MFA when MFA_REQUIRED is True
)
ADMIN_MFA_REQUIRED = True  # Require admin users to set up MFA when MFA_REQUIRED is True
MFA_UNALLOWED_METHODS = ("U2F", "FIDO2", "Email", "Trusted_Devices")
# A function that should be called by username to login the user in session
MFA_LOGIN_CALLBACK = "tethys_portal.utilities.log_user_in"
MFA_RECHECK = False  # Allow random rechecking of the user
MFA_RECHECK_MIN = 600  # Minimum interval in seconds
MFA_RECHECK_MAX = 1800  # Maximum in seconds
MFA_QUICKLOGIN = (
    False  # Allow quick login for returning users by provide only their 2FA
)
MFA_HIDE_DISABLE = ("FIDO2",)  # Can the user disable his key (Added in 1.2.0).
MFA_OWNED_BY_ENTERPRISE = False  # Who owns security keys
TOKEN_ISSUER_NAME = "Tethys Portal"  # TOTP Issuer name
MFA_SUCCESS_REGISTRATION_MSG = ""

U2F_APPID = "http://localhost"  # URL For U2F
FIDO_SERVER_ID = (
    "localhost"  # Server rp id for FIDO2, it's the full domain of your project
)
FIDO_SERVER_NAME = "Tethys Portal"
FIDO_LOGIN_URL = portal_config_settings.pop("FIDO_LOGIN_URL", "/auth/login")

MFA_CONFIG = portal_config_settings.pop("MFA_CONFIG", {})

for setting, value in MFA_CONFIG.items():
    setattr(this_module, setting, value)

# Lockout Configuration
AXES_ENABLED = not DEBUG
AXES_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = dt.timedelta(hours=0.5)
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_ENABLE_ADMIN = True
AXES_LOCKOUT_TEMPLATE = "tethys_portal/accounts/lockout.html"
AXES_VERBOSE = True
AXES_RESET_ON_SUCCESS = True

LOCKOUT_CONFIG = portal_config_settings.pop("LOCKOUT_CONFIG", {})
for setting, value in LOCKOUT_CONFIG.items():
    if setting == "AXES_COOLOFF_TIME" and isinstance(value, str):
        import isodate

        try:
            value = isodate.parse_duration(value)
        except Exception:
            pass

    setattr(this_module, setting, value)

# Django Guardian Settings
ANONYMOUS_USER_ID = -1

CAPTCHA_CONFIG = portal_config_settings.pop("CAPTCHA_CONFIG", {})
# RECAPTCHA values need a default or else they will throw an error
#  - Alternative is to set SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
CAPTCHA_CONFIG.setdefault("RECAPTCHA_PRIVATE_KEY", None)
CAPTCHA_CONFIG.setdefault("RECAPTCHA_PUBLIC_KEY", None)
for setting, value in CAPTCHA_CONFIG.items():
    setattr(this_module, setting, value)

# Placeholders for the ID's required by various web-analytics services supported by Django-Analytical.
# Replace False with the tracking ID as a string e.g. SERVICE_ID = 'abcd1234'
ANALYTICS_CONFIG = portal_config_settings.pop("ANALYTICS_CONFIG", {})
for setting, value in ANALYTICS_CONFIG.items():
    setattr(this_module, setting, value)

ASGI_APPLICATION = "tethys_portal.asgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

COOKIE_CONFIG = portal_config_settings.pop("COOKIE_CONFIG", {})
for setting, value in COOKIE_CONFIG.items():
    setattr(this_module, setting, value)

CORS_CONFIG = portal_config_settings.pop("CORS_CONFIG", {})
for setting, value in CORS_CONFIG.items():
    setattr(this_module, setting, value)

LOGIN_URL = portal_config_settings.pop("LOGIN_URL", "/accounts/login/")
PREFIX_URL = portal_config_settings.pop("PREFIX_URL", "/")
if PREFIX_URL is not None and PREFIX_URL != "/":
    PREFIX_URL = f"{PREFIX_URL.strip('/')}"
    STATIC_URL = f"/{PREFIX_URL}/{STATIC_URL.strip('/')}/"
    LOGIN_URL = f"/{PREFIX_URL}/{LOGIN_URL.strip('/')}/"
    FIDO_LOGIN_URL = f"/{PREFIX_URL}/{FIDO_LOGIN_URL.strip('/')}/"


def get__all__(mod):
    try:
        return mod.__all__
    except AttributeError:
        return [a for a in dir(mod) if not a.startswith("__")]


ADDITIONAL_SETTINGS_FILES = TETHYS_PORTAL_CONFIG.pop("ADDITIONAL_SETTINGS_FILES", [])
for settings_module in ADDITIONAL_SETTINGS_FILES:
    mod = (
        SourceFileLoader("mod", settings_module).load_module()
        if Path(settings_module).is_file()
        else import_module(settings_module)
    )
    all_settings = get__all__(mod)
    for setting in all_settings:
        value = getattr(mod, setting)
        setattr(this_module, setting, value)

# TODO backward compatibility setting. Remove in Tethys 5.0
USE_OLD_WORKSPACES_API = portal_config_settings.pop("USE_OLD_WORKSPACES_API", True)

# Add any additional specified settings to module
for setting, value in portal_config_settings.items():
    setattr(this_module, setting, value)
