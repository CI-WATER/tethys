.. _contribute_code_docker:

******************
Docker Development
******************

**Last Updated**: February 2025

This document is for contributors who wish to help improve the Docker image for Tethys Platform. The Docker image is used to deploy Tethys Platform and Tethys apps in a containerized environment. The Docker image is built using a combination of a Dockerfile and Salt State scripts.

.. note::

    If you are wanting to build your own Docker image to deploy your Tethys app, please refer to the :ref:`docker_production_installation` documentation.

Dockerfile
==========

The Docker image for Tethys Platform is configured using the :file:`Dockerfile` located a the root of the Tethys Platform repository. See `Dockerfile reference | Docker Docs <https://docs.docker.com/reference/dockerfile/>`_ for an explanation of Dockerfile syntax.

Micromamba
----------

The Tethys Platform Docker image use the `mambaorg/micromamba <https://hub.docker.com/r/mambaorg/micromamba>`_ image as the base image. `Micromamba <https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html>`_ is a minimal Conda-like package manager that is both smaller and faster than a normal Conda installation. This makes it ideal for use in container images where size and speed are important.

Here are a few tips for working with Micromamba in the Docker image:

* Any lines that need the environment active, should be run after the ``ARG MAMBA_DOCKERFILE_ACTIVATE=1`` line in the Dockerfile. It is not necessary to run the ``activate`` after this line.
* Use the ``micromamba`` command in place of the ``conda`` command. For example, to install a package use ``micromamba install -y package_name``. 
* The ``micromamba`` command has many fo the same subcommands as ``conda``, but not all of them. Check the `Micromamba documentation <https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html>`_ for more information.

.. _contrib_dockerfile_build_args:

Build Args
----------

There are a few build args (``ARG``) that are used to support building the image with different configurations. The following build args are defined in the Dockerfile:

* ``PYTHON_VERSION``: The version of Python to use in the image. The default is ``3.*``.
* ``DJANGO_VERSION``: The version of Django to use in the image. The default is ``4.2.*``.
* ``MICRO_TETHYS``: A flag to indicate whether to build a minimal Tethys image. The default is ``false``.
* ``DJANGO_CHANNELS_VERSION``: The version of Django Channels to use in the image. The default is ``null``.
* ``DAPHNE_VERSION``: The version of Daphne to use in the image. The default is ``null``.

See :ref:`contrib_building_the_docker_image` for instructions on building the Docker image with build args.

Environment Variables
---------------------

There are many environment variables (``ENV``) that are used to configure the container at runtime. Many of these environment variables are used to configure the Tethys Portal settings for a specific deployment. For an explanation of the environment variables used in the Tethys Platform Docker image, see :ref:`docker_official_image`.

Don't forget to update the :file:`tethys_docker_reference.rst` file with any changes to the environment variables in the Docker image.

File Permissions
----------------

Files that are added to the image (``ADD``) should be owned by the ``www`` user and group. This is because the Tethys Platform runs as the ``www`` user and group. Use the ``--chown=www:www`` option with the ``ADD`` command to set the owner and group of the files instead of running ``chown`` in a ``RUN`` command. For example:

.. code-block:: dockerfile

    ADD --chown=www:www /path/to/source /path/to/destination

Volumes
-------

Two volumes are defined in the Dockerfile:

* ``/var/lib/tethys_persist`` or ``$TETHYS_PERSIST``: This volume is used to store persistent data for apps and the Tethys Portal. The default location for the workspaces and media directories are located in this directory. Users are encouraged to mount this location to a persistent, backed-up location to preserve data between container updates.
* ``/var/lib/tethys/keys`` or ``$TETHYS_HOME/keys``: This volume is used to store SSL keys and certificates for the Tethys Portal.

Exposed Ports
-------------

The HTML port, 80, is exposed by default in the Dockerfile because the nginx/apache server is configured to listen on port 80 by default.

Working Directory
-----------------

The working directory is set to the ``/var/lib/tethys`` or ``$TETHYS_HOME`` directory. Some of the subsequent commands run by the salt state scripts expect this to be the case.

Start up Command
----------------

The start up command is set to run the ``run.sh`` script. This script is responsible for checking if there is a database connection and then starting the salt state scripts. See :ref:`contrib_docker_supporting_files` for more information on the ``run.sh`` script.

Health Check
------------

The health check is set to run the ``liveness-probe.sh`` script. This script is responsible for checking if the Tethys Portal is running and healthy. See :ref:`contrib_docker_supporting_files` for more information on the ``liveness-probe.sh`` script.

Salt State Scripts
==================

The Tethys Platform Docker uses `Salt States <https://docs.saltproject.io/en/getstarted/fundamentals/states.html>`_, one component of `Salt Stack <https://docs.saltproject.io/en/latest/topics/index.html>`_, to perform runtime initialization of Tethys Portal and Tethys Apps. Salt States are YAML files that specify various commands to run when Tethys starts up.

The initialization steps are split across multiple Salt State scripts to allow opportunities for derivative containers to hook into different points of the initialization life cycle. For example, a salt script that performs app specific set up should be added between the :file:`tethyscore.sls` and :file:`post_app.sls` scripts. The Salt State scripts are located in the :file:`docker/salt` directory of the Tethys Platform repository and they are run by the ``run.sh`` script when the container starts up.

pre_tethys.sls
--------------

The :file:`pre_tethys.sls` script executes several preliminary tasks that are prerequisite to the main initialization. Specifically, it performs the following actions: 

* **Activates Conda Environment**: Activates the Tethys Conda environment.
* **Directories**: Creates the directories for static files, workspaces, and media files.
* **File Permissions**: Adjusts file permissions within these directories. 

These actions are necessary because the directories reside in the ``$TETHYS_PERSIST`` volume, which might have been replaced by a host-mounted directory. If any data already exists from an earlier container run, the script ensures that it is preserved.

tethyscore.sls
--------------

The :file:`tethyscore.sls` script performs the core initialization of the Tethys Portal, performing many of the same tasks that would be done during a :ref:`manual_production_installation` of Tethys. These are the primary tasks that are performed by the script:

* **Tethys Settings**: Runs the ``tethys gen settings`` command to set settings with environment variable values.
* **Configuration Files**: Generates the NGINX/Apache and Supervisor configuration files.
* **Database**: Initializes the database and creates the Tethys Portal superuser.
* **Custom Site Settings**: Runs the ``tethys site`` custom to set site settings for the Tethys Portal from environment variable values.

post_app.sls
------------

The :file:`post_app.sls` script performs common app initialization that normally occurs after apps have been installed. These are the primary tasks that are performed by the script:

* **Collect Files**: Collects static files and workspaces.
* **Persists Configs**: Persists the :file:`portal_config.yml`, NGINX, and Supervisor configuration files to the ``$TETHYS_PERSIST`` volume.

top.sls
-------

The :file:`top.sls` script is the entry point for the Salt State scripts. It defines the order in which the Salt State scripts are run. Developers who extend the Docker image should replace the :file:`top.sls` file with a copy that includes their custom scripts to ensure they are run at the appropriate time.

.. _contrib_docker_supporting_files:

Other Scripts
=============

The Docker image includes several shell scripts that are used to support the initialization of the Tethys Portal and Tethys Apps. These scripts are located in the :file:`docker` directory of the Tethys Platform repository.

run.sh
------

The :file:`run.sh` script is the entry point for the Docker container. It is responsible for checking if there is a database connection and then starting the Salt State scripts. Upon successful initialization of the Tethys Portal, it starts Supervisor and tails the logs.

The :file:`run.sh` script has several commandline options that can be passed in to the Docker ``run`` command to modify the behavior of the script. The following options are available:

* ``--skip-perm``: Skips the fix permissions step (which can be time consuming and sometimes unnecessary).
* ``--db-max-count``: The number of attempts to connect to the database before giving up. The default is 24.
* ``--test``: Runs Salt Scripts, but does not start Supervisor (useful for automated testing of Salt State results).

test-docker.sh
--------------

The :file:`test-docker.sh` script can be used as an alternative entry point for the Docker container to verify that the Salt State scripts are working correctly. The script runs the Salt State scripts and then exits, returning the status Salt State execution. If any of the Salt States fail, the script will return a non-zero exit code.


liveness-probe.sh
-----------------

The :file:`liveness-probe.sh` script is used as the health check for the Docker container. It checks if the Tethys Portal is running and healthy. Specifically, it verifies that Supervisor, NGINX, and Daphne (ASGI) processes are running. If any of the services are not healthy, the script will print an error message and return a non-zero exit code. Hosting services like Kubernetes can use the health check to determine if the container is healthy and should be restarted.

.. _contrib_building_the_docker_image:

Building the Docker Image
=========================

The container image can be built using Docker or any other compatible containerization tool, such as Kaniko. To build the image using Docker, run the following command from the root of the Tethys Platform repository, replacing ``<tag>`` with the desired tag for the image:

.. code-block:: bash

    docker build -t tethysplatform/tethys-core:<tag> .

With Build Args
---------------

To build the image with a specific version of Python and Django, use the build args discussed in the :ref:`contrib_dockerfile_build_args` section. For example, to build the image with Python 3.11 and Django 4.2, run the following command:

.. code-block:: bash

    docker build --build-arg PYTHON_VERSION=3.11 --build-arg DJANGO_VERSION=4.2 -t tethysplatform/tethys-core:<tag> .


.. tip::

    For more information on building Docker images, see `Build, tag, and publish an image | Docker Docs <https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/>`_.

Running the Docker Image
========================

To run the image, you will first need to start a database container image:

.. code-block:: bash

    docker run -d --name tethys-db -e POSTGRES_PASSWORD=mysecretpassword postgres

Then you can run the Tethys Platform container image, linking it with the database container and replacing ``<tag>`` with the tag of the image you built or would like to use from Docker Hub. You will also need to provide the necessary environment variables to configure the Tethys Portal settings for the database connection and other settings (see: :ref:`docker_official_image`).

.. code-block:: bash

    docker run -d --name tethys -p 80:80 --link tethys-db -e POSTGRES_PASSWORD=mysecretpassword -e TETHYS_DB_HOST=tethys-db -e TETHYS_DB_PORT=5432 tethysplatform/tethys-core:<tag>

To view the logs of the running container use the following command:

.. code-block:: bash

    docker logs -f tethys

.. tip::

    For more information on running Docker containers, see `docker container run | Docker Docs <https://docs.docker.com/reference/cli/docker/container/run/>`_.

Docker Compose
--------------

Running containers using the ``docker run`` command can be cumbersome, especially when there are multiple containers that need to be run together. `Docker Compose <https://docs.docker.com/compose/>`_ is a tool that allows you to define and run multi-container Docker applications using a YAML file.

The Tethys Platform repository includes a :file:`docker-compose.yml` file that can be used to run the Tethys Platform and database containers together. To use Docker Compose, run the following command from the :file:`docker` directory of the Tethys Platform repository:

.. code-block:: bash

    docker compose up -d

Docker Compose can be used to manage additional services like THREDDS and GeoServer. To learn more about using Docker Compose, review the :ref:`docker_run_with_compose` tutorial.

Start Up Behavior
-----------------

The first time the image is run takes longer than subsequent runs because the image needs to initialize the database and perform other setup tasks. Subsequent runs will be faster because the image will skip most of these steps. Most Salt State steps have an ``unless`` condition that checks for a file that is created after the initial setup is complete. If the file exists, the Salt State step is skipped.