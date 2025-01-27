.. _supplementary_docker_testing:

Test Docker Containers
======================

If you would like, you may perform the following tests to ensure the containers are working properly.


Activate the virtual environment if you have not done so already and use the following Tethys command to start the Docker containers:

::

  . /usr/lib/tethys/bin/activate
  tethys docker start

.. note::

  Although each Docker container seem to start instantaneously, it may take several minutes for the started containers to be fully up and running.

Use the following command in the terminal to obtain the ports that each software is running on:

::

  tethys docker ip

You will be able to access each software on ``localhost`` at the appropriate port. For example, GeoServer and 52 North WPS both have web administrative interfaces. In a web browser, enter the following URLs replacing the ``<port>`` with the appropriate port number from the previous command:

::

  # GeoServer
  http://localhost:<port>/geoserver

  # 52 North WPS
  http://localhost:<port>/wps

With some luck, you should see the administrative page for each. Feel free to explore. You can login to the 52 North WPS admin site using the username and password you specified during installation or the defaults if you accepted those which are:

Default 52 North WPS Admin

* Username: wps
* Password: wps


You are not given the option of specifying a custom username and password for GeoServer, because it can only be done through the web interface. You may log into your GeoServer using the default username and password:

Default GeoServer Admin

* Username: admin
* Password: geoserver

The PostgreSQL database is installed with the database users and databases required by Tethys Platform: **tethys_default**, **tethys_db_manager**, and **tethys_super**. You set the passwords for each user during installation of the container. You can test the database by installing the `PGAdmin III <http://www.pgadmin.org/>`_ desktop client for PostgreSQL and using the credentials of the **tethys_super** database user to connect to it. For more detailed instructions on how to do this, see the :doc:`./pgadmin`.