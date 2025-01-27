.. _contribute_docs_build:

******************************
How to Build the Documentation
******************************

**Last Updated**: January 2025

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
================

Any time you make changes to the documentation source files, you will need to rebuild the documentation to see the changes. To avoid having to manually rebuild the documentation every time you make a change, you can use the `sphinx-autobuild <https://github.com/sphinx-doc/sphinx-autobuild#readme>`_ tool. It watches the source files for changes and automatically rebuilds the documentation and reloads the browser when changes are detected.

To use `sphinx-autobuild`, run the following commands:

.. code-block:: bash

   cd docs
   sphinx-autobuild --host 127.0.0.1 --port 8001 . ./_build/html

.. _contribute_docs_clean:

Cleaning the Build Directory
============================

Occasionally, you'll want to clean the build directory to rebuild the documentation from scratch. To do this, run the following command:

.. code-block:: bash

   make clean

If the documentation doesn't open in your web browser automatically, navigate to http://127.0.0.1:8001 in your browser to view the documentation. The documentation will automatically rebuild and reload in the browser when changes are detected.