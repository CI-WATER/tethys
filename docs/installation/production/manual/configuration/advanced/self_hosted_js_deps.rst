.. _self_hosted_deps_config:

**************************************
Self Hosted Dependency Mode (Optional)
**************************************

**Last Updated**: January 2025

By default, Tethys Portal retrieves JavaScript dependencies from the `jsDelivr <https://www.jsdelivr.com/>`_ CDN (Content Delivery Network) as needed. However, in certain situations, such as adhering to organizational policies or operating in an offline environment, relying on the CDN may not be practical. This guide provides instructions on how to configure Tethys Portal to host these dependencies locally.

1. Install ``node`` and ``npm``
-------------------------------

Use ``conda`` to install ``node`` and ``npm``:

.. code-block:: bash

    conda install -c conda-forge nodejs

2. Set ``STATICFILES_USE_NPM``
------------------------------

Set the ``STATICFILES_USE_NPM`` setting to ``True``. This configures Tethys to look for dependencies locally, rather than using the CDN.

.. code-block:: bash

    tethys settings --set STATICFILES_USE_NPM True


3. Generate :file:`package.json`
--------------------------------

Run the command below to generate a :file:`package.json`. This file contains a list of JavaScript dependencies for ``npm`` to install.

.. code-block:: bash

    tethys gen package_json

Note the path of the generated :file:`package.json` file. You will need it in the next step.

4. Download Dependencies Using ``npm``
--------------------------------------

Run the ``npm install`` command from the directory that contains the :file:`package.json`:

.. code-block:: bash

    npm install

This will create a :file:`node_modules` directory in the :file:`tethys_portal/static` directory and download all of the JavaScript dependencies to that directory.

5. Collect Static Files
-----------------------

Follow the instructions in :ref:`production_static_workspaces_dirs` to set up the static file directory and collect the static files to that directory for hosting.