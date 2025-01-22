.. _production_configuration:

************************
Production Configuration
************************

**Last Updated:** October 2024

There is a lot of configuration to be done when setting up a production installation of Tethys Portal. Each part of the configuration has been divided into the following guides. We recommend you go through them in order when doing an installation, but they are split out for simpler lookup and reference.

Basic Configuration
-------------------

These guides describe the minimum amount of configuration that needs to be performed for every production installation of Tethys Portal.

.. toctree::
    :maxdepth: 1

    configuration/basic/portal_config
    configuration/basic/database
    configuration/basic/static_and_workspaces
    configuration/basic/nginx
    configuration/basic/apache
    configuration/basic/supervisor
    configuration/basic/file_permissions
    configuration/basic/firewall

Advanced Configuration
----------------------

These guides describe additional configuration that you can perform to add more capabilities to your Tethys Portal.

.. toctree::
    :maxdepth: 1

    configuration/advanced/https_config
    configuration/advanced/customize
    configuration/advanced/email_config
    configuration/advanced/lockout
    configuration/advanced/self_hosted_js_deps
    configuration/advanced/social_auth
    configuration/advanced/multi_factor_auth
    configuration/advanced/webanalytics
    configuration/advanced/django_channels_layer
