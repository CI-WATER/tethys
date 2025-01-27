.. _persistent_stores_api:

*********************
Persistent Stores API
*********************

**Last Updated:** May 2017

.. important::

    This feature requires the ``psycopg2`` and ``sqlalchmey`` libraries to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install these libraries using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge psycopg2 "sqlalchemy<2"

        # pip
        pip install psycopg2 "sqlalchemy<2"

The Persistent Store API streamlines the use of SQL databases in Tethys apps. Using this API, you can provision SQL databases for your app. The databases that will be created are `PostgreSQL <http://www.postgresql.org/>`_ databases. Currently, no other databases are supported.

The process of creating a new persistent database can be summarized in the following steps:

1. create a new PersistentStoreDatabaseSetting in the :term:`app configuration file`,
2. assign a PersistentStoreService to the PersistentStoreDatabaseSetting from the admin pages.
3. create a data model to define the table structure of the database,
4. write a persistent store initialization function, and
5. use the Tethys command line interface to create the persistent store.

More detailed descriptions of each step of the persistent store process will be discussed in this article.

Persistent Store Settings
=========================

Using :term:`persistent stores` in your app is accomplished by adding the ``persistent_store_settings()`` method to your :term:`app class`, which is located in your :term:`app configuration file` (:file:`app.py`). This method should return a list or tuple of ``PersistentStoreDatabaseSetting`` and/or ``PersistentStoreConnectionSetting`` objects. For example:

::

    from tethys_sdk.base import TethysAppBase
    from tethys_sdk.app_settings import PersistentStoreDatabaseSetting


    class App(TethysAppBase):
        """
        Tethys App Class for My First App.
        """
        ...

        def persistent_store_settings(self):
            ps_settings = (
                PersistentStoreDatabaseSetting(
                    name='example_db',
                    description='Primary database for my_first_app.',
                    initializer='my_first_app.model.init_example_db',
                    required=True
                ),
            )

            return ps_settings

.. caution::

    The ellipsis in the code block above indicates code that is not shown for brevity. **DO NOT COPY VERBATIM**.

In this example, a database called "example_db" would be created for this app. It would be initialized by a function called "init_example_db", which is located in a Python module called :file:`init_stores.py`. Notice that the path to the initializer function is given using dot notation (e.g.: ``'foo.bar.function'``).

Persistent store databases follow a specific naming convention that is a combination of the app name and the name that is provided during registration. For example, the database for the example above may have a name "my_first_app_example_db". To register another database, add another ``PersistentStoreDatabaseSetting`` object to the tuple that is returned by the ``persistent_store_settings()`` method.

Assign Persistent Store Service
===============================

The ``PersistentStoreDatabaseSetting`` can be thought of as a socket for a connection to a database. Before we can do anything with the ``PersistentStoreDatabaseSetting`` we need to "plug in" or assign a ``PersistentStoreService`` to the setting. The ``PersistentStoreService`` contains the connection information and can be used by multiple apps. Assigning a ``PersistentStoreService`` is done through the Admin Interface of Tethys Portal as follows:

1. Create ``PersistentStoreService`` if one does not already exist

    a. Access the Admin interface of Tethys Portal by clicking on the drop down menu next to your user name and selecting the "Site Admin" option.

    b. Scroll to the **Tethys Service** section of the Admin Interface and select the link titled **Persistent Store Services**.

    c. Click on the **Add Persistent Store Services** button.

    d. Fill in the connection information to the database server.

    e. Press the **Save** button to save the new ``PersistentStoreService``.

    .. tip::

        You do not need to create a new ``PersistentStoreService`` for each ``PersistentStoreDatabaseSetting`` or each app. Apps and ``PersistentStoreDatabaseSettings`` can share ``PersistentStoreServices``.

2. Navigate to App Settings Page

    a. Return to the Home page of the Admin Interface using the **Home** link in the breadcrumbs or as you did in step 1a.

    b. Scroll to the **Tethys Apps** section of the Admin Interface and select the **Installed Apps** linke.

    c. Select the link for your app from the list of installed apps.



3. Assign ``PersistentStoreService`` to the appropriate ``PersistentStoreDatabaseSetting``

    a. Scroll to the **Persistent Store Database Settings** section and locate the ``PersistentStoreDatabaseSetting``.

    .. note::

        If you don't see the ``PersistentStoreDatabaseSetting`` in the list, uninstall the app and reinstall it again.

    b. Assign the appropriate ``PersistentStoreService`` to your ``PersistentStoreDatabaseSetting`` using the drop down menu in the **Persistent Store Service** column.

    c. Press the **Save** button at the bottom of the page to save your changes.

.. note::

    During development you will assign the ``PersistentStoreService`` setting yourself. However, when the app is installed in production, this steps is performed by the portal administrator upon installing your app, which may or may not be yourself.

Data Model Definition
=====================

The tables for a persistent store should be defined using an SQLAlchemy data model. The recommended location for data model code is :file:`model.py` file that is generated with the scaffold. The following example illustrates what a typical SQLAlchemy data model may consist of:

::

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, Float

    # DB Engine, sessionmaker, and base
    Base = declarative_base()


    # SQLAlchemy ORM definition for the stream_gages table
    class StreamGage (Base):
        """
        Example SQLAlchemy DB Model
        """
        __tablename__ = 'stream_gages'

        # Columns
        id = Column(Integer, primary_key=True)
        latitude = Column(Float)
        longitude = Column(Float)
        value = Column(Integer)

        def __init__(self, latitude, longitude, value):
            """
            Constructor for a gage
            """
            self.latitude = latitude
            self.longitude = longitude
            self.value = value

Object Relational Mapping
-------------------------

Each class in an SQLAlchemy data model defines a table in the database. Each object instantiated using an SQLAlchemy class represent a row or record in the table. The contents of a table or multiple rows would be represented as a list of SQLAlchemy objects. This pattern for interacting between database tables using objects in code is called Object Relational Mapping or ORM.

The example above consists of a single table called "stream_gages", as denoted by the ``__tablename__`` property of the ``StreamGage`` class. The ``StreamGage`` class is defined as an SQLAlchemy data model class because it inherits from the ``Base`` class that was created in the previous lines using the ``declarative_base()`` function provided by SQLAlchemy. This inheritance makes SQLAlchemy aware of the ``StreamGage`` class is part of the data model. All tables belonging to the same data model should inherit from the same ``Base`` class.

The columns of tables defined using SQLAlchemy classes are defined by properties that contain ``Column`` objects. The class in the example above defines four columns for the "stream_gages" table: ``id``, ``latitude``, ``longitude``, and ``value``. The column type and options are defined by the arguments passed to the ``Column`` constructor. For example, the ``latitude`` column is of type ``Float`` while the ``id`` column is of type ``Integer`` and is also flagged as the primary key for the table.

Engine Object
-------------

Anytime you wish to retrieve data from a persistent store database, you will need to connect to it. In SQLAlchemy, the connection to a database is provided via ``engine`` objects. You can retrieve the SQLAlchemy ``engine`` object for a persistent store database using the ``get_persistent_store_database()`` method of the :term:`app class` provided by the Persistent Store API. The example above shows how the ``get_persistent_store_database()`` function should be used. Provide the name of the persistent store to the function and it will return the ``engine`` object for that store.

.. note::

    Although the full name of the persistent store database follows the app-database naming convention described in `Persistent Store Settings`_, you need only use the name you provided when you created the setting to retrieve the engine using ``get_persistent_store_database()``.

Session Object
--------------

Database queries are issued using SQLAlchemy ``session`` objects. You need to create new session objects each time you perform a new set of queries (i.e.: in each controller). Creating ``session`` objects is done via a ``SessionMaker``. In the example above, the ``SessionMaker`` is created using the ``sessionmaker()`` function provided by SQLAlchemy. The ``SessionMaker`` is bound to the ``engine`` object. This means that anytime a ``session`` is created using that ``SessionMaker`` it will automatically be connected to the database that the ``engine`` provides a connection to. You should create a ``SessionMaker`` for each persistent store that you create. An example of how to use ``session`` and ``SessionMaker`` objects is shown in the `Initialization Function`_ section.

SQLAlchemy ORM is a powerful tool for working with SQL databases. As a primer to SQLAlchemy ORM, we highly recommend you complete the `Object Relational Tutorial <http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html>`_.

Initialization Function
=======================

The code for initializing a persistent store database should be defined in an initialization function. The recommended location for initialization functions is the :file:``init_stores.py`` file that is generated with the scaffold. In most cases, each persistent store should have it's own initialization function. The initialization function makes use of the SQLAlchemy data model to create the tables and load any initial data the database may need. The following example illustrates a typical initialization function for a persistent store database:

::

    from sqlalchemy.orm import sessionmaker
    from .model import Base, StreamGage


    def init_example_db(engine, first_time):
        """
        An example persistent store initializer function
        """
        # Create tables
        Base.metadata.create_all(engine)

        # Initial data
        if first_time:
            # Make session
            SessionMaker = sessionmaker(bind=engine)
            session = SessionMaker()

            # Gage 1
            gage1 = StreamGage(latitude=40.23812952992122,
                               longitude=-111.69585227966309,
                               value=1)

            session.add(gage1)

            # Gage 2
            gage2 = StreamGage(latitude=40.238784729316215,
                               longitude=-111.7101001739502,
                               value=2)

            session.add(gage2)

            session.commit()
            session.close()

Create Tables
-------------

The SQLAlchemy ``Base`` class defined in the data model is used to create the tables. Every class that inherits from the ``Base`` class is tracked by a ``metadata`` object. As the name implies, the ``metadata`` object collects metadata about each table defined by the classes in the data model. This information is used to create the tables when the ``metadata.create_all()`` method is called:

::

    Base.metadata.create_all(engine)

.. note::

    The ``metadata.create_all()`` method requires the ``engine`` object as an argument for connection information.

Initial Data
------------

The initialization functions should also be used to add any initial data to persistent store databases. The ``first_time`` parameter is provided to all initialization functions as an aid to adding initial data. It is a boolean that is ``True`` if the function is being called after the tables have been created for the first time. This is provided as a mechanism for adding initial data only the first time the initialization function is run. Notice the code that adds initial data to the persistent store database in the example above is wrapped in a conditional statement that uses the ``first_time`` parameter.

Example SQLAlchemy Query
------------------------

This initial data code uses an SQLAlchemy data model to add four stream gages to the persistent store database. A new ``session`` object is created using the ``SessionMaker`` that was defined in the model. Creating a new record in the database using SQLAlchemy is achieved by creating a new ``StreamGage`` object and adding it to the ``session`` object using the ``session.add()`` method. The ``session.commit()`` method is called, to persist the new records to the persistent store database. Finally, ``session.close()`` is called to free up the connection to the database.

Managing Persistent Stores
==========================

Persistent store management is handled via the :command:`syncstores` command provided by the Tethys Command Line Interface (Tethys CLI). This command is used to create the persistent stores of apps during installation. It should also be used anytime you make changes to persistent store registration, data models, or initialization functions. For example, after performing the registration, creating the data model, and defining the initialization function in the example above, the :command:`syncstores` command would need to be called from the command line to create the new persistent store:

::

    tethys syncstores my_first_app

This command would create all the non-existent persistent stores that are registered for ``my_first_app`` and run the initialization functions for them. This is the most basic usage of the :command:`syncstores` command. A detailed description of the :command:`syncstores` command can be found in the :doc:`../../tethys_cli` documentation.


Dynamic Persistent Store Provisioning
=====================================

As of Tethys Platform 1.3.0, methods were added to the app class that allow apps to create persistent stores dynamically at run time, list existing persistent stores, and check if a given persistent store exists. See the API documentation below for details.

API Documentation
=================

.. automethod:: tethys_sdk.base.TethysAppBase.persistent_store_settings

.. automethod:: tethys_sdk.base.TethysAppBase.get_persistent_store_connection

.. automethod:: tethys_sdk.base.TethysAppBase.get_persistent_store_database

.. automethod:: tethys_sdk.base.TethysAppBase.list_persistent_store_connections

.. automethod:: tethys_sdk.base.TethysAppBase.list_persistent_store_databases

.. automethod:: tethys_sdk.base.TethysAppBase.persistent_store_exists

.. automethod:: tethys_sdk.base.TethysAppBase.create_persistent_store

.. automethod:: tethys_sdk.base.TethysAppBase.drop_persistent_store
