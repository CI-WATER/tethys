.. _tethys_cli_install:

install command
***************

This command is used to trigger an automatic install for an application on a portal. We recommend using an
:ref:`install.yml file <tethys_install_yml>` in the app directory to customize the installation process. If the install
file doesn't exist the command will offer to create a blank template install.yml file for you. If you require services
to be setup automatically, place a :ref:`services.yml file <tethys_services_yml>` in the root of your application. If
there are any services that are needed by settings in your app that haven't been setup yet, you will be prompted to
configure them interactively during the installation process. If there are any linked persistent stores upon completing
the installation process, the install command will automatically run ``tethys syncstores {app_name}``. Finally, any
scripts listed in the install.yml will be run to finish the installation.

.. important::

    Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``conda`` itself within your tethys conda environment to be able to install app and extension dependencies with ``conda``. Otherwise, you will receive a prompt to attempt to use pip instead.

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge conda

.. argparse::
   :module: tethys_cli
   :func: tethys_command_parser
   :prog: tethys
   :path: install