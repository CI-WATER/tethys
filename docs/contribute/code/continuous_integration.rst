.. _code_ci:

*************************************
Continuous Integration and Automation
*************************************

**Last Updated:** February 2025

Continuous integration and continuous delivery (CI/CD) is a software development practice where code changes are automatically built, tested, and deployed. This practice helps to catch bugs early in the development process and ensures that the codebase is always in a deployable state. This guide provides an overview of the CI/CD workflows and automation tools used in the Tethys Platform development process.

GitHub Actions
==============

Tethys Platform uses `GitHub Actions <https://docs.github.com/en/actions>`_ for CI/CD and automation. GitHub Actions is a CI/CD service that is integrated into GitHub repositories and allows open source projects hosted on GitHub to automate software development workflows directly from their GitHub repositories.

Workflow Files
--------------

The GitHub Actions for Tethys Platform are defined in the :file:`.github/workflows` directory of the repository. In this directory are two workflows files: 

* :file:`tethys.yml`: Contains the main development jobs that run on pushes and pull requests to the repository. Jobs in this workflow include linting and formatting checks, running tests, building Docker images and Conda packages, and Docker container tests.
* :file:`tethys-release.yml`: Contains release jobs that run when a new tag created/pushed to the repository. Jobs in this workflow include building and uploading Docker images and Conda packages.

Triggers
--------

A trigger is a repository event or user action that starts a workflow run. There are many `events that can trigger GitHub actions workflows <https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows>`_. The following are the events that are used to trigger the Tethys Platform workflows:

* **Push**: Pushes to the default branch (main) trigger the :file:`tethys.yml` workflow.
* **Pull Request**: Pull Requests to any branch trigger the :file:`tethys.yml` workflow.
* **Schedule**: Once per week, the :file:`tethys.yml` workflow is triggered to ensure the codebase is always in a functioning state, even in periods of low development activity.
* **Tag**: Tags created on any branch trigger the :file:`tethys-release.yml` workflow.

Jobs
----

Each workflow file contains multiple jobs that are run in parallel. Some jobs are defined in both workflow files, with some minor differences. Each job is described in the following sections.

Lint
~~~~

The ``lint`` job, titled "Lint with Flake8", is found in the :file:`tethys.yml`. It uses the `Flake8 <https://flake8.pycqa.org/en/latest/>`_ linter to verify that the code style conforms to Python best practices. The Flake8 analysis can be customized by settings found in :file:`tox.ini` at the root of the repository. See the `Flake8 documentation <https://flake8.pycqa.org/en/latest/user/configuration.html>`_ for more information on configuring Flake8.

Format
~~~~~~

The ``format`` job, titled "Check Black Formatting", is found in :file:`tethys.yml`. It uses the `Black <https://black.readthedocs.io/en/stable/>`_ code formatter to check if the Python code adheres to the project's coding standards. Using a code formatter simplifies code reviews and keeps the code consistent.

This job makes use of the `psf/black <https://black.readthedocs.io/en/stable/integrations/github_actions.html>`_ GitHub action to run the Black formatter. At the time of writing, there was no configuration for Black for Tethys Platform (i.e. the default configuration is used), however if custom configuration is desired in the future, it should done by adding a ``tool.black`` section to the :file:`pyproject.toml` file at the root of the project. See the `Black configuration documentation <https://black.readthedocs.io/en/stable/usage_and_configuration/index.html>`_ for more information on configuring Black.

Tests
~~~~~

The ``test`` job, titled "Tests (<os>, <django_version>, <python_version>)", is found in the :file:`tethys.yml`. This job employs a `matrix <matrix_link>`_ strategy to create a copy of the job for each combination of OS (platform), Django version, and Python version, as defined in ``tests.strategy.matrix``. The matrix parameters are passed to the job and used to set up the test runs on the corresponding platform and with the correct versions of Django and Python installed. The result is the Python test suite is run once for each combination of listed Python version x Django version x operating system to ensure compatibility across different environments.

The ``test`` jobs use the :file:`scripts/install_tethys.sh` script to install the Tethys Platform dependencies and set up the environment for testing. The tests are run using the `unittest <https://docs.python.org/3/library/unittest.html>`_ framework via a custom ``tethys test`` command. Each job generates a code coverage report, but the coverage check is evaluated using the coverage results for only one of the jobs (see :ref:`code_ci_coveralls` below for more details).

Docker Build
~~~~~~~~~~~~

The ``docker-build`` job, titled "Docker Build (<os>, <django_version>, <python_version>)", is found in both :file:`tethys.yml` and :file:`tethys-release.yml` files. This job employs a `matrix <matrix_link>`_ strategy to create a copy of the job for each combination of OS (platform), Django version, and Python version, as defined in ``docker-build.strategy.matrix``. The matrix parameters are passed to the job and used to build a Docker image with the corresponding versions of Django and Python installed. The Docker image is built using the :file:`Dockerfile` located at the root of the repository.

The difference between the :file:`tethys.yml` and :file:`tethys-release.yml` ``docker-build`` jobs is how the images are tagged and where they are published after the build succeeds:

* :file:`tethys.yml`:
    *  Tag pattern: ``dev-py<python_version>-dj<django_version>``
    *  Only uploaded to the `Tethys Platform Docker Hub <https://hub.docker.com/r/tethysplatform/tethys-core/tags>`_ when a **Push** event triggered the job (i.e. when changes are merged into ``main``). 
* :file:`tethys-release.yml`:
    * Tag pattern: ``<tag>-py<python_version>-dj<django_version>``
    * Uploaded to the `Tethys Platform Docker Hub <https://hub.docker.com/r/tethysplatform/tethys-core/tags>`_.

Docker Start-up Tests
~~~~~~~~~~~~~~~~~~~~~

The ``startup_test`` job, titled "Docker Start-up Test (<os>, <django_version>, <python_version>)", is found in :file:`tethys.yml`. This job employs a `matrix <matrix_link>`_ strategy to create a copy of the job for each combination of OS (platform), Django version, and Python version, as defined in ``startup_test.strategy.matrix``. The matrix parameters are passed to the job and used to run the corresponding Docker image built in the ``docker-build``. The Docker image is started in a test mode to ensure that it starts up successfully without any Salt failures.

Conda Build
~~~~~~~~~~~

The ``conda-build`` job, titled "Conda Build (os)", is found in both the :file:`tethys.yml` and :file:`tethys-release.yml` files. While technically a `matrix <matrix_link>`_ job, this job is only run once on Ubuntu as a ``noarch`` build meaning the build is OS agnostic. Each job builds two Conda packages: a standard package (all dependencies) and a ``micro-tethys`` package. For each package, the job installs the dependencies for Tethys, generates a Conda recipe file (:file:`meta.yaml`), and builds a Conda package using the recipe. 

The recipe file is generated using the ``tethys gen metayaml`` command, which compares the dependencies that were just installed to those listed in the :file:`environment.yml` or :file:`micro_environment.yml` files. The dependencies listed in the generated ``meta.yaml`` file are pinned to an appropriate version based on the ``env.CONDA_BUILD_PIN_LEVEL`` environment variable. At the time of writing, dependencies were being pinned to the ``minor`` version number. Pinning to the ``minor`` version number balances the stability of the release with security. The assumption made is that the dependencies installed in this job are the same as those that were installed in the last successful ``test`` job runs.

The difference between the :file:`tethys.yml` and :file:`tethys-release.yml` ``conda-build`` jobs is which channel the packages are published to after the build succeeds:

* :file:`tethys.yml`:
    * If the workflow was triggered by a **Push** event (e.g.: merge to main), the packages are uploaded to the ``dev`` channel of the `Tethys Platform Anaconda Cloud <https://anaconda.org/tethysplatform/tethys-platform>`_.
    * If the workflow was triggered by a **Pull Request** event, the packages are not uploaded.
*  :file:`tethys-release.yml`:
    * If the tag has a prerelease suffix (e.g. ``rc``, ``alpha``, ``beta``), the packages are uploaded to the ``dev`` channel of the `Tethys Platform Anaconda Cloud <https://anaconda.org/tethysplatform/tethys-platform>`_.
    * If the tag is a normal release (e.g. ``1.2.3``), the packages are uploaded to the ``main`` channel of the `Tethys Platform Anaconda Cloud <https://anaconda.org/tethysplatform/tethys-platform>`_.

.. note::

    The Conda packages built and published with these jobs are **NOT** the same as those published to Conda Forge, which has its own process for automating package builds and uploads. The Conda Build GitHub Actions jobs are maintained because they can catch issues that may occur with the Conda build process. Additionally, the packages published to Anaconda Cloud provide a convenient alternative if issues or delays are encountered with the Conda Forge build, which usually lags by about a day. See :ref:`deploying_tethys` for more details on the Conda Forge build process for Tethys Platform.

Third-Party Integrations
------------------------

The Tethys Platform CI/CD workflows use several third-party integrations for additional checks and automation. These integrations are described in the following sections.

.. _code_ci_coveralls:

Coveralls
~~~~~~~~~

The `Coveralls GitHub Action <https://github.com/marketplace/coveralls>`_ is used to publish and evaluate the code coverage report generated by the test jobs. The published results can be viewed on the `Tethys Platform Coveralls page <https://coveralls.io/github/tethysplatform/tethys>`_. Administrators of the Tethys Coveralls repo can configure what constitutes a failure for coverage (i.e. minimum % coverage). At the time of writing this was configured to fail if the coverage drops below 100%, but branch coverage is not enforced. For access to the Tethys Platform Coveralls repo or to change the coverage settings, contact a Tethys Platform admin to request access (see :ref:`contribute_intro_communication`).

Read the Docs
~~~~~~~~~~~~~

A GitHub integration has been set up with Read the Docs to automatically build the documentation for Pull Requests. This integration builds a temporary version of the documentation for the PR and provides a link to it in the PR checks. This provides a rendered version of the documentation for reviewers. The added check also fails if the documentation build fails, which helps catch documentation issues early in the development process.

.. tip::

    For more details about the documentation build process, see: :ref:`contribute_documentation`.

Secrets
-------

The CI/CD workflows make use of the `GitHub Secrets <https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions>`_ feature to store sensitive information and configuration settings. This allows these values to be stored securely and updated independently of the workflow files.

Secrets are stored in two places: Tethys Platform repository settings and the Tethys Platform organization settings. Secrets stored at the organization level can be accessed by any of the Organization's workflows, while repository Secrets are only accessible to that repository.

The use of one of these values in a workflow file is denoted by the ``secrets.<secret_name>`` syntax. For example, to use the ``DOCKER_USERNAME`` secret in a workflow file, the value would be accessed as ``secrets.DOCKER_USERNAME``.

If a new secret needs to be added or an existing secret needs to be updated, please contact a Tethys Platform admin (see :ref:`contribute_intro_communication`).

.. _matrix_link: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow










