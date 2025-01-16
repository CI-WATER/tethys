.. _contribute_rtd:

*************
Read the Docs
*************

**Last Updated:** January 2025

The Tethys Platform documentation (https://docs.tethysplatform.org) is hosted on `Read the Docs (RTD) <https://docs.readthedocs.io/en/stable/>`_. The purpose of this guide is to provide guidance on how the Tethys Platform RTD project is configured and maintained. For a detailed explanation of RTD features see: `Read the Docs: documentation simplified <https://docs.readthedocs.io/en/stable/index.html>`_. 

Dashboard
=========

The RTD web app or dashboard is used to manage the Tethys Platform documentation project. You will need to `create a Read the Docs account <https://app.readthedocs.com/accounts/signup/>`_ and then be granted access to the **Tethys Platform RTD project**. Please contact a Tethys Platform admin to request access (see :ref:`contribute_intro_communication`). Once this is done, you will be able to access the RTD dashboard for the Tethys Platform documentation project at: https://app.readthedocs.org/dashboard/. After logging in, you will see a list of RTD projects that you have access to. Click on the **Tethys Platform** project to access the project dashboard. For more details on the RTD dashboard see: `Read the Docs: dashboard <https://docs.readthedocs.io/en/stable/glossary.html#term-dashboard>`_.

Versions
========

The **Versions** tab displays the different versions of the documentation that are maintained. The following versions are maintained for the Tethys Platform documentation:

* **stable** (default): The version of the documentation for the latest stable release of Tethys Platform. This version corresponds with the latest tag in the GitHub repository. This version should be considered the "production" version of the documentation.
* **latest**: The version of the documentation that corresponds with the latest changes on the ``main`` branch. This includes changes that will be released in a future version. The **latest** version should be considered the "development" version of the documentation.
* **X.Y.Z**: The last patch version of every major release of Tethys Platform, kept for historical purposes. At the time of writing the versions maintained in this category included ``1.4.0``, ``2.1.7``, and ``3.4.4``.

For more information on maintaining versions see: `Versions — Read the Docs <https://docs.readthedocs.io/en/stable/versions.html>`_.

Builds
======

The **Builds** tab displays the build history for the documentation. Each time the documentation is built, a new build is added to the list. New builds of documentation are triggered when the following conditions are met:

* A new commit is pushed to the ``main`` branch.
* A new tag is pushed to the repository.
* A pull request is opened or merged.

The build history includes the build number and a reference to the commit, pull request or tag that triggered the build. Logs of the build are also accessible by clicking on the build title link. Admins are also able to trigger a rebuild for any build that has failed. This is very useful for debugging failed builds.

For a detailed overview on the RTD build process see: `Builds — Read the Docs <https://docs.readthedocs.io/en/stable/builds.html>`_.

The :file:`.readthedocs.yml` File
---------------------------------

The :file:`.readthedocs.yml` file is the configuration file for the RTD builds and is located in the repository root directory (the same directory as the :file:`pyproject.toml`). This file is used to customize the build process for the documentation, providing hooks to different parts of the build process. For example, for the Tethys Platform build it is necessary to install Git LFS and pull the images before building the documentation. This is handled in the ``post_checkout`` section of the :file:`.readthedocs.yml` file.

For a detailed explanation of the :file:`.readthedocs.yml` file see: `Configuration file reference — Read the Docs <https://docs.readthedocs.io/en/stable/config-file/v2.html>`_.

Settings
========

The **Settings** tab is where the configuration settings for the RTD project are maintained. The settings are organized into sections that control different aspects of the documentation build process. Examples of settings that can be configured in this tab include the following:

* **Maintainers**: The RTD users that have access to the project.
* **Repository URL**: The URL of the GitHub repository that contains the documentation source files.
* **Default Branch**: The branch that the documentation is built from. This is typically the ``main`` branch.
* **Domains**: The custom domain that the documentation is hosted on. This is where we set the documentation to be hosted at ``docs.tethysplatform.org`` instead of ``tethys-platform.readthedocs.org``.
* **Notifications**: The email addresses that receive notifications when the documentation build fails.
* **Git Integrations**: The GitHub integrations that are connected to the RTD project.
* **Addons**: Settings for RTD Addons such as the Flyout menu, Search, and Analytics.

For a detailed explanation of the RTD settings see: `Settings — Read the Docs <https://docs.readthedocs.io/en/stable/settings.html>`_.
