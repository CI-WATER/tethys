.. _index:

*************************
Tethys Platform |version|
*************************

**Last Updated:** September 2024

Tethys is a platform that can be used to develop and host environmental web apps. It includes a suite of free and open source software (FOSS) that has been carefully selected to address the unique development needs of environmental web apps. Tethys web apps are developed using a Python software development kit (SDK) which includes programmatic links to each software component. Tethys Platform is powered by the Django Python web framework giving it a solid web foundation with excellent security and performance. Refer to the :doc:`./features` article for an overview of the features of Tethys Platform.

.. important::

    Tethys Platform |version| has arrived! Check out the :doc:`./whats_new` article for a description of the new features and changes.

.. _quickstart:

Quick Start
===========

The quickest way to get started with Tethys Platform is via ``conda`` (`Miniconda <https://docs.anaconda.com/miniconda/miniconda-install/>`_ or `Anaconda <https://docs.anaconda.com/anaconda/install/>`_):

.. code-block:: bash

    conda create -n tethys -c conda-forge tethys-platform
    conda activate tethys
    tethys quickstart

.. tip::

    For more details on the installation process see :ref:`development_installation`.
    
Your browser will automatically open to http://127.0.0.1:8000/. 

.. figure:: images/getting_started/hello_world_login.png
    :width: 600px
    :align: center

.. admonition:: Log in with:

   **Username**: admin
   
   **Password**: pass

Voilá! Your very own Hello World application!

.. figure:: images/getting_started/hello_world_app.png
    :width: 600px
    :align: center

Time to develop! The code behind your Hello World app can be found in your current working directory in the newly-created ``tethysapp-hello_world`` folder.

Next Steps
----------

There are several directions that you may want to go from here.

* Install an app you have already developed using the :ref:`app_installation` guide.
* Complete one or more :ref:`tutorials` to learn how to develop apps using Tethys Platform.
* Install one or both of the :ref:`installation_showcase_apps` to see live demos and code examples of Gizmos and Layouts.
* Checkout the :doc:`./installation/web_admin_setup` docs to customize your Tethys Portal.
* For help getting started with docker see :ref:`using_docker`

Contents
========

.. toctree::
   :maxdepth: 1
   
   features
   whats_new
   installation
   installation/update

App Development
===============

.. toctree::
   :maxdepth: 2

   tutorials
   dev_guides

Production Installation
=======================

.. toctree::
   :maxdepth: 3

   installation/production

Contributing to Tethys Platform
===============================

.. toctree::
   :maxdepth: 2

   contribute
   repos
   supplementary

Acknowledgements
================

This material is based upon work supported by the National Science Foundation under Grant No. 1135482

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

