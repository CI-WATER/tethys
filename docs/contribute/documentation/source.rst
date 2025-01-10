.. _contribute_docs_files:

************
Source Files
************

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
======================

The documentation includes many images and a few other binary files. To keep the repository size manageable, we use `Git Large File Storage (LFS) <https://git-lfs.github.com/>`_ to store these files. The images will not be downloaded automatically when you clone the repository. You will need to install Git LFS to download these files (see: :ref:`contribute_docs_build`).

Docstrings
==========

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