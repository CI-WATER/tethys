.. _contribute_docs_files:

**************************
Documentation Source Files
**************************

**Last Updated:** January 2025

The ``docs`` Directory
======================

The reStructuredText (RST) source files for the Tethys Platform documentation are located in the :file:`docs` directory of the `tethysplatform/tethys` repository. In this directory you will find the following files and directories:

* :file:`conf.py` - The Sphinx configuration file.
* :file:`index.rst` - The RST source file for the landing page of the documentation.
* :file:`Makefile` and :file:`make.bat` - Makefiles that are used in building the documentation.
* :file:`docs_environment.yml` - The conda environment file for building the documentation Python environment.
* :file:`README.md` - The README file for the documentation with reminders of the commands used to build the documentation.
* :file:`images` - A directory containing most, but not all, of the images used in the documentation.
* :file:`_static` - A directory containing static files such as images, CSS, and JavaScript.
* :file:`_templates` - A directory containing custom templates for the documentation.
* :file:`_build` - A directory containing the built documentation (only present after building the documentation).
* Over 200 RST files organized into many subdirectories.

Git Large File Storage
----------------------

The documentation includes many images and a few other binary files. To keep the repository size manageable, we use `Git Large File Storage (LFS) <https://git-lfs.github.com/>`_ to store these files. The images will not be downloaded automatically when you clone the repository, so you will need to install Git LFS to download these files (see: :ref:`contribute_docs_build`).

Docstrings in Python Code
-------------------------

In addition to the RST files, many of the Python files in the Tethys Platform codebase include documentation in the form of `Google Style Python Docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_. These are incorporated into the documentation using a Sphinx extensions called `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ and `napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html>`_. Docstrings are discussed in more detail in the :ref:`contribute_docs_reference` section.

.. _contribute_docs_narrative:

Types of Documentation
======================

The documentation for Tethys Platform can be categorized into two main types: narrative and reference. The two types of documentation are often intermixed in the same RST file. Each type is discussed in more detail below.

Narrative Documentation
-----------------------

Narrative documentation is the documentation that is written in a more conversational style. The purpose of narrative documentation is to guide the user through specific tasks or introduce new concepts. It is characterized by step-by-step instructions, explanations, and illustrative examples. Examples of narrative documentation in the Tethys Platform documentation include the tutorials, guides, and recipes. These and other narrative documentation can be found in the following directories:

* :file:`docs/`
   * :file:`contribute/`
   * :file:`software_suite/`
   * :file:`supplementary/`
   * :file:`tethys_portal/`
   * :file:`tethys_sdk/` (mixed)
   * :file:`tutorials/`


.. _contribute_docs_reference:

Reference Documentation
-----------------------

Reference documentation is the documentation that is written in a more concise, factual style. The purpose of reference documentation is to provide detailed information about the various components of Tethys Platform. It is characterized by detailed descriptions of classes, functions, methods, APIs, tables and lists of settings, and other components. Examples of reference documentation in the Tethys Platform documentation include the commandline interface (CLI) documentation and the Tethys Portal configuration documentation. These and other reference documentation can be found in the following files and directories:

* :file:`docs/`
   * :file:`tethys_cli/`
   * :file:`tethys_portal/configuration.rst`
   * :file:`tethys_sdk/` (mixed)


.. _contribute_docs_python_docstrings:

Python Docstrings
-----------------

The Python codebase includes documentation in the form Google Style Docstrings. These docstrings are included in the documentation using the `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ and `napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html>`_ See :ref:`contribute_docs_docstrings` for guidance on writing and including docstrings in the documentation.

.. _contribute_docs_configuration:

The ``conf.py`` file
====================

The :file:`conf.py` file is the Sphinx configuration file for the documentation. It contains settings that control how the documentation is built. The file is organized into sections that control different aspects of the documentation build process. It is sometimes necessary to modify or update this file so a brief explanation of the important sections of the document are described below.

Mock Dependencies
-----------------

When the documentation is built, the modules containing the docstrings are imported. A consequence of this is that most third-party dependencies used by the modules with docstrings either need to be installed in the ``tethys-docs`` conda environment or mocked. Mocking dependencies is the preferred approach, because installing the dependencies takes too long and causes the documentation build on Read the Docs (RTD) to timeout.

Dependencies that need to be mocked during the documentation build are listed in the ``conf.py`` file in the ``MOCK_MODULES`` list. It is sometimes necessary to include submodules in the ``MOCK_MODULES`` list. Please maintain **alphabetical order** when adding new dependencies to the ``MOCK_MODULES`` list. An example of mocking dependencies is shown below:

.. code-block:: python
   :emphasize-lines: 7-8

   MOCK_MODULES = [
       ...
       "social_core",
       "social_core.exceptions",
       "social_django",
       "social_django.utils",
       "some_other_module",
       "some_other_module.submodule",
       "sqlalchemy",
       ...
   ]

.. important::

    Avoid mocking modules that are part of the Tethys Platform codebase. If a Tethys Platform module is mocked, the docstrings in that module will not be included in the documentation. Instead, try to mock the dependencies of the module or that are causing issues.

Django Configuration
--------------------

Django is one of the few third-party dependencies that is not mocked in the documentation build because of how fundamental it is to the Tethys Platform codebase. As a result it is necessary to configure the Django settings in the :file:`conf.py` to prevent ``django.core.exceptions.ImproperlyConfigured`` errors when modules are imported.

Sphinx Configuration
--------------------

Most of the Sphinx configuration settings are included in this section. The settings control the behavior of the Sphinx build process. This includes the settings for the various Sphinx extensions that are used by the Tethys Platform documentation project. For a comprehensive list of Sphinx configuration options. See `Configuration — Sphinx <https://www.sphinx-doc.org/en/master/usage/configuration.html>`_ for a comprehensive list of Sphinx configuration options.


Read the Docs Configuration
---------------------------

This section is actually a subset of the Sphinx Configuration settings. It contains the required RTD settings. These settings are necessary to enable the RTD features such as the version menu and search capabilities. See `Sphinx — Read the docs user documentation <https://docs.readthedocs.io/en/stable/intro/sphinx.html>`_ for more information.

Theme Configuration
-------------------

This section is also a subset of the Sphinx Configuration settings. It contains settings related to controlling the HTML theme that is used to render the documentation. The HTML theme dictates the look and feel of the documentation. The Tethys Platform documentation uses the `Sphinx Awesome Theme <https://sphinxawesome.xyz/>`_.
