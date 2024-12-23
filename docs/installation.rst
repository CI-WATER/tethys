.. _development_installation:

***************
Getting Started
***************

**Last Updated:** September 2024

This section describes how to get Tethys Platform up and running as a fresh installation for app development.

.. note::
    
    For the simplest and most streamlined instructions, see :ref:`quickstart`.
    
    For upgrading an existing installation, see :ref:`update_tethys`. 
    
    For deploying a production instance of Tethys Portal, see :ref:`production_installation`.
    
    To contribute to the Tethys Platform source code itself, see :ref:`setup_dev_environment`.

Prerequisites
-------------

Tethys Platform requires the `conda packaging system <https://docs.conda.io/en/latest/index.html>`_. If you do not already have an installation of ``Miniconda`` (or ``Anaconda``) then refer to their `documentation <https://docs.conda.io/en/latest/miniconda.html>`_ for installation instructions.

Also, be sure that the system you are using meets the minimum :ref:`system_reqs`.


1. Install the ``tethys-platform`` Conda Package
------------------------------------------------

a. To install ``tethys-platform`` into a new conda environment then run the following commands:

.. code-block:: bash

    conda create -n tethys -c conda-forge tethys-platform django=<DJANGO_VESION>

.. important::

    **Django Version**

    As of Tethys 4.3 and above, the version of Django is no longer pinned in the ``tethys-platform`` package. You will need to specify the version of Django that you want to use when creating the environment. This is especially important for production installations, as only the LTS versions of Django recieve bug and security fixes. For development installations, we recommend using the same version of Django that you plan to use in production. For production installations, we recommend using the current LTS version of Django (see: `How to get Django - Supported Versions <https://www.djangoproject.com/download/>`_. Failing to provide the Django version will result in installing the latest version of Django which may not be the LTS version.

.. tip::

    **Installation Speedup**

    If conda is taking too long to solve the Tethys environment, try using the ``libmamba`` solver: :ref:`libmamba_solver`.

    **Install Micro-Tethys**

    The ``micro-tethys-platform`` conda package is a minimal version of ``tethys-platform``. It has the exact same code base, but doesn't include any of the optional dependencies. As a result the environment is much smaller, but none of the optional features will be enabled. Any of the optional features can be enabled simply by installing the dependencies required by those features (see :ref:`optional_features`).

        .. code-block:: bash

            conda create -n tethys -c tethysplatform -c conda-forge micro-tethys-platform

    **Install Development Build**

    To install the latest development build of ``tethys-platform`` add the ``tethysplatform/label/dev`` channel to the list of conda channels:

        .. code-block:: bash

            conda create -n tethys -c tethysplatform/label/dev -c conda-forge tethys-platform

    Alternatively, to install from source refer to the :ref:`setup_dev_environment` docs.


2. Activate the Tethys Conda Environment
----------------------------------------

Anytime you want to work with Tethys Platform, you'll need to activate the ``tethys`` Conda environment. You will know the ``tethys`` environment is active when ``(tethys)`` is displayed to the left of the terminal prompt. Activate the ``tethys`` environment now as follows:

.. code-block:: bash

    conda activate tethys

3. Create a :file:`portal_config.yml` File
------------------------------------------

To add custom configurations such as the database and other local settings you will need to generate a :file:`portal_config.yml` file. To generate a new template :file:`portal_config.yml` run:

.. code-block:: bash

    tethys gen portal_config

You can customize your settings in the :file:`portal_config.yml` file after you generate it by manually editing the file or by using the :ref:`tethys_settings_cmd` command. Refer to the :ref:`tethys_configuration` documentation for more information.


4. Configure the Tethys Database
--------------------------------

There are several options for setting up a DB server: local, docker, or remote. Tethys Platform uses a local SQLite database by default. For development environments you can use Tethys to create a local server:

.. code-block:: bash

    tethys db configure

.. note::

    The tethys db command (:ref:`tethys_db_cmd`) will create a local database file in the location specified by the ``NAME`` setting in the ``DATABASES`` section of the :file:`portal_config.yml` file (by default ``tethys_platform.sqlite``). If the value of ``NAME`` is a relative path then the database file will be created relative to directory specified by the ``TETHYS_HOME`` environment variable. By default ``TETHYS_HOME`` is at `~/.tethys`.

For additional options for configuring a database see :ref:`database_configuration`

5. Start the Development Server
-------------------------------

Once you have a database successfully configured you can run the Tethys development server:

.. code-block:: bash

    tethys manage start

This will start up a locally running web server. You can access the Tethys Portal by going to `<http://localhost:8000>`_ in your browser.

.. tip::

    You can customize the port that the server is running on by adding the ``-p`` option.

    .. code-block:: bash

        tethys manage start -p 8001

    See :ref:`tethys_manage_cmd` for more details.

6. Next Steps
-------------

There are several directions that you may want to go from here.

* Install an app you have already developed using the :ref:`app_installation` guide.
* Complete one or more :ref:`tutorials` to learn how to develop apps using Tethys Platform.
* Install one or both of the :ref:`installation_showcase_apps` to see live demos and code examples of Gizmos and Layouts.
* Checkout the :doc:`./installation/web_admin_setup` docs to customize your Tethys Portal.
* For help getting started with docker see :ref:`using_docker`


Related Docs
------------

.. toctree::
    :maxdepth: 1

    installation/system_requirements
    tethys_portal/configuration
    installation/database_configuration
    installation/conda
    installation/application
    installation/showcase_apps
    installation/update
    installation/production
    contribute/dev_environment
    installation/using_docker
    installation/web_admin_setup