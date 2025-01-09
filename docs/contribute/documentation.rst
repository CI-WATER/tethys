.. _contribute_documentation:

**************************
Contributing Documentation
**************************

**Last Updated:** January 2025

.. _contribute_docs_intro:

Introduction
============

The Tethys Platform documentation (https://docs.tethysplatform.org) is built using `Sphinx <https://www.sphinx-doc.org/en/master/>`_ and hosted on `Read the Docs <https://docs.readthedocs.io/en/stable/>`_. The documentation is written using a lightweight markup language called `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-primer>`_. Sphinx converts the reStructuredText files into HTML, PDF, and other formats.

This guide will help you get started with contributing to the Tethys Platform documentation. It covers essential topics and initial steps to get you up and running quickly.

.. _contribute_docs_files:

Source Files
============

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

The documentation includes many images and a few other binary files. To keep the repository size manageable, we use `Git Large File Storage (LFS) <https://git-lfs.github.com/>`_ to store these files. The images will not be downloaded automatically when you clone the repository. You will need to install Git LFS to download these files (see: :ref:`contribute_docs_build`).

Docstrings
----------

In addition to the RST files, many of the Python objects in the Tethys Platform codebase are documented with `Google Style Python Docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_. These are incorporated into the documentation using a Sphinx extensions called `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ and `napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html>`_. An example of a Google style docstring is shown below:

.. code-block:: Python

   def some_function(arg1, arg2):
       """
       This is a Google style docstring.
       Args:
           arg1 (int): The first argument.
           arg2 (str): The second argument.
       Returns:
           bool: The return value. True for success, False otherwise.
       """
       return True

.. _contribute_docs_build:

How to Build the Documentation
==============================

This section will guide you through the process of building the Tethys Platform documentation on your local machine.

1. **Install Prerequisites**

   Before building the documentation, you will need to install the following prerequisites:

   * `Miniconda <https://docs.anaconda.com/miniconda/install/>`_ - Python package manager
   * `Git <https://git-scm.com/downloads>`_ - Version control system
   * `Git LFS <https://git-lfs.github.com/>`_ - Git extension for managing image and binary files

2. **Clone the Repository**

   Clone your fork of the Tethys Platform GitHub repository to your local machine (see: :ref:`contribute_development_process`):

   .. code-block:: bash

      git clone <FORK_URL>

3. **Initialize Git LFS and Pull Images**
   Initialize Git LFS in the repository and pull the images:

   .. code-block:: bash

      git lfs install
      git lfs pull

   .. note::

       Once Git LFS is installed in your repository, you can commit new images to the repository in the normal fashion. Git LFS will automatically manage the storage of the images.

4. **Create the Docs Environment**

   Create the conda environment for building the documentation:

   .. code-block:: bash

      conda env create -f docs/docs_environment.yml

   Then activate the environment:

   .. code-block:: bash

      conda activate tethys-docs

5. **Build the Documentation**

   Build the documentation using the Makefile:

   .. code-block:: bash

      make html

   The built documentation will be located in the :file:`docs/_build/html` directory.

6. **View the Documentation**

   Open the built documentation in your web browser. Locate the :file:`index.html` file in the :file:`docs/_build/html` directory and open it in your preferred browser.


.. _contribute_docs_autobuild:

sphinx-autobuild
----------------

Any time you make changes to the documentation source files, you will need to rebuild the documentation to see the changes. To avoid having to manually rebuild the documentation every time you make a change, you can use the `sphinx-autobuild <https://github.com/sphinx-doc/sphinx-autobuild#readme>`_ tool. It watches the source files for changes and automatically rebuilds the documentation and reloads the browser when changes are detected.

To use `sphinx-autobuild`, run the following commands:

.. code-block:: bash

   cd docs
   sphinx-autobuild --host 127.0.0.1 --port 8001 . ./_build/html

.. _contribute_docs_clean:

Cleaning the Build Directory
----------------------------

Occasionally, you'll want to clean the build directory to rebuild the documentation from scratch. To do this, run the following command:

.. code-block:: bash

   make clean

If the documentation doesn't open in your web browser automatically, navigate to http://127.0.0.1:8001 in your browser to view the documentation. The documentation will automatically rebuild and reload in the browser when changes are detected.

.. _contribute_docs_narrative:

Narrative Documentation
=======================

* Guides
* Tutorials
* Recipes

.. _contribute_docs_api:

API Documentation
=================

* Sphinx autodoc
* Writing Docstrings
* Referencing docstrings in RST files
* Mocking third party dependencies

.. _contribute_docs_demo_apps:

Demonstration Apps
==================

* Gizmo Showcase
* Layout Showcase

.. _contribute_docs_guidelines:

Screenshot Guidelines
=====================

* Aspect Ratio
* Guest Mode in Browser

.. _contribute_docs_i18n:

Internationalization
====================

* i18n
* https://www.sphinx-doc.org/en/master/usage/advanced/intl.html
