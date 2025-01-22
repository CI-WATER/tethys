.. _tethys_configuration:

***************************
Tethys Portal Configuration
***************************

Beginning in Tethys Platform 3.0 the Tethys Portal is configured via a :file:`portal_config.yml` file in the :file:`$TETHYS_HOME/` directory. This instructions outline the various settings that can be added to the :file:`portal_config.yml` file.

Once you have installed Tethys you can generate a new :file:`portal_config.yml` file using the ``gen`` command. (See :ref:`tethys_gen_cmd` for more information).

.. code-block::bash

  tethys gen portal_config

This will create a new :file:`portal_config.yml` file in your ``TETHYS_HOME`` directory that looks like this:

.. literalinclude:: ../installation/resources/blank-portal-config.yml
   :language: yaml

Portal Yaml Keys
----------------

The following sections describe the keys that can be added to the :file:`portal_config.yml` file. These first two keys are just metadata and don't affect the portal.

* **version**: the version of the :file:`portal_config.yml` file schema.
* **name**: the name of the :file:`portal_config.yml`.

The next three sections describe different types of settings that allow you to customize the behavior and appearance of your portal. Note that the settings for each section are applied in different ways. The mechanism for applying the settings is noted in a comment at the top of the section in the :file:`portal_config.yml` file, and will also be described for each section below.

Apps
====

* **apps**: settings for apps installed in this portal (see: :ref:`app_installation`).

.. tip::

  This section is applied when running the "tethys install" command. Tethys will first look for app settings in this file. If none are found it will then look for a "services.yml" file in the install location.



Settings
========

Tethys Portal settings. Note: do not edit the :file:`settings.py` file directly, Instead set any Django setting in this section, even those not listed here. If you need to use Python logic to set specific settings, then you can use the ``ADDITIONAL_SETTINGS_FILES`` key under the ``TETHYS_PORTAL_CONFIG`` key to specify additional Python files to include in the :file:`settings.py` file (see :ref:`tethys_portal_config_settings`).

.. tip::

  You can customize these settings either by manually editing the :file:`portal_config.yml` file, or by using the :ref:`tethys_settings_cmd`.

  .. caution::

    The :ref:`tethys_settings_cmd` will rewrite the :file:`portal_config.yml` file each time it is run and will not preserve user-added comments.


================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
SECRET_KEY                                         the Django `SECRET_KEY <https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key>`_ setting. Automatically generated if not set, however setting it manually is recommended.
DEBUG                                              the Django `DEBUG <https://docs.djangoproject.com/en/4.2/ref/settings/#debug>`_ setting. Defaults to True.
ALLOWED_HOSTS                                      the Django `ALLOWED_HOSTS <https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts>`_ setting. Defaults to ``[]``.
ADMINS                                             the Django `ADMINS <https://docs.djangoproject.com/en/4.2/ref/settings/#admins>`_ setting.
INSTALLED_APPS                                     the Django `INSTALLED_APPS <https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps>`_ setting. For convenience, any Django apps listed here will be appended to default list of Django apps required by Tethys. To override ``INSTALLED_APPS`` completely, use the ``INSTALLED_APPS_OVERRIDE`` setting.
INSTALLED_APPS_OVERRIDE                            override for ``INSTALLED_APPS`` setting. CAUTION: improper use of this setting can break the Tethys Portal.
MIDDLEWARE                                         the Django `MIDDLEWARE <https://docs.djangoproject.com/en/4.2/ref/settings/#middleware>`_ setting. For convenience, any middleware listed here will be appended to default list of middleware required by Tethys. To override ``MIDDLEWARE`` completely, use the ``MIDDLEWARE_OVERRIDE`` setting.
MIDDLEWARE_OVERRIDE                                override for ``MIDDLEWARE`` setting. CAUTION: improper use of this setting can break the Tethys Portal.
AUTHENTICATION_BACKENDS                            the Django `AUTHENTICATION_BACKENDS <https://docs.djangoproject.com/en/4.2/ref/settings/#authentication-backends>`_ setting. For convenience, any authentication backends listed here will be appended to default list of authentication backends required by Tethys. To override ``AUTHENTICATION_BACKENDS`` completely, use the ``AUTHENTICATION_BACKENDS_OVERRIDE`` setting.
AUTHENTICATION_BACKENDS_OVERRIDE                   override for ``AUTHENTICATION_BACKENDS`` setting. CAUTION: improper use of this setting can break the Tethys Portal.
CONTEXT_PROCESSORS                                 the `context_processors` option of the Django `TEMPLATES <https://docs.djangoproject.com/en/4.2/ref/settings/#templates>`_ setting. For convenience, any context processor functions listed here will be appended to default list of context processors used by Tethys. To override ``CONTEXT_PROCESSORS`` completely, use the ``CONTEXT_PROCESSORS_OVERRIDE`` setting.
CONTEXT_PROCESSORS_OVERRIDE                        override for ``CONTEXT_PROCESSORS`` setting. CAUTION: improper use of this setting can break the Tethys Portal.
RESOURCE_QUOTA_HANDLERS                            a list of Tethys ``ResourceQuotaHandler`` classes to load (see: :ref:`sdk_quotas_api`). For convenience, any quota handlers listed here will be appended to the default list of quota handlerss. To override ``RESOURCE_QUOTA_HANDLERS`` completely, use the ``RESOURCE_QUOTA_HANDLERS_OVERRIDE`` setting.
RESOURCE_QUOTA_HANDLERS_OVERRIDE                   override for ``RESOURCE_QUOTA_HANDLERS`` setting. CAUTION: improper use of this setting can break the Tethys Portal.
USE_OLD_WORKSPACES_API                             a temporary setting that maintains backward compatibility for the :ref:`tethys_workspaces_api` when True. When False the the new :ref:`tethys_paths_api` functionality will apply. Defaults to True. Will be removed in 5.0.
================================================== ================================================================================

.. _tethys_portal_config_settings:

TETHYS_PORTAL_CONFIG
++++++++++++++++++++

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
ENABLE_OPEN_SIGNUP                                 anyone can create a Tethys Portal account using a "Sign Up" link on the home page when ``True``. Defaults to ``False``.
REGISTER_CONTROLLER                                override the default registration page with a custom controller. The value should be the dot-path to the controller function/class (e.g. ``tethysext.my_extension.controllers.custom_registration``)
ENABLE_OPEN_PORTAL                                 no login required for Tethys Portal when ``True``. Defaults to ``False``. Controllers in apps need to use the ``controller`` decorator from the Tethys SDK, rather than Django's ``login_required`` decorator.
ENABLE_RESTRICTED_APP_ACCESS                       app access can be restricted based on user object permissions when ``True``. Defaults to ``False``. A list can also be provided to restrict specific applications. If ``ENABLE_OPEN_PORTAL`` is set to ``True`` this setting has no effect. That is, users will have unrestricted access to apps independently of the value of this setting.
TETHYS_WORKSPACES_ROOT                             location to where app/user workspaces will be created. Defaults to :file:`<TETHYS_HOME>/workspaces`.
STATIC_ROOT                                        the Django `STATIC_ROOT <https://docs.djangoproject.com/en/4.2/ref/settings/#static-root>`_ setting. Defaults to :file:`<TETHYS_HOME>/static`.
MEDIA_URL                                          the Django `MEDIA_URL <https://docs.djangoproject.com/en/4.2/ref/settings/#media-url>`_ setting. Defaults to ``'/media/'``.
MEDIA_ROOT                                         the Django `MEDIA_ROOT <https://docs.djangoproject.com/en/4.2/ref/settings/#media-root>`_ setting. Defaults to :file:`~/.tethys/media/`.
STATICFILES_USE_NPM                                serves JavaScript dependencies through Tethys rather than using a content delivery network (CDN) when ``True``. Defaults to ``False``. When set to ``True`` then you must run ``tethys gen package_json`` to npm install the JS dependencies locally so they can be served by Tethys.
ADDITIONAL_TEMPLATE_DIRS                           a list of dot-paths to template directories. These will be prepended to Tethys's list of template directories so specific templates can be overridden.
ADDITIONAL_URLPATTERNS                             a list of dot-paths to list or tuples that define additional URL patterns to register in the portal. Additional URL patterns will precede default URL patterns so URLs will first match against user specified URL patterns.
ADDITIONAL_SETTINGS_FILES                          a list of dot-paths or file paths to Python files that will be imported into the ``settings.py`` file. Additional settings files are imported at the end of the file and thus will override any previous settings with name conflicts.
MULTIPLE_APP_MODE                                  boolean indicating if the portal should host multiple apps or be configured for a single standalone app.
STANDALONE_APP                                     configured app for when ``MULTIPLE_APP_MODE`` is set to ``False``. If ``None``, then the first configured app in the DB will be used.
================================================== ================================================================================

SESSION_CONFIG
++++++++++++++

.. important::

    These settings require the ``django-session-security`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``django-session-security`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-session-security

        # pip
        pip install django-session-security

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
SESSION_SECURITY_WARN_AFTER                        the Django Session Security `WARN_AFTER <https://django-session-security.readthedocs.io/en/latest/full.html#module-session_security.settings>`_ setting. Defaults to 840 seconds.
SESSION_SECURITY_EXPIRE_AFTER                      the Django Session Security `EXPIRE_AFTER <https://django-session-security.readthedocs.io/en/latest/full.html#module-session_security.settings>`_ setting. Defaults to 900 seconds.
================================================== ================================================================================

.. _database_settings:

DATABASES
+++++++++

See the Django `DATABASES <https://docs.djangoproject.com/en/4.2/ref/settings/#databases>`_ setting.

+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Setting     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                      |
+=============+==================================================================================================================================================================================================================================================================================================================================================================================================================================================+
| default     |                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | ENGINE   | the Django default database `ENGINE <https://docs.djangoproject.com/en/4.2/ref/settings/#engine>`_ setting. Default is ``django.db.backends.sqlite3``.                                                                                                                                                                                                                                                                                           |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | NAME     | the Django default databases `NAME <https://docs.djangoproject.com/en/4.2/ref/settings/#name>`_ setting. If using the ``sqlite3`` ``ENGINE`` (default) then the default value for name will be ``tethys_platform.sqlite`` and will be located in the ``TETHYS_HOME`` directory. If another ``ENGINE`` is used then the default value is ``tethys_platform``.                                                                                     |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | USER     | the Django default database `USER <https://docs.djangoproject.com/en/4.2/ref/settings/#user>`_ setting. Not used with SQLite.                                                                                                                                                                                                                                                                                                                    |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | PASSWORD | the Django default database `PASSWORD <https://docs.djangoproject.com/en/4.2/ref/settings/#password>`_ setting. Not used with SQLite.                                                                                                                                                                                                                                                                                                            |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | HOST     | the Django default database `HOST <https://docs.djangoproject.com/en/4.2/ref/settings/#host>`_ setting. Not used with SQLite.                                                                                                                                                                                                                                                                                                                    |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | PORT     | the Django default database `PORT <https://docs.djangoproject.com/en/4.2/ref/settings/#port>`_ setting. Not used with SQLite.                                                                                                                                                                                                                                                                                                                    |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  | DIR      | name of psql directory for a local PostgreSQL database (if using the ``django.db.backends.postgresql`` ``ENGINE``). This directory will be created relative to the ``TETHYS_HOME`` directory when ``tethys db create`` is executed, unless an absolute path is provided. If you are using the ``sqlite3`` ``ENGINE`` or an external database server then exclude this key or set it to `None`.                                                   |
+--+----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

LOGGING
+++++++

+----------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| Setting        | Description                                                                                                                                  |
+================+==============================================================================================================================================+
| formatters     | override all of the default logging formatters.                                                                                              |
+----------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| handlers       | override all of the default logging handlers.                                                                                                |
+----------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| loggers        |                                                                                                                                              |
+--+-------------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  | django      |define specific loggers or change the following default loggers:                                                                              |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | handlers | override the default handlers for the ``django`` logger. Defaults to ``['console_simple']``.                                                 |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | level    | override the default level for the ``django`` logger. Defaults to ``'WARNING'`` unless the ``DJANGO_LOG_LEVEL`` environment variable is set. |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  | tethys      |define specific loggers or change the following default loggers:                                                                              |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | handlers | override the default handlers for the ``tethys`` logger. Defaults to ``['console_verbose']``.                                                |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | level    | override the default level for the ``tethys`` logger. Defaults to ``'INFO'``.                                                                |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  | tethysapp   |define specific loggers or change the following default loggers:                                                                              |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | handlers | override the default handlers for the ``tethysapp`` logger. Defaults to ``['console_verbose']``.                                             |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+
|  |  | level    | override the default level for the ``tethysapp`` logger. Defaults to ``'INFO'``.                                                             |
+--+--+----------+----------------------------------------------------------------------------------------------------------------------------------------------+

CAPTCHA_CONFIG
++++++++++++++

.. important::

    The Captcha feature requires either the ``django-simple-captcha`` library or the ``django-recaptcha2`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install one of these libraries using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-simple-captcha
        # Or
        conda install -c conda-forge django-recaptcha2

        # pip
        pip install django-simple-captcha
        # Or
        pip install django-recaptcha2

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
ENABLE_CAPTCHA                                     Boolean specifying if captcha should be enabled on the login screen. If using Google ReCaptcha then the following two settings are required. Default is ``False``
RECAPTCHA_PRIVATE_KEY                              Private key for Google ReCaptcha. Required to enable ReCaptcha on the login screen. See `Django Recaptcha 2 Installation <https://github.com/kbytesys/django-recaptcha2#how-to-install>`_.
RECAPTCHA_PUBLIC_KEY                               Public key for Google ReCaptcha. Required to enable ReCaptcha on the login screen. See `Django Recaptcha 2 Installation <https://github.com/kbytesys/django-recaptcha2#how-to-install>`_.
RECAPTCHA_PROXY_HOST                               Proxy host for Google ReCaptcha. Optional. See `Django Recaptcha 2 Installation <https://github.com/kbytesys/django-recaptcha2#how-to-install>`_.
================================================== ================================================================================

OAUTH_CONFIG
++++++++++++

.. important::

    These settings require the ``social-auth-app-django`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``social-auth-app-django`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge social-auth-app-django

        # pip
        pip install social-auth-app-django
    
    If using the OneLogin OIDC provider, you will also need to install the ``python-jose`` library:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge python-jose

        # pip
        pip install python-jose

    If using the HydroShare provider, you will also need the ``hs_restclient`` library:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge hs_restclient

        # pip
        pip install hs_restclient

====================================================== ================================================================================
Setting                                                Description
====================================================== ================================================================================
SSO_TENANT_REGEX                                       A regular expression defining the characters allowed in the Tenant field on the /accounts/tenant/ page. This page is only needed when using Multi-Tenant SSO features. Defaults to "^[\w\s_-]+$".
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY                         Key for authenticating with Azure Active Directory using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET                      Secret for authenticating with Azure Active Directory using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_MULTI_TENANT         Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_auth_azuread_multi` Setup.
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY                  Key for authenticating with Azure Active Directory against a single Tenant/Active Directory using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET               Secret for authenticating with Azure Active Directory against a single Tenant/Active Directory using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID            The ID of the Tenant/Active Directory to authenticate against. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_MULTI_TENANT            Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_auth_azuread_multi` Setup.
SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_KEY                     Key for authenticating with Azure Active Directory B2C using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_SECRET                  Secret for authenticating with Azure Active Directory B2C using their OAuth2 service. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_TENANT_ID               The ID of the Tenant/Active Directory to authenticate against in Azure Active Directory B2C. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_POLICY                  The user flow policy to use. Use `'b2c_'` unless you have created a custom user flow that you would like to use. See :ref:`social_auth_azuread` SSO Setup.
SOCIAL_AUTH_ADFS_OIDC_MULTI_TENANT                     Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_adfs_multi` Setup.
SOCIAL_AUTH_ADFS_OIDC_KEY                              Client ID for authenticating with an AD FS services using its Open ID Connect interface. See :ref:`social_adfs` SSO Setup.
SOCIAL_AUTH_ADFS_OIDC_SECRET                           Secret for authenticating with an AD FS service using its Open ID Connect interface. See :ref:`social_adfs` SSO Setup.
SOCIAL_AUTH_ADFS_OIDC_DOMAIN                           Domain of the AD FS server. See :ref:`social_adfs` SSO Setup.
SOCIAL_AUTH_FACEBOOK_KEY                               Key for authenticating with Facebook using their OAuth2 service. See :ref:`social_auth_facebook` SSO Setup.
SOCIAL_AUTH_FACEBOOK_SECRET                            Secret for authenticating with Facebook using their OAuth2 service. See :ref:`social_auth_facebook` SSO Setup.
SOCIAL_AUTH_FACEBOOK_SCOPE                             List of scopes for authenticating with Facebook using their OAuth2 service. See :ref:`social_auth_facebook` SSO Setup.
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY                          Key for authenticating with Google using their OAuth2 service. See :ref:`social_auth_google` SSO Setup.
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET                       Secret for authenticating with Google using their OAuth2 service. See :ref:`social_auth_google` SSO Setup.
SOCIAL_AUTH_HYDROSHARE_KEY                             Key for authenticating with HydroShare using their OAuth2 service. See :ref:`social_auth_hydroshare` SSO Setup.
SOCIAL_AUTH_HYDROSHARE_SECRET                          Secret for authentication with HydroShare using their OAuth2 service. See :ref:`social_auth_hydroshare` SSO Setup.
SOCIAL_AUTH_ARCGIS_KEY                                 Key for authenticating with ArcGIS Online using their OAuth2 service. See :ref:`social_auth_arcgis` SSO Setup.
SOCIAL_AUTH_ARCGIS_SECRET                              Secret for authentication with ArcGIS Online using their OAuth2 service. See :ref:`social_auth_arcgis` SSO Setup.
SOCIAL_AUTH_ARCGIS_PORTAL_KEY                          Key for authenticating with an ArcGIS Enterprise Portal using their OAuth2 service. See :ref:`social_auth_arcgis` SSO Setup.
SOCIAL_AUTH_ARCGIS_PORTAL_SECRET                       Secret for authentication with an ArcGIS Enterprise Portal using their OAuth2 service. See :ref:`social_auth_arcgis` SSO Setup.
SOCIAL_AUTH_ARCGIS_PORTAL_URL                          Root URL of the ArcGIS Enterprise Portal that will provide their OAuth2 service. See :ref:`social_auth_arcgis` SSO Setup.
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY                        Key for authenticating with LinkedIn using their OAuth2 service. See :ref:`social_auth_linkedin` SSO Setup.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET                     Secret for authenticating with LinkedIn using their OAuth2 service. See :ref:`social_auth_linkedin` SSO Setup.
SOCIAL_AUTH_OKTA_OAUTH2_MULTI_TENANT                   Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_auth_okta_multi` Setup.
SOCIAL_AUTH_OKTA_OAUTH2_KEY                            Client ID for authenticating with Okta using their OAuth 2 interface. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_OKTA_OAUTH2_SECRET                         Secret for authenticating with Okta using their OAuth 2 interface. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_OKTA_OAUTH2_API_URL                        Your Okta Organization URL. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_OKTA_OPENIDCONNECT_MULTI_TENANT            Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_auth_okta_multi` Setup.
SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY                     Client ID for authenticating with Okta using their Open ID Connect interface. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET                  Secret for authenticating with Okta using their Open ID Connect interface. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL                 Your Okta Organization URL. See :ref:`social_auth_okta` SSO Setup.
SOCIAL_AUTH_ONELOGIN_OIDC_MULTI_TENANT                 Define one or more sets of settings for multiple tenants, each indexed by a Tenant Key. See: :ref:`social_auth_onelogin_multi` Setup.
SOCIAL_AUTH_ONELOGIN_OIDC_KEY                          Client ID for authenticating with OneLogin using their Open ID Connect interface. See :ref:`social_auth_onelogin` SSO Setup.
SOCIAL_AUTH_ONELOGIN_OIDC_SECRET                       Secret for authenticating with OneLogin using their Open ID Connect interface. See :ref:`social_auth_onelogin` SSO Setup.
SOCIAL_AUTH_ONELOGIN_OIDC_SUBDOMAIN                    Your OneLogin Subdomain. See :ref:`social_auth_onelogin` SSO Setup.
SOCIAL_AUTH_ONELOGIN_OIDC_TOKEN_ENDPOINT_AUTH_METHOD   The authentication method to use when requesting tokens from the token endpoint. See :ref:`social_auth_onelogin` SSO Setup.
====================================================== ================================================================================

.. _oauth2_provider_settings:

OAUTH2_PROVIDER
+++++++++++++++

.. important::

    The OAuth2 Provider feature requires the ``django-oauth-toolkit`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install one of these libraries using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-oauth-toolkit

        # pip
        pip install django-oauth-toolkit

.. note::

    The ``OAUTH2_PROVIDER`` heading can be listed under the ``OAUTH_CONFIG`` heading or it can be it's own heading.

====================================================== ================================================================================
Setting                                                Description
====================================================== ================================================================================
URL_NAMESPACE                                          The URL prefix to use to register the ``oauth2_provider`` urls. Default is ``o`` which produces URL endpoints like `<http://127.0.0.1:8000/o/applications/register/>`_.
====================================================== ================================================================================

For additional ``OAUTH2_PROVIDER`` refer to the `Django OAuth Toolkit documentation <https://django-oauth-toolkit.readthedocs.io/en/stable/settings.html>`_.


MFA_CONFIG
++++++++++

.. important::

    These settings require the ``django-mfa2``, ``arrow``, and ``isodate`` libraries to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install these libraries using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-mfa2 arrow isodate

        # pip
        pip install django-mfa2 arrow isodate

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
ADMIN_MFA_REQUIRED                                 Are admin (staff) users required to set up MFA when MFA_REQUIRED is ``True``. Defaults to ``True``.
SSO_MFA_REQUIRED                                   Are users logged in with SSO required to set up MFA when MFA_REQUIRED is ``True``. Defaults to ``False``.
MFA_RECHECK                                        Allow random rechecking of the user. Defaults to False.
MFA_RECHECK_MIN                                    Minimum recheck interval in seconds. Defaults to 600 seconds (10 minutes).
MFA_RECHECK_MAX                                    Maximum recheck interval in seconds. Defaults to 1800 seconds (30 minutes).
MFA_QUICKLOGIN                                     Allow quick login for returning users by provide only their 2FA. Defaults to False.
TOKEN_ISSUER_NAME                                  TOTP Issuer name to display in the app. Defaults to ``Tethys Portal``.
MFA_UNALLOWED_METHODS                              A list of MFA methods to be disallowed. Valid methods are include ``U2F``, ``FIDO2``, ``Email``, ``Trusted_Devices``, and ``TOTP``. All but ``TOPT`` are disabled by default.
================================================== ================================================================================

ANALYTICS_CONFIG
++++++++++++++++

The Django Analytical configuration settings for enabling analytics services on the Tethys Portal (see: `Enabling Services - Django Analytical <https://django-analytical.readthedocs.io/en/latest/install.html#enabling-the-services>`_. The following is a list of settings for some of the supported services that can be enabled.


.. important::

    These settings require the ``django-analytical`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``django-analytical`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-analytical

        # pip
        pip install django-analytical

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
CLICKY_SITE_ID
CRAZY_EGG_ACCOUNT_NUMBER
GAUGES_SITE_ID
GOOGLE_ANALYTICS_JS_PROPERTY_ID
GOSQUARED_SITE_TOKEN
HOTJAR_SITE_ID
HUBSPOT_PORTAL_ID
INTERCOM_APP_ID
KISSINSIGHTS_ACCOUNT_NUMBER
KISSINSIGHTS_SITE_CODE
KISS_METRICS_API_KEY
MIXPANEL_API_TOKEN
OLARK_SITE_ID
OPTIMIZELY_ACCOUNT_NUMBER
PERFORMABLE_API_KEY
PIWIK_DOMAIN_PATH
PIWIK_SITE_ID
RATING_MAILRU_COUNTER_ID
SNAPENGAGE_WIDGET_ID
SPRING_METRICS_TRACKING_ID
USERVOICE_WIDGET_KEY
WOOPRA_DOMAIN
YANDEX_METRICA_COUNTER_ID
================================================== ================================================================================

EMAIL_CONFIG
++++++++++++

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
EMAIL_HOST                                         the Django `EMAIL_HOST <https://docs.djangoproject.com/en/4.2/ref/settings/#email-host>`_ setting.
EMAIL_PORT                                         the Django `EMAIL_PORT <https://docs.djangoproject.com/en/4.2/ref/settings/#email-port>`_ setting.
EMAIL_HOST_USER                                    the Django `EMAIL_HOST_USER <https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-user>`_ setting.
EMAIL_HOST_PASSWORD                                the Django `EMAIL_HOST_PASSWORD <https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-password>`_ setting.
EMAIL_USE_TLS                                      the Django `EMAIL_USE_TLS <https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-tls>`_ setting.
DEFAULT_FROM_EMAIL                                 the Django `DEFAULT_FROM_EMAIL <https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email>`_ setting.
EMAIL_FROM                                         the email alias setting (e.g.: 'John Smith').
================================================== ================================================================================

LOCKOUT_CONFIG
++++++++++++++

The Django Axes configuration settings for enabling lockout capabilities on Tethys Portal (see: :ref:`advanced_config_lockout`). The following is a list of the Django Axes settings that are configured for the default lockout capabilities in Tethys Portal. For a full list of Django Axes settings, see: `Django Axes Configuration Documentation <https://django-axes.readthedocs.io/en/latest/4_configuration.html>`_.

.. important::

    These settings require the ``django-axes`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``django-axes`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-axes

        # pip
        pip install django-axes

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
AXES_FAILURE_LIMIT                                 Number of failed login attempts to allow before locking. Default ``3``.
AXES_COOLOFF_TIME                                  Time to elapse before locked user is allowed to attempt logging in again. In the :file:`portal_config.yml` this setting accepts only integers or `ISO 8601 time duration formatted strings <https://en.wikipedia.org/wiki/ISO_8601#Durations>`_ (e.g.: ``"PT30M"``). Default is 30 minutes.
AXES_LOCKOUT_PARAMETERS                            A list of parameters that Axes uses to lock out users. See `Django Axes - Customizing lockout parameters <https://django-axes.readthedocs.io/en/latest/5_customization.html#customizing-lockout-parameters>`_ for more details. Defaults to ``['username']``.
AXES_ENABLE_ADMIN                                  Enable the Django Axes admin interface. Defaults to ``True``.
AXES_VERBOSE                                       More logging for Axes when True. Defaults to ``True``.
AXES_RESET_ON_SUCCESS                              Successful login (after the cooloff time has passed) will reset the number of failed logins when True. Defaults to ``True``.
AXES_LOCKOUT_TEMPLATE                              Template to render when user is locked out. Defaults to ``'tethys_portal/accounts/lockout.html'``
AXES_LOGGER                                        The logger for Django Axes to use. Defaults to ``'tethys.watch_login'``.
================================================== ================================================================================

CORS_CONFIG
+++++++++++

These CORS settings are used to configure Cross-Origin Resource Sharing (CORS) for the Tethys Portal. See: `Django CORS Headers <https://pypi.org/project/django-cors-headers>`_ for more information for the complete list of availalbe settings.

.. important::

    These settings require the ``django-cors-headers`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``django-cors-headers`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-cors-headers

        # pip
        pip install django-cors-headers

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
CORS_ALLOWED_ORIGINS                               A list of origins that are authorized to make cross-site HTTP requests. Defaults to ``[]``.
CORS_ALLOWED_ORIGIN_REGEXES                        A list of strings representing regexes that match Origins that are authorized to make cross-site HTTP requests. Defaults to ``[]``.
CORS_ALLOW_ALL_ORIGINS                             If ``True``, all origins will be allowed. Other settings restricting allowed origins will be ignored. Defaults to ``False``.
CORS_ALLOW_METHODS                                 A list of HTTP verbs that are allowed for cross-site requests. Defaults to ``("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT")``.
CORS_ALLOW_HEADERS                                 The list of non-standard HTTP headers that you permit in requests from the browser. Sets the Access-Control-Allow-Headers header in responses to preflight requests. Defaults to ``("accept", "authorization", "content-type", "user-agent", "x-csrftoken", "x-requested-with")``.
================================================== ================================================================================

Gravatar Settings
+++++++++++++++++

The Gravatar settings are used to configure the Gravatar service user profile pictures for the Tethys Portal. See: `Django Gravatar 2 <https://pypi.org/project/django-gravatar2>`_ for more information.

.. important::

    These settings require the ``django-gravatar2`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``django-gravatar2`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge django-gravatar2

        # pip
        pip install django-gravatar2

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
GRAVATAR_URL                                       the Gravatar service endpoint. Defaults to ``"http://www.gravatar.com/"``.
GRAVATAR_SECURE_URL                                the secure Gravatar service endpoint. Defaults to ``"https://secure.gravatar.com/"``.
GRAVATAR_DEFAULT_SIZE                              the default size in pixels of the Gravatar image. Defaults to ``"80"``.
GRAVATAR_DEFAULT_IMAGE                             the default Gravatar image. Defaults to ``"retro"``.
GRAVATAR_DEFAULT_RATING                            the default allowable image rating. Defaults to ``"g"``.
GRAVATAR_DEFAULT_SECURE                            uses Gravatar secure endpoint when ``True``. Defaults to ``True``.
================================================== ================================================================================

Other Settings
++++++++++++++

================================================== ================================================================================
Setting                                            Description
================================================== ================================================================================
CHANNEL_LAYERS                                     the Django Channels `CHANNEL_LAYERS <https://channels.readthedocs.io/en/latest/topics/channel_layers.html#channel-layers>`_ setting.
AUTH_PASSWORD_VALIDATORS                           the Django `AUTH_PASSWORD_VALIDATORS <https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#module-django.contrib.auth.password_validation>`_ setting.
GUARDIAN_RAISE_403                                 the Django Guardian `GUARDIAN_RAISE_403 <https://django-guardian.readthedocs.io/en/stable/configuration.html#guardian-raise-403>`_ setting.
GUARDIAN_RENDER_403                                the Django Guardian `GUARDIAN_RENDER_403 <https://django-guardian.readthedocs.io/en/stable/configuration.html#guardian-render-403>`_ setting.
GUARDIAN_TEMPLATE_403                              the Django Guardian `GUARDIAN_TEMPLATE_403 <https://django-guardian.readthedocs.io/en/stable/configuration.html#guardian-template-403>`_ setting.
ANONYMOUS_USER_NAME                                the Django Guardian `ANONYMOUS_USER_NAME <https://django-guardian.readthedocs.io/en/stable/configuration.html#anonymous-user-name>`_ setting.
================================================== ================================================================================

.. note::

    All of the settings groupings that end in ``_CONFIG`` are merely for convenience and organization, but are not necessary. Thus the following two examples are effectively the same:

    .. code-block:: yaml

        settings:
          TETHYS_PORTAL_CONFIG:
            BYPASS_TETHYS_HOME_PAGE: False

    .. code-block:: yaml

        settings:
          BYPASS_TETHYS_HOME_PAGE: False


.. note::

    You may define any Django Setting as a key under the ``settings`` key. Only the most common Django settings are listed above. For a complete reference of Django settings see: `Django Settings Reference <https://docs.djangoproject.com/en/2.2/ref/settings/>`_.


.. tip::

  Settings from this section are read everytime the Portal starts up. If changes are made you will need to restart the portal for the settings to be applied.


.. _tethys_configuration_site_settings:

Site Settings
=============

The **site_settings** Portal Yaml Key is used to specify settings related to customization of the portal theme and content. Here is a comprehensive list of the available settings:

.. note::

  **New in Tethys 4.0**

  The ``site_settings`` key is new in Tethys 4.0. Previous versions used the ``site_content`` key. Additionally, the setting categories were introduced, and the names of several settings were changed to be consistent with the corresponding settings in the Portal Admin pages :doc:`admin_pages`.


General Settings
++++++++++++++++

The following settings can be used to modify global features of the site. Access the settings using the Site Settings > General Settings links on the admin pages or under the ``GENERAL_SETTINGS`` category in the ``site_settings`` section of the :file:`portal_config.yml` file.

============================== ============================== ============================== ================================================================================
Admin Setting                  Portal Config Yaml Key         Site Setting Command Option    Description
============================== ============================== ============================== ================================================================================
Site Title                     SITE_TITLE                     --site-title                   Title of the web page that appears in browser tabs and bookmarks of the site. Default is "Tethys Portal".
Favicon                        FAVICON                        --favicon                      Local or external path to the icon that will display in the browser tab. We recommend storing the favicon in the static directory of tethys_portal. Default is "tethys_portal/images/default_favicon.png".
Brand Text                     BRAND_TEXT                     --brand-text                   Title that appears in the header of the portal. Default is "Tethys Portal".
Brand Image                    BRAND_IMAGE                    --brand-image                  Local or external path to the portal logo. We recommend storing the logo in the static directory of tethys_portal. Default is "tethys_portal/images/tethys-logo-75.png".
Brand Image Height             BRAND_IMAGE_HEIGHT             --brand-image-height           The height of the brand image.
Brand Image Width              BRAND_IMAGE_WIDTH              --brand-image-width            The width of the brand image.
Brand Image Padding            BRAND_IMAGE_PADDING            --brand-image-padding          The padding for the brand image.
Apps Library Title             APPS_LIBRARY_TITLE             --apps-library-title           Title of the page that displays app icons. Default is "Apps".
Primary Color                  PRIMARY_COLOR                  --primary-color                The primary color for the portal theme. Default is #0a62a9.
Secondary Color                SECONDARY_COLOR                --secondary-color              The secondary color for the portal theme. Default is #7ec1f7.
Primary Text Color             PRIMARY_TEXT_COLOR             --primary-text-color           Color of the text appearing in the headers and footer.
Primary Text Hover Color       PRIMARY_TEXT_HOVER_COLOR       --primary-text-hover-color     Hover color of the text appearing in the headers and footer (where applicable).
Secondary Text Color           SECONDARY_TEXT_COLOR           --secondary-text-color         Color of secondary text on the home page.
Secondary Text Hover Color     SECONDARY_TEXT_HOVER_COLOR     --secondary-text-hover-color   Hover color of the secondary text on the home page.
Background Color               BACKGROUND_COLOR               --background-color             Color of the background on the apps library page and other pages.
Copyright                      COPYRIGHT                      --copyright                    Copyright text that appears in the footer of the portal. Default is "Copyright © 2022 Your Organization".
Home Page Template             HOME_PAGE_TEMPLATE             --home-page-template           Path to alternate Home page template (will replace Home page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Apps Library Template          APPS_LIBRARY_TEMPLATE          --apps-library-template        Path to alternate Apps Library page template (will replace Apps Library page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Login Page Template            LOGIN_PAGE_TEMPLATE            --login-page-template          Path to alternate portal login page template (will replace login page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Register Page Template         REGISTER_PAGE_TEMPLATE         --register-page-template       Path to alternate portal registration (or signup) page template (will replace signup page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
User Page Template             USER_PAGE_TEMPLATE             --user-page-template           Path to alternate user profile page template (will replace user page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
User Settings Page Template    USER_SETTINGS_PAGE_TEMPLATE    --user-settings-page-template  Path to alternate user settings (i.e. edit) page template (will replace settings page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
============================== ============================== ============================== ================================================================================

Home Page
+++++++++

The following settings can be used to modify the content on the home page. Access the settings using the Site Settings > Home Page links on the admin pages or under the ``HOME_PAGE`` category in the ``site_settings`` section of the :file:`portal_config.yml` file.

============================== ============================== ============================== ================================================================================
Admin Setting                  Portal Config Yaml Key         Site Setting Command Option    Description
============================== ============================== ============================== ================================================================================
Hero Text                      HERO_TEXT                      --hero-text                    Text that appears in the hero banner at the top of the home page. Default is "Welcome to Tethys Portal,\nthe hub for your apps.".
Blurb Text                     BLURB_TEXT                     --blurb-text                   Text that appears in the blurb banner, which follows the hero banner. Default is "Tethys Portal is designed to be customizable, so that you can host apps for your\norganization. You can change everything on this page from the Home Page settings.".
Feature 1 Heading              FEATURE_1_HEADING              --feature-1-heading            Heading for 1st feature highlight (out of 3).
Feature 1 Body                 FEATURE_1_BODY                 --feature-1-body               Body text for the 1st feature highlight.
Feature 1 Image                FEATURE_1_IMAGE                --feature-1-image              Path or url to image for the 1st feature highlight.
Feature 2 Heading              FEATURE_2_HEADING              --feature-2-heading            Heading for 2nd feature highlight (out of 3).
Feature 2 Body                 FEATURE_2_BODY                 --feature-2-body               Body text for the 2nd feature highlight.
Feature 2 Image                FEATURE_2_IMAGE                --feature-2-image              Path or url to image for the 2nd feature highlight.
Feature 3 Heading              FEATURE_3_HEADING              --feature-3-heading            Heading for 3rd feature highlight (out of 3).
Feature 3 Body                 FEATURE_3_BODY                 --feature-3-body               Body text for the 3rd feature highlight.
Feature 3 Image                FEATURE_3_IMAGE                --feature-3-image              Path or url to image for the 3rd feature highlight.
Call To Action                 CALL_TO_ACTION                 --call-to-action               Text that appears in the call to action banner at the bottom of the page (only visible when user is not logged in). Default is "Ready to get started?".
Call To Action Button          CALL_TO_ACTION_BUTTON          --call-to-action-button        Text that appears on the call to action button in the call to action banner (only visible when user is not logged in). Default is "Start Using Tethys!".
============================== ============================== ============================== ================================================================================

For more advanced customization, you may use the Custom Styles and Custom Template options to completely replace the Home Page or Apps Library page CSS and HTML.

Custom Styles
+++++++++++++

The following settings can be used to add additional CSS to the Home page, Apps Library page, and portal-wide. Access the settings using the Site Settings > Custom Styles links on the admin pages or under the ``CUSTOM_STYLES`` category in the ``site_settings`` section of the :file:`portal_config.yml` file.

============================== ============================== ============================== ================================================================================
Admin Setting                  Portal Config Yaml Key         Site Setting Command Option    Description
============================== ============================== ============================== ================================================================================
Portal Base Css                PORTAL_BASE_CSS                --portal-base-css              CSS code to modify the Tethys Portal Base Page, which extends most of the portal pages (i.e. Home, Login, Developer, Admin, etc.). Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
Home Page Css                  HOME_PAGE_CSS                  --home-page-css                CSS code to modify the Tethys Portal Home Page. Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
Apps Library Css               APPS_LIBRARY_CSS               --apps-library-css             CSS code to modify the Tethys Portal Apps Library. Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
Accounts Base Css              ACCOUNTS_BASE_CSS              --accounts-base-css            CSS code to modify the base template for all of the accounts pages (e.g. login, register, change password, etc.). Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
Login Css                      LOGIN_CSS                      --login-css                    CSS code to modify the Portal Login page. Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
Register Css                   REGISTER_CSS                   --register-css                 CSS code to modify the Portal Registration page. Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
User Base Css                  USER_BASE_CSS                  --user-base-css                CSS code to modify the base template for all of the user profile pages (e.g. user, settings, manage storage). Takes or straight CSS code or a file path available through Tethys static files, such as in a Tethys app, Tethys extension, or Django app.
============================== ============================== ============================== ================================================================================

Custom Templates
++++++++++++++++

The following settings can be used to override the templates for the Home page and Apps Library page. Access the settings using the Site Settings > Custom Templates links on the admin pages or under the ``CUSTOM_TEMPLATES`` category in the ``site_settings`` section of the :file:`portal_config.yml` file..

============================== ============================== ============================== ================================================================================
Admin Setting                  Portal Config Yaml Key         Site Setting Command Option    Description
============================== ============================== ============================== ================================================================================
Home Page Template             HOME_PAGE_TEMPLATE             --home-page-template           Path to alternate Home page template (will replace Home page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Apps Library Template          APPS_LIBRARY_TEMPLATE          --apps-library-template        Path to alternate Apps Library page template (will replace Apps Library page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Login Page Template            LOGIN_PAGE_TEMPLATE            --login-page-template          Path to alternate portal login page template (will replace login page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
Register Page Template         REGISTER_PAGE_TEMPLATE         --register-page-template       Path to alternate portal registration (or signup) page template (will replace signup page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
User Page Template             USER_PAGE_TEMPLATE             --user-page-template           Path to alternate user profile page template (will replace user page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
User Settings Page Template    USER_SETTINGS_PAGE_TEMPLATE    --user-settings-page-template  Path to alternate user settings (i.e. edit) page template (will replace settings page template entirely). The template must be located within a valid templates directory, such as in a Tethys app, Tethys extension, or Django app.
============================== ============================== ============================== ================================================================================


.. tip::

  Settings from this section are read when running the "tethys site -f" command. Note that the "-f" flag indicates that site settings should be applied from this file.

.. note::

  All of the site settings can also be modified through the :doc:`admin_pages`.

Example Portal Config File
--------------------------

.. literalinclude:: ../installation/resources/example-portal-config.yml
   :language: yaml