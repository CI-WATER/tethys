.. _contribute_testing:

*******
Testing
*******

**Last Updated:** January 2025


.. _contribute_testing_setup_env:

Setup Testing Environment
=========================

The Tethys Platform test suite requires a PostgreSQL database and Tethys must be configured with a database user that has superuser privileges so that it can create and delete the test database automatically. The following steps will guide you through setting up a testing environment for Tethys Platform:

1. Setup a development installation of Tethys Platform by following the :ref:`setup_dev_environment` tutorial.
2. Be sure to set up your development environment to :ref:`setup_dev_environment_postgis`.
3. Configure Tethys Platform to use the ``tethys_super`` user for the database connection by editing the :file:`portal_config.yml`:

    .. code-block:: yaml

        settings:
          DATABASES:
            default:
                ENGINE: django.db.backends.postgresql
                NAME: tethys_platform
                USER: tethys_super
                PASSWORD: pass
                HOST: localhost
                PORT: <DB_PORT>

Your development environment should be ready for running the test suite.

.. _contribute_testing_running_tests:

Running Tests
=============

When you are developing, you will need to write tests and run them locally to verify that they work. At the time of writing, Tethys Platform only had unit tests for its Python code. To run the entire Python unit test suite, use the following command:

.. code-block:: bash

    tethys test -u

The ``-u`` flag selects the Unit test suite to run, which is currently the only test suite that is maintained. Running the entire suite can take a long time, so you may want to run a subset of the tests. Use the ``-f`` flag to run a specific test file or directory, giving it the path relative to the CWD directory or the absolute path. For example, to run the tests for the ``harvester.py`` file from the repository root directory, you could use the following command:

.. code-block:: bash

    tethys test -f tests/unit_tests/test_tethys_apps/test_harvester.py

.. _contribute_testing_test_results:

Test Results
------------

The output from the test command should look similar to this when all of the tests have passed:

.. code-block:: bash

    Test App not found. Installing.....
    Test Extension not found. Installing.....

    Found 2044 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .....................................................................
    .....................................................................
    .....................................................................
    ..........................................
    ----------------------------------------------------------------------
    Ran 2044 tests in 367.599s

    OK
    Destroying test database for alias 'default'...

If any tests fail, the output will indicate which tests failed and why. You can use this information to debug the issue and fix the tests:

.. code-block:: bash

    Test App not found. Installing.....
    Test Extension not found. Installing.....

    Found 2044 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ............F........................................................
    .....................................................................
    .....................................................................
    ..........................................
    ======================================================================
    FAIL: test_add_settings (tests.unit_tests.test_tethys_apps.test_models.test_TethysApp.TethysAppTests)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/username/tethys/tests/unit_tests/test_tethys_apps/test_models/test_TethysApp.py", line 23, in test_add_settings
        self.assertEqual(1, len(settings))
    AssertionError: 1 != 0

    ----------------------------------------------------------------------
    Ran 2044 tests in 367.599s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

.. _contribute_testing_coverage:

Code Coverage
-------------

Tethys Platform requires 100% test coverage for all new code. This means that every line of code is passed over at least once during the running of the tests suite. To check the test coverage locally, you can the ``-c`` flag when running the tests:

.. code-block:: bash

    tethys test -cu

This will add a coverage report to the end of the test output. The coverage report will indicate which files and which lines in the files are missing coverage, if any:

.. code-block:: bash

    Name                    Stmts   Miss  Cover   Missing
    -----------------------------------------------------
    tethys_apps/models.py     525      2    99%   81, 110
    -----------------------------------------------------
    TOTAL                   11177      2    99%

    173 files skipped due to complete coverage.

.. _contribute_testing_linting:

Code Style
==========

The Python code in Tethys Platform is developed following the `PEP8 style guide <https://peps.python.org/pep-0008/>`_. The code is linted using flake8 and formatted using the Black code formatter.

flake8
------

Tethys Platform uses the flake8 linter to check for conformance to the PEP8 style guide and other Python codestyle best practices. To run the linter, run the following command in the root of the Tethys Platform repository:

.. code-block:: bash

    flake8

This is an example of the output you might see when running flake8:

.. code-block:: bash

    ./tests/unit_tests/test_tethys_layouts/test_mixins/test_map_layout.py:1373:17: B041 Repeated key-value pair in dictionary literal.
    ./tethys_apps/models.py:1263:2: E999 TabError: inconsistent use of tabs and spaces in indentation

**If no output is displayed, the check passed and there are no issues.** No news is good news. If any issues are found, they will be listed in the output. Most are self explanatory, but a quick web search referencing the issue code will usually provide more information on the issue and how to resolve it. For more information on flake8, see the `flake8 documentation <https://flake8.pycqa.org/en/latest/>`_.

Black
-----

Within the PEP8 style guide, there is a lot of room for interpretation for how code can be formatted. This can lead to inconsistencies in code style across a large codebase. To help maintain a consistent code style, Tethys Platform uses the Black code formatter. Using a formatter like Black can help reduce the time spent on code reviews by minimizing the diffs and preventing tiffs over how a block of code should be styled.

You will most frequently encounter the need to run the Black formatter after the Black check fails on a Pull Request you have opened. Fixing the failure is simple: run Black on the codebase, then commit and push the changes. To format the code using Black, run the following command in the root of the Tethys Platform repository:

.. code-block:: bash

    black .

This is an example of the output you might see when running Black:

.. code-block:: bash

    All done! ✨ 🍰 ✨
    483 files left unchanged.

To learn more about the Black code formatter, see the `Black documentation <https://black.readthedocs.io/en/stable/>`_.

.. _contribute_testing_writing_tests:

Writing Tests
=============

Whether you are adding a new feature or fixing a bug, you should write tests to verify that the code works as expected. This may involve updating existing tests or writing new ones. The following sections provide guidance on writing tests for Python and JavaScript code.

Python Unit Tests
-----------------

The Python tests are written using the `unittest <https://docs.python.org/3/library/unittest.html>`_ framework and 


Organization
++++++++++++

The Python tests are located in the :file:`tests` directory at the root of the repository. The tests are organized into subdirectories based on the module they are testing. For example, tests for the ``tethys_apps.harvester`` module are located in the :file:`tests/unit_tests/test_tethys_apps/test_harvester.py` file. This pattern is used to make finding tests easier and should be followed when adding new test files.

.. _contribute_testing_mocking:

Mocking
+++++++

As unit tests, the Python tests should be focused on testing the smallest units of code possible. This means that you should mock out any external service dependencies that are not the focus of the test such as GeoServer or HTCondor. When the tests are run during the GitHub action checks, these services won't be available. The exception to this is the primary Tethys Platform database, which may be used in tests and will be available for checks (see below).

The `unittest.mock <https://docs.python.org/3/library/unittest.mock.html>`_ module is used to create mock objects in place of services or third-party library objects. The mock objects can be used to simulate the behavior of the real objects and control the return values of methods. For example, to mock the ``requests.get`` function, you could use the following code:

.. code-block:: python

    from unittest.mock import patch

    @patch('some_module.that_uses.requests.get')
    def test_my_function(mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        result = my_function()

        assert result == 'value'

There are many tutorials and guides available online that can help you learn how to use the ``unittest.mock`` module effectively, so it won't be covered in detail here. There are also many examples in the 2000+ existing tests in the Tethys Platform codebase that you can use as a reference.

Database
++++++++

Some tests need to interact with the database to verify that the code is working as expected. Most often this is the case when the code makes uses of one of the many Django ORM models (e.g. tethys_apps.models). Tests that interact with the database should use the ``TethysTestCase``, which inherits from the Django ``TestCase`` class. This class is able to use the test database that is created for tests. It also provides special setup and tear down functionality that ensures that the tests are isolated from each other and that the database is in a known state when the test starts.

Consider this example from :file:`tests/unit_tests/test_tethys_apps/test_models/test_TethysApp.py`:

.. code-block:: python

    from tethys_sdk.testing import TethysTestCase
    from tethys_apps.models import (
        TethysApp,
        TethysAppSetting,
    )

    class TethysAppTests(TethysTestCase):
        def set_up(self):
            self.test_app = TethysApp.objects.get(package="test_app")

        def tear_down(self):
            self.test_app.delete()

        def test_add_settings(self):
            new_setting = TethysAppSetting(name="new_setting", required=False)

            self.test_app.add_settings([new_setting])

            app = TethysApp.objects.get(package="test_app")
            settings = app.settings_set.filter(name="new_setting")
            self.assertEqual(1, len(settings))

The ``test_add_settings`` method tests the ``add_settings`` method of the ``TethysApp`` Django model. The test creates a new ``TethysAppSetting``, adds it to the app, and then verifies that the setting was added to the database. The test uses the ``TethysTestCase`` class to ensure that the test database is available for the test.

There are many examples of tests that interact with the database that can be found with a project-wide search for ``TethysTestCase``.

JavaScript Unit Tests
---------------------

Coming Soon
