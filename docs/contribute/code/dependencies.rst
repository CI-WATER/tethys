.. _maintain_dependencies:

*********************
Maintain Dependencies
*********************

**Last Updated:** January 2025

Dependencies are the libraries, packages, and other software that Tethys Platform relies on to function. Most of these dependencies are maintained by others in the open source community, but some are maintained by the developers of Tethys Platform. This document outlines the process for maintaining dependencies for Tethys Platform.

.. _contrib_deps_python:

Python Dependencies
===================

The Python dependencies are tracked in several Conda :file:`environment.yml` files:

* :file:`environment.yml`: Lists all Python dependencies of Tethys Platform, including those needed for optional features. This file is used to build the current |version| release of Tethys Platform.
* :file:`micro_environment.yml`: Lists only the minimal dependencies needed to run Tethys Platform, excluding the dependencies needed by optional features. This file is used to build the Micro-Tethys release of Tethys Platform (see: :ref:`contrib_deps_optional_dependencies`). 
* :file:`docs/docs_environment.yml`: Lists the Python dependencies needed to build the Tethys Platform documentation.


.. _contrib_deps_optional_dependencies:

Optional Dependencies and Micro-Tethys
--------------------------------------

As the the Tethys Project has grown and added more features, the number of dependencies have also grown. The large number of dependencies has made it more difficult to install Tethys Platform. This is primarily caused by the complex, interconnected web of dependency version requirements that the Conda solver must sort through. Occasionally, the Conda solver is not able to solve the environment, which prevents users from installing Tethys Platform. Using a faster solver, like `Conda libmamba solver <https://www.anaconda.com/blog/conda-is-fast-now>`_ usually side steps this issue, but not always.

To address this issue, the optional dependencies feature was introduced early in the 4.X series. Optional dependencies are dependencies that are not required to run Tethys Platform, but are required to enable certain features (e.g. captchas, persistent stores, and analytics). By making these dependencies optional, users can install Tethys Platform faster and more easily. Optional dependencies are then installed "on demand" when they are needed for a certain feature.

To support backward compatibility, the primary release of Tethys Platform (4.X) still ships with all of the optional dependencies being installed. However, there is a secondary release, called Micro-Tethys, that ships with only the minimal dependencies needed to run Tethys Platform (see Tip box of the :ref:`Install the tethys-platform Conda Package step <getting_started_install_tethys>`). Users can install the optional dependencies as needed to enable the optional features. In version 5.0, the Micro-Tethys release will become the default release.

Adding Dependencies
-------------------

When adding new dependencies to Tethys Platform, developers should consider whether the dependency is required for the core functionality of Tethys Platform or if it is supporting an optional feature. If the dependency is required for core functionality, it should be added to both the :file:`environment.yml` and :file:`micro_environment.yml` files. If the dependency is needed for an optional feature, it should be added to the :file:`environment.yml` file only in the Optional Dependency section. The documentation for the features should include instructions for installing the optional dependency to enable the feature. For an example of optional dependency installation instructions in the documentation, see :ref:`persistent_stores_api`.

Add dependencies to the :file:`environment.yml` files as **unpinned** dependencies (without a version number). This enables the dependencies to automatically update to their latest versions during automated testing runs, allowing potential issues introduced by these new versions to be detected. Dependencies are automatically pinned to the versions used in the last successful test run during the release process to ensure greater stability in the releases.

Conda Forge Packages
--------------------

The Tethys Platform package is published on the `Conda Forge <https://conda-forge.org/>`_ channel so that it can be easily installed using `Conda <https://conda.org/>`_. The Conda Forge channel is a community-maintained collection of Conda packages. One requirement for packages being published on the Conda Forge channel is that all of their dependencies must also be published on the Conda Forge channel. As a result, *all* of the Tethys Platform dependencies must also be published on the Conda Forge channel.

However, not all Python package maintainers release their packages on Conda Forge, but anyone can create a Conda Forge package for any Python library by creating a Conda Forge feedstock for the package. A feedstock is a repository that contains the recipe for building the package and publishing it on the Conda Forge channel. You **do not** have to be a maintainer of a Python library to package it on Conda Forge.

The Tethys Platform developers maintain `Conda Forge feedstocks <https://conda-forge.org/docs/maintainer/adding_pkgs.html>`_ for many of the project's Python dependencies. The following spreadsheet lists the Conda Forge feedstocks that Tethys Platform developers maintain: `Tethys Platform Conda Forge Feedstocks <https://docs.google.com/spreadsheets/d/1H7V-oKfgA3vE7aSko04ELPWQRVEzRziVrZpJsrSV7Ig/edit>`_. To assist with maintaining a feedstock, create a personal fork of the repository, add your GitHub username to the :file:`recipe/meta.yaml`, and submit a pull request.

.. tip:

    For more information about creating and maintaining Conda Forge feedstocks, see `Maintainer Documentation | Conda Forge <https://conda-forge.org/docs/maintainer/>`_.

Project Maintained Dependencies
-------------------------------

The Tethys Platform developers maintain several of the project's dependencies. These are separate projects that contain functionality that is general purpose enough to be useful outside of Tethys Platform. The following sections briefly describe each of these dependencies and where they can be found.

Tethys Dataset Services
~~~~~~~~~~~~~~~~~~~~~~~

Tethys Dataset Services (TDS) provides high-level Python APIs for GeoServer and CKAN. These are used to support the Tethys Services functionality in Tethys Platform (see: :ref:`tds_geoserver_reference` and :ref:`tds_ckan_reference`).

* **Source Code**: https://github.com/tethysplatform/tethys_dataset_services
* **Documentation**: :ref:`tds_geoserver_reference` and :ref:`tds_ckan_reference`
* **PyPI Package**: https://pypi.org/project/tethys-dataset-services/
* **Conda Forge Feedstock**: https://github.com/conda-forge/tethys_dataset_services-feedstock

Tethys Dask Scheduler
~~~~~~~~~~~~~~~~~~~~~

The Tethys Dask Scheduler is an extended version of the Dask Scheduler that is able to communicate with a Tethys Portal to update associated Tethys Job statuses (see: :ref:`tethys_job_dask` and :ref:`tutorials_dask`).

* **Source Code**: https://github.com/tethysplatform/tethys_dask_scheduler
* **Documentation**: :ref:`tethys_job_dask` and :ref:`tutorials_dask`
* **PyPI Package**: https://pypi.org/project/tethys-dask-scheduler/
* **Conda Forge Feedstock**: https://github.com/conda-forge/tethys_dask_scheduler-feedstock

CondorPy
~~~~~~~~

CondorPy is a Python package that provides a high-level interface for submitting and managing jobs on a HTCondor cluster. It is used by the Tethys Job Manager to submit and manage Tethys Jobs on a HTCondor cluster (see: :ref:`tethys_jobs_condor` and :ref:`tethys_jobs_condor_workflow`).

* **Source Code**: https://github.com/tethysplatform/condorpy
* **Documentation**: https://www.tethysplatform.org/condorpy/
* **PyPI Package**: https://pypi.org/project/condorpy/
* **Conda Forge Feedstock**: https://github.com/conda-forge/condorpy-feedstock

Bokeh Django
~~~~~~~~~~~~

The bokeh-django package provides support for running Bokeh apps in Django. Tethys Platform uses this package to run Bokeh widgets within Tethys Apps via the handler functionality (see :ref:`handler-decorator`).

* **Source Code**: https://github.com/bokeh/bokeh-django
* **Documentation**: https://github.com/bokeh/bokeh-django/blob/main/README.md
* **PyPI Package**: https://pypi.org/project/bokeh-django/
* **Conda Forge Feedstock**: https://github.com/conda-forge/bokeh-django-feedstock

.. _contrib_deps_javascript:

JavaScript Dependencies
=======================

Tethys Platform has many JavaScript dependencies that are required to support the dynamic, interactive functionality. These include libraries for plotting, mapping, interactive tables, and interactive controls like date pickers and searchable dropdowns.

CDN and ``npm`` Support
-----------------------

Tethys Platform supports two modes for hosting JavaScript dependencies: CDN hosted (default) or self hosted.

**CDN Hosted**

The default mode for Tethys Portal to retrieve JavaScript dependencies is to retrieve the packages from the `jsDelivr <https://www.jsdelivr.com/>`_ CDN (Content Delivery Network) as needed. The advantage of using a CDN is that it allows for faster and more reliable delivery of content and offloads the load to third-party servers. CDN servers are able to handle high traffic volumes resulting in overall performance improvements.

The reason the ``jsDelivr`` CDN is used is twofold:

1. ``jsDelivr`` automatically packages all packages published on `npm <https://www.npmjs.com/>`_ (Node Package Manager), the worlds largest software registry. It is likely that any JavaScript dependency that Tethys needs will be on ``npm``, and thus ``jsDelivr``.
2. To support the ability to download dependencies for the self hosted mode, which is discussed in more detail below.

**Self Hosted**

In some cases, it is not feasible to rely on the CDN mode for JavaScript dependencies, usually due to organization policies or running in an offline environment. For these cases, Tethys Platform provides a self-hosted mode. In this mode, the dependencies are downloaded from ``npm`` using the ``npm`` commandline tool and Tethys Portal hosts the dependencies itself (see: :ref:`self_hosted_deps_config`).

The :file:`dependencies.py` File
--------------------------------

A list of JavaScript dependencies is maintained in the :file:`dependencies.py` file located in the :file:`tethys_portal` package. In this file is a variable named ``vendor_static_dependencies`` that contains the list (in dictionary form).

Adding Dependencies
-------------------

To add a new JavaScript dependency to Tethys Platform, do the following:

1. Locate the dependency on `jsDelivr <https://www.jsdelivr.com/>`_.
2. Open :file:`tethys_portal/dependencies.py`.
3. Locate the ``vendor_static_dependencies`` dictionary near the end of the file.
4. Add a new key to the dictionary as a unique lookup key for the dependency (please maintain alphabetical order).
5. Create a new instance of ``JsDelivrStaticDependency`` for the value, filling in the necessary information:

   * **npm_name**: Name of the NPM package.
   * **version**: Version of the package for Tethys Platform to use.
   * **js_path**: Relative path to the JavaScript file, usually a :file:`*.min.js` file.
   * **js_integrity**: The integrity string for the specific version of the JavaScript file (if available).
   * **css_path**: Relative path to the CSS file, usually a :file:`*.min.css` file (if applicable).
   * **css_integrity**: The integrity string for the specific version of the CSS file (if available).

.. tip::

    Compare an existing entry in ``vendor_static_dictionary`` to what you find on ``jsDelivr`` for that package.