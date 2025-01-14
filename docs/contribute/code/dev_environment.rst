.. _setup_dev_environment:

**********************************
Setting Up Development Environment
**********************************

**Last Updated:** January 2025

The first step in contributing code to Tethys Platform is setting up a development environment. This guide will walk you through the process of setting up a development environment for Tethys Platform.

.. _dev_setup_manual:

Manual Setup
============

The manual setup process involves cloning a copy of the Tethys Platform source code from GitHub, creating a new conda environment, and installing the Tethys Platform and its dependencies.

0. Install Prerequisites
------------------------

    For a minimal dev installation, you will need the following software installed on your system:

      * `Miniconda <https://docs.anaconda.com/miniconda/install/>`_ - Python package manager
      * `libmamba Solver for Conda <https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community>`_ - A faster Conda package solver
      * `Git <https://git-scm.com/downloads>`_ - Version control system

    Other software that may be required for working on specific parts of the platform:

      * `Docker <https://docs.docker.com/get-docker/>`_ - for running PostGIS, GeoServer, THREDDS
      * `PostgreSQL with PostGIS <https://postgis.net/install/>`_ - if not installing with Docker
      * `GeoServer <https://docs.geoserver.org/latest/en/user/installation/index.html>`_ - if not installing with Docker
      * `THREDDS <https://downloads.unidata.ucar.edu/tds/>`_ - if not installing with Docker
      * `pgadmin <https://www.pgadmin.org/download/>`_ - for managing PostGIS

1. Clone the Tethys Platform Repository
---------------------------------------

    .. code-block:: bash

        git clone https://github.com/tethysplatform/tethys.git

    .. note::

        If you do not have permission to push changes to the Tethys Platform repository, you should fork the repository on GitHub and clone your fork instead (see: :ref:`contribute_forking`).

2. Create a New Conda Environment
---------------------------------

    Environment with all dependencies installed, including optional dependencies:

    .. code-block:: bash
    
        cd tethys
        conda env create -n <ENV_NAME> -f environment.yml

    Environment with only the core dependencies installed (i.e. "Micro Tethys"):

    .. code-block:: bash
    
        cd tethys
        conda env create -n <ENV_NAME> -f micro_environment.yml

    .. note::

        If you need to create an environment with a specific version of Python, Django, or other dependency, temporarily modify :file:`environment.yml` file before running the command above.

3. Activate the Conda Environment
---------------------------------

    .. code-block:: bash

        conda activate <ENV_NAME>


4. Install Tethys Platform in Editable Mode
-------------------------------------------

    .. code-block:: bash

        pip install -e .

5. Generate a :file:`portal_config.yml`
---------------------------------------

    .. code-block:: bash

        tethys gen portal_config

6. Configure the Database
-------------------------

    .. code-block:: bash

        tethys db configure

7. Run the Development Server
-----------------------------

    .. code-block:: bash

        tethys start

Other Common Development Setups
===============================

.. _setup_dev_environment_postgis:

Use PostGIS Running in Docker
-----------------------------

The most common use case for this setup is to run the test suite. Another common need for using a PostGIS database is to debug features related to Persistent Stores API.

.. warning::

    **DO NOT** use these instructions for production deployments. Instead, see :ref:`production_database`.

1. Run PostGIS in Docker

    Using Tethys CLI:

    .. code-block:: bash

        tethys docker init -c postgis
        tethys docker start -c postgis

    Or using Docker CLI:

    .. code-block:: bash

        docker run  -d --name <POSTGIS_CONTAINER_NAME> -e POSTGRES_PASSWORD=mysecretpassword -p <DB_PORT>:5432 postgis/postgis

    .. warning::

        **DO NOT** use these instructions for production deployments. Instead, see :ref:`production_database`.

2. Configure Tethys to use PostGIS Docker

    Using the Tethys CLI:

    .. code-block:: bash

        tethys settings --set DATABASES.default.ENGINE django.db.backends.postgresql --set DATABASES.default.NAME tethys_platform --set DATABASES.default.USER tethys_default --set DATABASES.default.PASSWORD pass --set DATABASES.default.HOST localhost --set DATABASES.default.PORT <DB_PORT>

    Or manually edit the :file:`portal_config.yml` file:

    .. code-block:: yaml

        settings:
          DATABASES:
            default:
                ENGINE: django.db.backends.postgresql
                NAME: tethys_platform
                USER: tethys_default
                PASSWORD: pass
                HOST: localhost
                PORT: <DB_PORT>

    .. warning::

        **DO NOT** use these instructions for production deployments. Instead, see :ref:`production_database`.

3. Configure the database:

    .. code-block:: bash

        PGPASSWORD=mysecretpassword tethys db configure --username tethys_default --password pass --superuser-name tethys_super --superuser-password pass

    .. warning::

        **DO NOT** use these instructions for production deployments. Instead, see :ref:`production_database`.


.. _dev_setup_script:

Installation Script
===================

An installation script is available that automates the setup process. To use the script, follow these steps:

    For systems with `wget` (most Linux distributions):

    .. parsed-literal::

        wget :install_tethys:`sh`
        bash install_tethys.sh

    For Systems with `curl` (e.g. Mac OSX and Rocky Linux):

    .. parsed-literal::

        curl :install_tethys:`sh` -o ./install_tethys.sh
        bash install_tethys.sh


.. _install_script_options:

Install Script Options
----------------------

You can customize your tethys installation by passing command line options to the installation script. The available options can be listed by running


.. code-block:: bash

     bash install_tethys.sh --help

Each option is also descriped here:
  * `-n, --conda-env-name <NAME>`:
          Name for tethys conda environment. Default is 'tethys-dev'.
  * `-t, --tethys-home <PATH>`:
          Path for tethys home directory. Default is ~/.tethys/${CONDA_ENV_NAME}/.

          .. note::

              If ``${CONDA_ENV_NAME}`` is "tethys" then the default for ``TETHYS_HOME`` is just :file:`~/.tethys/`

  * `-s, --tethys-src <PATH>`:
          Path to the tethys source directory. Default is ${TETHYS_HOME}/tethys/.
  * `-a, --allowed-hosts <HOST>`:
          Hostname or IP address on which to serve Tethys. Default is 127.0.0.1.
  * `-p, --port <PORT>`:
          Port on which to serve Tethys. Default is 8000.
  * `-b, --branch <BRANCH_NAME>`:
          Branch to checkout from version control. Default is 'main'.
  * `-c, --conda-home <PATH>`:
          Path to conda home directory where Miniconda will be installed, or to an existing installation of Miniconda. Default is ~/miniconda/.

          .. tip::

              The conda home path cannot contain spaces. If the your home path contains spaces then the `--conda-home` option must be specified and point to a path without spaces.

  * `--db-username <USERNAME>`:
          Username for the normal tethys database user. Default is 'tethys_default'.

          .. note::

             The developer install script configures the database user to be the ``db-super-username`` rather than the ``db-username`` so that tests can be run.

  * `--db-password <PASSWORD>`:
          Password that the tethys database server will use. Default is 'pass'.
  * `--db-super-username <USERNAME>`:
          Username for super user on the tethys database server. Default is 'tethys_super'.
  * `--db-super-password <PASSWORD>`:
          Password for super user on the tethys database server. Default is 'pass'.
  * `--db-port <PORT>`:
          Port that the tethys database server will use. Default is 5436.
  * `--db-dir <PATH>`:
          Path where the local PostgreSQL database will be created. Default is ${TETHYS_HOME}/psql/.
  * `-S, --superuser <USERNAME>`:
          Tethys super user name. Default is 'admin'.
  * `-E, --superuser-email <EMAIL>`:
          Tethys super user email. Default is ''.
  * `-P, --superuser-pass <PASSWORD>`:
          Tethys super user password. Default is 'pass'.
  * `--skip-tethys-install`:
          Flag to skip the Tethys installation so that the Docker installation or production installation can be added to an existing Tethys installation.

          .. tip::

              If conda home is not in the default location then the `--conda-home` options must also be specified with this option.

  * `--partial-tethys-install <FLAGS>`:
          List of flags to indicate which steps of the installation to do.

          Flags:
              * `m` - Install Miniconda
              * `r` - Clone Tethys repository (the `--tethys-src` option is required if you omit this flag).
              * `c` - Checkout the branch specified by the option `--branch` (specifying the flag `r` will also trigger this flag)
              * `e` - Create Conda environment
              * `s` - Create :file:`portal_config.yml` file and configure settings
              * `d` - Create a local database server
              * `i` - Initialize database server with the Tethys database (specifying the flag `d` will also trigger this flag)
              * `u` - Add a Tethys Portal Super User to the user database (specifying the flag `d` will also trigger this flag)
              * `a` - Create activation/deactivation scripts for the Tethys Conda environment
              * `t` - Create the `t` alias to activate the Tethys Conda environment

          For example, if you already have Miniconda installed and you have the repository cloned and have generated a :file:`portal_config.yml` file, but you want to use the install script to:
              * create a conda environment,
              * setup a local database server,
              * create the conda activation/deactivation scripts, and
              * create the `t` shortcut

          then you can run the following command::

              bash install_tethys.sh --partial-tethys-install edat

          .. warning::

              If `--skip-tethys-install` is used then this option will be ignored.

  * `--install-docker`:
          Flag to include Docker installation as part of the install script (Linux only). See `2. Install Docker (OPTIONAL)`_ for more details.

  * `--docker-options <OPTIONS>`:
          Command line options to pass to the `tethys docker init` call if --install-docker is used. Default is "'-d'".

          .. tip::

              The value for the `--docker-options` option must have nested quotes. For example "'-d -c geoserver'" or '"-d -c geoserver"'.
  * `--production`
          Flag to install Tethys in a production configuration.
  * `--configure-selinux`
          Flag to perform configuration of SELinux for production installation. (Linux only).
  * `-x`:
          Flag to turn on shell command echoing.
  * `-h, --help`:
          Print this help information.

Example with Options
--------------------

Here is an example of calling the installation script with customized options

.. code-block:: bash

    bash install_tethys.sh -t ~/Workspace/tethys -a localhost -p 8005 -c ~/miniconda3 --db-username tethys_db_user --db-password db_user_pass --db-port 5437 -S tethys -E email@example.com -P tpass

The installation script may take several minutes to run. Once it is completed you will need to activate the new conda environment so you can start the Tethys development server. This is most easily done using an alias created by the install script. To enable the alias you need to open a new terminal or re-run the :file:`.bashrc` (Linux) or :file:`.bash_profile` (Mac) file.

For Linux:

.. code-block:: bash

    . ~/.bashrc

For Mac:

.. code-block:: bash

    . ~/.bash_profile

You can then activate the Tethys conda environment and start the Tethys development server by running:

.. code-block:: bash

    t
    tethys manage start

or simply just:

.. code-block:: bash

    t
    tms

Environment Variables and Aliases
---------------------------------

The installation script adds several environmental variables and aliases to help make using Tethys easier. Most of them are active only while the tethys conda environment is activated, however one alias to activate the tethys conda environment was added to your `.bashrc` or `bash_profile` file in your home directory and should be available from any terminal session:

- `t`: Alias to activate the tethys conda environment. It is a shortcut for the command `conda activate tethys` or more accurately `source <CONDA_HOME>/bin/activate tethys` where <CONDA_HOME> is the value of the `--conda-home` option that was passed to the install script.

Environmental Variables
+++++++++++++++++++++++

The following environmental variables are available once the tethys conda environment is activated:

- `TETHYS_HOME`:
        The directory where the Tethys source code and other Tethys resources are. It is set from the value of the `--tethys-home` option that was passed to the install script.
- `TETHYS_PORT`:
        The port that the Tethys development server will be served on. Set from the `--port` option.
- `TETHYS_DB_PORT`:
        The port that the Tethys local database server is running on. Set from the `--db-port` option.

Aliases
+++++++

The following aliases are available:

- `tms`:
        An alias to start the Tethys development server. It calls the command `tethys manage start -p <HOST>:${TETHYS_PORT}` where `<HOST>` is the value of the `--allowed-host` option that was passed to the install script and `${TETHYS_PORT}` is the value of the environmental variable which is set from the `--port` option of the install script.
- `tstart`:
        Combines the `tethys_start_db` and the `tms` commands.

Production Only
+++++++++++++++

When installing Tethys in production mode the following additional environmental variables and aliases are added:

- `NGINX_USER`:
        The name of the Nginx user.
- `NGINX_HOME`:
        The home directory of the Nginx user.
- `tethys_user_own`:
        Changes ownership of relevant files to the current user by running the command `sudo chown -R ${USER} ${TETHYS_HOME}/src ${NGINX_HOME}/tethys`.
- `tuo`:
        Another alias for `tethys_user_own`
- `tethys_server_own`:
        Reverses the effects of `tethys_user_own` by changing ownership back to the Nginx user.
- `tso`:
        Another alias for `tethys_server_own`

When you start up a new terminal there are three steps to get the Tethys development server running again:

  1. Activate the Tethys conda environment
  2. Start the Tethys database server
  3. Start the Tethys development server

Using the supplied aliases, starting the Tethys development server from a fresh terminal can be done with the following two commands:

::

    t
    tstart

2. Install Docker (OPTIONAL)
----------------------------

To facilitate leveraging the full capabilities of Tethys Platform Docker containers are provided to allow the :ref:`software_suite` to be easily installed. To use these containers you must first install Docker. The Tethys installation script :file:`install_tethys.sh` will support installing the community edition of Docker on several Linux distributions. To install Docker when installing Tethys then add the `--install-docker` option. You can also add the `--docker-options` options to pass options to the `tethys docker init` command (see the :ref:`tethys_cli_docker` documentation).

To install Docker on other systems or to install the enterprise edition of Docker please refer to the `Docker installation documentation <https://docs.docker.com/engine/installation/>`_

Use the following Tethys command to start the Docker containers.

.. code-block:: bash

    tethys docker start

You are now ready to link your Tethys Portal with the Docker containers using the web admin interface. Follow the :ref:`web_admin_setup` tutorial to finish setting up your Tethys Platform.

If you would like to test the Docker containers, see :ref:`supplementary_docker_testing`.