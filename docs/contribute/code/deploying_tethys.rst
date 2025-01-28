.. _deploying_tethys:

**********************
Deploying New Versions
**********************

**Last Updated:** January 2025

Versioning
==========

The first step to creating a new release of Tethys Platform is to determine what the new version number should be. Tethys Platform uses Semantic Versioning to streamline the version numbers. Semantic Versioning is a versioning scheme that uses a three-part number format: ``MAJOR.MINOR.PATCH``. Each number has a specific meaning:

* ``MAJOR``: Incremented when making incompatible or "breaking" API changes (i.e. existing functionality will not work the same).
* ``MINOR``: Incremented when adding new functionality in a backward-compatible manner (i.e. existing functionality still works the same).
* ``PATCH``: Incremented when adding backward-compatible bug fixes.

This system helps communicate the nature of changes in each release, making it easier for users to understand the impact of updating to a new version. Here are a few additional tips for semantic versioning:

* Whenever a version number is incremented, the release numbers following it should be reset to zero. For example, if the current version is ``1.2.3`` and breaking changes are introduced, the next version should be ``2.0.0``.
* Version numbers are not to be interpreted as decimal numbers and each version number can be incremented beyond 9. For example, ``1.9.9`` -> ``1.10.0``.
* Pre-release versions can be denoted by appending a hyphen and a series of dot-separated identifiers immediately following the patch version. For example, ``1.0.0-alpha.1``, ``1.0.0-beta.1``, ``1.0.0-rc.1``.

Setuptools SCM
--------------

Tethys Platform uses a tool called ``setuptools_scm`` to automatically manage version numbers based on tags in the git repository. This tool reads the version number from the git tags and sets the version number in the package. This means that the version number in the ``pyproject.toml`` file does not need to be manually updated. Instead, the version number should be updated by creating a new git tag (described later in this document).

In addition, ``setuptools_scm`` automatically generates a version number on the main branch for development versions. This version number is based on the next patch version, the number of commits since that tag, the commit hash, and the current workdir state. For example, if the latest tag/last release was ``1.2.3`` and there have been 5 commits since that tag and there are uncommitted changes the version number would be something like this: ``1.2.4.dev5+a1b2c3d4e.d2024.12.30``.

For more information on setuptools SCM, see the `setuptools_scm documentation <https://setuptools-scm.readthedocs.io/en/latest>`_.

Preparing for a Release
=======================

Before creating a new release, there are a few steps that need to be completed to ensure that the release is complete and successful. These steps include the following:

1. Merge Applicable Pull Requests
2. Label All Pull Requests
3. Package New Dependencies on Conda-Forge
4. Update Documentation
5. Update the What's New Page
6. Ensure all Checks are Passing
7. Update Tutorial Solutions

Merge Applicable Pull Requests
------------------------------

Before creating a new release, all applicable Pull Requests should be merged into the ``main`` branch or target release branch. Only code in the ``main`` branch or release branch will be released. This includes Pull Requests that have been approved and are ready to be merged. See :ref:`contribute_development_process` for more information on merging Pull Requests.

Label All Pull Requests
-----------------------

Review all of the merged pull requests that are included in the new release and ensure each one has at least one Label per the best practices outlined in :ref:`Open a Pull Request - Labels <contribute_pull_request_labels>`. These labels are used to group the list of pull request into categories in the automatically generated release notes on GitHub. 

Package New Dependencies on Conda-Forge
---------------------------------------

If new Python dependencies have been added to the project or new versions of existing dependencies are required, they must be packaged on Conda-Forge. The Conda-Forge build will not succeeed if the new dependencies are not available on Conda-Forge. Don't forget to verify that the correct version is available.

To check if a package is available on Conda-Forge, use the ``conda search`` command:

.. code-block:: bash

    conda search -c conda-forge <package-name>

If a required pacakge is not packaged on conda-forge, you will need to add it. This can be done by following the `Contributing packages <https://conda-forge.org/docs/maintainer/adding_pkgs/>`_ guide on the Conda-Forge website.

Update Documentation
--------------------

Before creating a new release, ensure that the documentation is up-to-date with the latest changes. This includes updating the API documentation and tutorials that are affected by the changes in the release. See :ref:`contribute_documentation` for more information on updating the documentation.

Update the What's New Page
--------------------------

The `What's New page <https://docs.tethysplatform.org/en/stable/whats_new.html>`_ is a page in the Tethys Platform documentation that lists the changes that have been made in each release. This page is used to communicate the changes to users and developers. The What's New page is located in the ``docs/whats_new.rst`` file. To update the What's New page, follow these steps:

1. Open the ``docs/whats_new.rst`` file in a text editor.
2. Move all the content from the previous release to ``docs/whats_new/prior_release.rst``.
3. Add a new heading for the new release the ``docs/whats_new.rst`` file.
4. Add subheadings for each major features with summary bullets and links to relevant documentation.

Ensure all Checks are Passing
-----------------------------

Before creating a new release, ensure that all GitHub checks are passing on the ``main`` branch. These checks are run on every Pull Request and weekly on Sundays. To review the status of the checks navigate to `Tethys Platform GitHub Actions <https://github.com/tethysplatform/tethys/actions>`_.

The checks that need to be passing before creating a new release include:

* The code has been formatted with Black
* No code style lint is found by Flake8 linter
* Code test coverage is at 100%
* All Tests are passing on all supported configurations
* All Docker image builds succeeed for all supported configurations
* Docker start-up tests pass for all supported configurations
* The Conda package build is successful
* Documentation build is successful

See :ref:`contribute_checks` for more information on the automated GitHub checks.

Update Tutorial Solutions
-------------------------

Each tutorial in the Tethys Platform documentation is accompanied by a solution repository on GitHub that contains the completed code for each step of the tutorial. Before creating a new release, these repositories need to be updated with the latest solution code. To update the tutorial solutions, follow these steps:

1. Complete the tutorial steps on your local development environment. You may want to use Git to commit the changes for each tutorial step to separate branches, mimicking the solution repository.
2. Clone the tutorial solution repository from GitHub.
3. Checkout each branch in the solution repository, delete the existing code, and copy the new code from your updated local development environment.
4. Commit and push the changes.

Solution Repositories
+++++++++++++++++++++

The tutorial repositories are located in the Tethys Platform GitHub organization:

* Key Concepts: `tethysplatform/tethysapp-dam_inventory <https://github.com/tethysplatform/tethysapp-dam_inventory>`_
* WebSockets Concepts: `tethysplatform/tethysapp-dam_inventory (websocket-solution branch) <https://github.com/tethysplatform/tethysapp-dam_inventory/tree/websocket-solution>`_
* Quota Concepts: `tethysplatform/tethysapp-dam_inventory (quotas-solution branch) <https://github.com/tethysplatform/tethysapp-dam_inventory/tree/quotas-solution>`_
* Map Layout: `tethysplatform/tethysapp-map_layout_tutorial <https://github.com/tethysplatform/tethysapp-map_layout_tutorial>`_
* GeoServer: `tethysplatform/tethysapp-geoserver_app <https://github.com/tethysplatform/tethysapp-geoserver_app>`_
* THREDDS: `tethysplatform/tethysapp-thredds_tutorial <https://github.com/tethysplatform/tethysapp-thredds_tutorial>`_
* Google Earth Engine: `tethysplatform/tethysapp-earth_engine <https://github.com/tethysplatform/tethysapp-earth_engine>`_
* Dask Tutorial: `tethysplatform/tethysapp-dask_tutorial <https://github.com/tethysplatform/tethysapp-dask_tutorial>`_
* Bokeh Integration Concepts: `tethysplatform/bokeh_tutorial <https://github.com/tethysplatform/tethysapp-bokeh_tutorial>`_

Update Tutorial Solution Tags
+++++++++++++++++++++++++++++

For major and minor version release updates, use the ``scripts/update_tutorial_tags.py`` script to update the tags in each tutorial solution repository. The script will create new tags for each tutorial solution repository with the new version number so that it matches the links that will be generated for the new version in the documentation.

.. important::

    This process will only work if you have write permissions on all of the tutorial repositories. If you do not have write permissions, you will need to ask a Tethys Platform GitHub Organization admin to grant you access.

1. Obtain a GitHub personal access token with the ``read`` and ``write`` scope on all of the tutorial repositories. For more details, see: `GitHub Docs | Managining your personal access tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>`_.

    a. Login to GitHub and Navigate to https://github.com/settings/tokens.
    b. Click on **Generate new token** and select **Generate new token (classic)**.
    c. Enter a note for the token (e.g. "Tethys 4.3 Tutorial Solutions Update").
    d. Set an expiration date for the token (e.g. 7 days).
    e. Under **Select scopes**, select the ``repo`` scope.
    f. Click **Generate token**.
    g. Copy the token to a secure location.

2. Install the GitHub Python package:

.. code-block:: bash

    pip install PyGithub

3. Update version in the ``scripts/update_tutorial_tags.py`` script to the new version number:

.. code-block:: python

    # Tethys Version to Tag For
    tethys_version = "4.3"

.. important::

    The version number should only contain the ``MAJOR`` and ``MINOR`` version numbers. The ``PATCH`` version number should be omitted.

4. Run the script and provide the GitHub personal access token when prompted:

.. code-block:: bash

    cd scripts
    python update_tutorial_tags.py

.. note::

    The :file:`scripts` directory is located at the root of the Tethys Platform repository.

Creating a Release
==================

The release process is varies slightly depending on the type of release being made: Major or Minor Release vs. Patch Release. In both cases, use the Release functionality in GitHub.

.. _contribute_deploy_github_release:

Create GitHub Release
---------------------

First create a new GitHub Release for the new version. This will create a new tag in the repository and generate a release page with the release notes. To create a new GitHub Release, follow these steps:

1. Navigate to the `Tethys Platform Releases <https://github.com/tethysplatform/tethys/releases>`_ page on GitHub.
2. Click on the **Draft a new release** button.
3. Click on **Choose a tag** and enter for the new version in the **Find or create a new tag** field (e.g. ``4.3.0``). 
4. Select the **Create a new tag: <version> on publish** option.
5. Set the **Target branch**:
    * For Major or Minor releases, set the **Target** to be the ``main`` branch.
    * For Patch releases, set the **Target** to be the ``release-<MAJOR.MINOR>`` branch (e.g. ``release-4.3``; see :ref:`contribute_deploy_release_branch`).
6. Leave the **Previous tag** field set to ``auto``.
7. Press the **Generate release notes** button to generate the release notes.
8. Verify that the title of the release is set to the new version number (e.g. ``4.3.0``).
9. Review the release notes and make any necessary adjustments. For Major and Minor releases, compare the changes with the updated What's New page to ensure that all changes are included.
10. Click the **Publish release** button.

.. _contribute_deploy_release_branch:

Create a Release Branch
-----------------------

For Major and Minor releases, a new release branch should be created to manage the release. This branch will be used to manage any bugfixes/patches that are made to the release. To create a new release branch, follow these steps:

1. Navigate to the `Tethys Platform Repository <https://github.com/tethysplatform/tethys>`_ and make sure the ``main`` branch is selected.
2. Click on the **Branch: main** button and enter the new release branch name following the pattern ``release-<MAJOR.MINOR>`` (e.g. ``release-4.3``).
3. Click on the **Create branch release-<MAJOR.MINOR> from 'main'** button.

Verify Builds Pass
------------------

When a new release is created, GitHub Actions will automatically run the  builds for the new version. Navigate to `Tethys Platform Actions <https://github.com/tethysplatform/tethys/actions>`_ and monitor the GitHub actions to ensure the Docker and Conda packages are built and uploaded. If any checks fail, investigate the cause and make any necessary fixes. This may result in the creation of a new patch release.

Updating Release Packages
-------------------------

After the release is created, the release packages will need to be created before users can install the new release. This includes building and uploading the Docker images, Conda-Forge packages, and PyPI packages. The following sections describe how to update each of these packages.

.. _contribute_deploy_conda_forge:

Conda Forge
+++++++++++

The Conda-Forge package for Tethys Platform is semi-automatically built by the Conda-Forge build system. Conda-Forge bots monitor the Tethys Platform GitHub repository for new versions and will automatically create a pull request to the `Tethys Platform Conda-Forge Feedstock <https://github.com/conda-forge/tethys-platform-feedstock>`_ when a new version tag is detected. This pull request will need to be reviewed and merged by one of the Feedstock Maintainers. Once the pull request is merged, the Conda-Forge build system will automatically build the new package and upload it to the `conda-forge channel`.

This semi-automated approach can take several days to resolve. If you need the Conda-Forge package to be built and uploaded immediately, you can manually create a new feedstock pull request. To do this, follow these steps:

1. Navigate to the `Tethys Platform Conda-Forge Feedstock <https://github.com/conda-forge/tethys-platform-feedstock>`_ repository.
2. Create a Fork of the repository to your personal GitHub account (the process won't work on the main repository or Organization repositories).
3. Clone the forked repository to your local machine and make a new feature branch.
4. Make the necessary changes to the ``recipe/meta.yaml`` file:

    * Update the ``version`` number to the new version.
    * Update the ``sha256`` hash to match that of the ``Source code (tar.gz)`` release package found on the `GitHub Release page <https://github.com/tethysplatform/tethys/releases>`_ for that version. The ``sha256`` can be computed by downloadig the tar.gz file and running the following command:

    .. code-block:: bash

        sha256sum tethys-<version>.tar.gz

5. Commit the changes and push the branch to your forked repository.
6. Create a new Pull Request from your forked repository to the main feedstock repository.

Docker
++++++

Docker images for Linux are automatically built by the GitHub actions that are triggered when a new release is created. This process will create an image for each combination of supported Python version and Django version. These images are pushed to the `Tethys Platform Docker Hub Organization <https://hub.docker.com/r/tethysplatform>`_ in the `tethysplaform/tethys-core <https://hub.docker.com/r/tethysplatform/tethys-core>`_ repository.

Python Package Index (PyPI)
+++++++++++++++++++++++++++

At the time of writing, there was no automated process for building the `Tethys Platform PyPI package <https://pypi.org/project/tethys-platform/#description>`_. To update the PyPI package, follow these steps:

1. Clone the Tethys Platform repository to your local machine.
2. Checkout the new release tag.
3. Generate a :file:`requirements.txt` file using the ``tethys gen`` command.

.. code-block:: bash

    tethys gen requirements

.. note::

    Do not commit the :file:`requirements.txt` file to the repository.

4. Review the :file:`requirements.txt` file, removing any conda-only or otherwise unnecessary packages such as ``libmambapy``.

5. Install the required packages for building and uploading the package:

.. code-block:: bash

    pip install setuptools twine build

6. From the repository root, run this command to build the package:

.. code-block:: bash

    python -m build

7. Verify that the .whl and .tar.gz packages have been created in the new :file:`dist` directory. For example:

.. code-block:: bash

    dist/
    ├── tethys_platform-<version>-py3-none-any.whl
    └── tethys_platform-<version>.tar.gz

8. Upload the packages to PyPI using the ``twine`` program:

.. code-block:: bash

    twine upload dist/*


.. note::

    You will need to have a PyPI account with necessary permissions to upload to the Tethys Platform package. Contact a Tethys Platform admin for more information (see :ref:`contribute_intro_communication`).


.. tip::

    For more information on building and uploading packages to PyPI, see the `Python Packaging User Guide <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_.
