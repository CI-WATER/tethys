.. _contribute_getting_started:

*******************************
Writing Your First Contribution
*******************************

**Last Updated:** January 2025

Introduction
============

If you are interested in contributing code to Tethys Platform, you have come to the right place. Perhaps you have an idea for a feature that you'd like to implement or there is a bug that you'd like to fix. Being able to contribute is one of the benefits of using open source software. The process can seem daunting at first, so this tutorial has been designed as a step-by-step guide to walk you through the process from start to finish.

Getting Help
============

If you get stuck at any point during this tutorial, don't hesitate to ask for help. The Tethys Platform community is eager and willing to help you succeed. The best way to get help with this tutorial is to post a question under the `Tutorial Help <https://github.com/tethysplatform/tethys/discussions/categories/tutorial-help>`_ category of `Tethys Platform GitHub Discussions <https://github.com/tethysplatform/tethys/discussions>`_. Please include "Writing Your First Contribution Tutorial" in the title of your post to help others know what you are working on.

.. tip::

    See :ref:`contribute_intro_communication` for other common communication mechanisms.

Learn Prerequisites
===================

There are a number of prerequisites that you should be familiar with before you start contributing to Tethys Platform. If any of the topics in this section are unfamiliar to you, the provided links to other resources can help you get up to speed. None of this is required to start contributing, but the more you know about these topics, the easier it will be to contribute.

**Python 3**

The primary programming language used in Tethys Platform is Python 3. The `Learn Python <https://www.learnpython.org/>`_ website is an excellent resource for learning Python. For those who want to go more in-depth, the free e-books `Think Python <http://greenteapress.com/thinkpython2/html/index.html>`_ and `Diving into Python 3 <https://diveintopython3.problemsolving.io/>`_ are great reads.

.. note::

    Make sure to learn Python version 3 syntax and features (preferably 3.8+). Python 2 has not been supported for some time.

**Django**

Tethys Platform *is* a Django web application, composed of multiple Django apps. Many of Django's features are used in Tethys Platform development. As such, it is recommended that you complete the `Writing your first Django app <https://docs.djangoproject.com/en/5.1/intro/tutorial01/>`_ tutorial (Parts 1-8 and the Advanced tutorial) to learn how Django works.

**HTML and CSS**

As a website project, knowing HTML and CSS will come in handy when contributing to Tethys Platform. They are used in Tethys for the frontend development. The `Learn HTML and CSS <https://www.learn-html.org/>`_ website is good resources for learning both HTML and CSS. In addition you should familiarize yourself with `Bootstrap <https://getbootstrap.com/docs/5.1/getting-started/introduction/>`_ which is used in Tethys Platform for layout and responsive development.

**Conda Environments**

Conda is a commandline environment and package manager for Python. It is used in Tethys Platform development to manage dependencies. It is recommended that you install `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ and the `libmamba solver <https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community>`_. Then learn how to create and manage conda environments using the `Getting started with conda guide <https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_.

**Git**

Git is a distributed version control system that is used to manage the source code for Tethys Platform. For this tutorial, you will need to `Download and install Git <https://git-scm.com/downloads>`_. The `Learn Git Branching <https://learngitbranching.js.org/>`_ website illustrates Git concepts visually and is a great resource for learning Git basics.

**JavaScript (Optional)**

JavaScript is an optional prerequisite that is used in Tethys Platform for the frontend development. Learning JavaScript is not required unless you plan to work on the frontend. The `Learn JavaScript <https://www.learn-js.org/>`_ website is a good resource for learning JavaScript.

**SQL (Optional)**

SQL is another optional prerequisite that is used occasionally in Tethys Platform development. Most database interaction is handled by the Django ORM, but there are times when you may need to write raw SQL queries. The `Learn SQL <https://www.learnsqlonline.org/>`_ website is a good resource for learning SQL.

**Code of Conduct and DCO**

A healthy community is important for the success of the project. You will be expected to follow the :ref:`Code of Conduct <contribute_intro_policies>`. In addition, a :ref:`contribute_intro_license` is used to ensure that all contributions are made with the proper permissions. Please review both documents and agree to their terms before contributing.

.. _contribute_getting_started_decide:

Decide What to Contribute
=========================

You don't have to have your own idea to contribute to Tethys Platform. There are many `Issues <https://github.com/tethysplatform/tethys/issues>`_ on GitHub that need attention. Look for issues that are labeled as ``good first issue`` or ``help wanted``. These issues are specifically tagged to help new contributors get started. 

Before you get started working on an issue, post a comment on the issue or assign yourself to it to let others know that you are working on it.

If you have your own idea for a contribution, it is a good idea to discuss it with the community before spending a lot of time on it. This can help you get feedback on your idea and ensure that your contribution is in line with the project's goals. Here are some suggestions to help you decide:

  * Search `Issues <https://github.com/tethysplatform/tethys/issues>`_ and `Discussions <https://github.com/tethysplatform/tethys/discussions>`_ on GitHub to see if your idea has already been discussed/addressed.
  * Write an Issue for what you plan to work on (see: :ref:`contribute_issues_creating`).
  * For more abstract proposals without a clear direction, consider starting a Discussion (see: :ref:`contribute_community_discussions`).

Create a Fork
=============

Create a fork of the ``tethysplatform/tethys`` repository on GitHub. This will create a copy of the repository in your GitHub account that you can make changes to (see: :ref:`contribute_forking`).

Create a Development Environment
================================

Create a development environment for Tethys Platform using these instructions: :ref:`setup_dev_environment` with the following changes:

    * Clone your fork of the repository instead of the main Tethys Platform repository.
    * Configure your development environment for running the tests (see: :ref:`contribute_testing_setup_env`).

Tutorial Issue
==============

For this tutorial you will work on the following issue:

* `#1139: [FEATURE] Add Easter Eggs to the Tethys CLI <https://github.com/tethysplatform/tethys/issues/1139>`_

To get started, read the issue on GitHub and add a comment to let others know that you are working on it.

Create a Feature Branch
=======================

Create a new branch in your fork of the repository to work on the issue. When creating a new branch, it is a good idea to name it something that is related to the issue you are working on. For example, you could name the branch ``feature-1139`` to reference the issue number. In this tutorial you will be adding ASCII art branding to the ``tethys version`` command, so another good name would be something descriptive like ``cli-ascii-art``.

Before creating the feature branch, make sure you are on the ``main`` branch by running ``git status`` command:

.. code-block:: bash

    git status

.. tip::

    Run ``git`` commands from the root of the repository (i.e. the same directory that has the pyproject.toml file).

This should print a message like the following:

.. code-block:: bash

    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean

If you are not on the ``main`` branch, switch to it by running the following command:

.. code-block:: bash

    git checkout main

Then create a new feature branch as follows:

.. code-block:: bash

    git checkout -b cli-ascii-art

Add Dependency
==============

In this tutorial you will be making the output of the ``tethys version`` command more exciting using ASCII art fonts. The third-party `pyfiglet <https://pypi.org/project/pyfiglet/>`_ package will be used to convert the version text as ASCII art font dynamically. Since this is a new dependency for Tethys Platform, you'll need to install it in the Conda environment and add it to the ``environment.yml`` so it gets installed automatically with Tethys Platform.

1. Search to see if ``pyfiglet`` is on the Conda Forge package channel with the following command:

.. code-block::

    conda search conda-forge::pyfiglet

2. Since it is already available on Conda Forge, it can be installed as follows:

.. code-block::

    conda install conda-forge::pyfiglet

.. note::

    If ``pyfiglet`` wasn't on Conda Forge, you would need to add it before the dependency could be added to Tethys Platform. Lucky us.

4. Finally, add ``pyfiglet`` to the :file:`environment.yml` and the :file:`micro_environment.yml` files (for more details on maintaining dependencies in Tethys Platform, see: :ref:`maintain_dependencies`). The "Gen CLI commands" section seems as good as any:

.. code-block:: yaml
    :emphasize-lines: 4

    # Gen CLI commands
    - pyyaml
    - jinja2
    - pyfiglet

.. note::

    A new dependency for a silly feature like this should probably be implemented as an optional dependency, but for simplicity it is added as a required dependency.

Write the Code
==============

With the feature branch created and new dependencies installed, you can begin coding. 

1. Open :file:`tethys_cli/version_command.py` in your favorite text editor or IDE. 

2. Modify the ``add_version_parser()`` function to add a new optional argument to the version command:

.. code-block:: python
    :emphasize-lines: 6-12

    def add_version_parser(subparsers):
        # Setup list command
        version_parser = subparsers.add_parser(
            "version", help="Print the version of tethys_platform"
        )
        version_parser.add_argument(
            "-e", "--exciting",
             help="Print the version of Tethys Platform in a more exciting way.",
            action="store_true",
            dest="exciting",
        )
        version_parser.set_defaults(func=version_command, exciting=False)

..
    The extra space in front of "help=" in the above example is intentional to illustrate linting and formatting later on in the tutorial.

3. Import the ``Figlet`` class from the ``pyfiglet`` package at the top of the file:

.. code-block:: python

    from pyfiglet import Figlet

4. Modify the ``version_command()`` function to use the ``Figlet`` class to print "Tethys Platform" and the version string in ASCII art font if the ``exciting`` option is given:

.. code-block:: python

    def version_command(args):
        if args.exciting:
            f =  Figlet(font='standard', width=300)
            print(f.renderText('Tethys Platform'))
            print(f.renderText(__version__))
        else:
            print(__version__)

..
    The extra space in front of "Figlet" in the above example is intentional to illustrate linting and formatting later on in the tutorial.

4. Manually test the changes by activating your development environment and running the ``tethys version`` command with the new option. You should see "Tethys Platform" in ASCII art letters followed by the version number.

.. code-block:: bash

    tethys version --exciting

5. Which should print something similar to this:

.. code-block::

     _____    _   _                 ____  _       _    __                      
    |_   _|__| |_| |__  _   _ ___  |  _ \| | __ _| |_ / _| ___  _ __ _ __ ___  
      | |/ _ \ __| '_ \| | | / __| | |_) | |/ _` | __| |_ / _ \| '__| '_ ` _ \ 
      | |  __/ |_| | | | |_| \__ \ |  __/| | (_| | |_|  _| (_) | |  | | | | | |
      |_|\___|\__|_| |_|\__, |___/ |_|   |_|\__,_|\__|_|  \___/|_|  |_| |_| |_|
                        |___/                                                  
    
      ___   _      _            _  ___   ___  _                   ___  ____        __  __ _     
     / _ \ / |  __| | _____   _/ |( _ ) / _ \/ |  _    __ _  ___ / _ \| ___|  ___ / _|/ _| |__  
    | | | || | / _` |/ _ \ \ / / |/ _ \| | | | |_| |_ / _` |/ _ \ (_) |___ \ / _ \ |_| |_| '_ \ 
    | |_| || || (_| |  __/\ V /| | (_) | |_| | |_   _| (_| |  __/\__, |___) |  __/  _|  _| |_) |
     \___(_)_(_)__,_|\___| \_/ |_|\___/ \___/|_| |_|  \__, |\___|  /_/|____/ \___|_| |_| |_.__/ 

Run the Test Suite
==================

Run the test suite with the coverage report to check which tests broke and which lines need test coverage:

.. code-block::

    tethys test -cu

This should result in a coverage report similar to the one below. Changes in the code base since this tutorial was written may cause differences in some of the numbers. The important details are the lines that are missing code coverage. You need to write one or more tests to handle the new case when the user provides the ``-e`` or ``--exciting`` options to the ``tethys version`` command.

.. code-block::

    Name                                        Stmts   Miss  Cover   Missing
    -------------------------------------------------------------------------
    tethys_cli/version_command.py                  12      1    92%   25
    -------------------------------------------------------------------------
    TOTAL                                       11201      1    99%

    173 files skipped due to complete coverage.

The astute observer will notice that the line missing coverage is actually one of the original lines and the new lines are reported as covered. This has to do with how the tests were written, which will be looked at more closely in the next section.

If you scroll up on the test output, you'll also notice some of the tests have failed (shown below). This is because the code that was added changed some of the assumptions that were made when the tests were written.

.. code-block::

    ======================================================================
    FAIL: test_add_version_parser (unit_tests.test_tethys_cli.test_version_command.VersionCommandTests.test_add_version_parser)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/path/to/tethys/tests/unit_tests/test_tethys_cli/test_version_command.py", line 22, in test_add_version_parser
        mock_subparsers.add_parser().set_defaults.assert_called_with(
    File "/path/to/miniconda3/envs/tethys431/lib/python3.12/unittest/mock.py", line 949, in assert_called_with
        raise AssertionError(_error_message()) from cause
    AssertionError: expected call not found.
    Expected: set_defaults(func=<function version_command at 0x7fcc28d69e40>)
    Actual: set_defaults(func=<function version_command at 0x7fcc28d69e40>, exciting=False)

    ======================================================================
    FAIL: test_version_command (unit_tests.test_tethys_cli.test_version_command.VersionCommandTests.test_version_command)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "/path/to/miniconda3/envs/tethys431/lib/python3.12/unittest/mock.py", line 1396, in patched
        return func(*newargs, **newkeywargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/path/to/tethys/tests/unit_tests/test_tethys_cli/test_version_command.py", line 32, in test_version_command
        mock_print.assert_called_with(tethys_portal.__version__)
    File "/path/to/miniconda3/envs/tethys431/lib/python3.12/unittest/mock.py", line 949, in assert_called_with
        raise AssertionError(_error_message()) from cause
    AssertionError: expected call not found.
    Expected: print('1.2.3')
    Actual: print("  ___   _      _            _  ___   ___  _                   ___  ____        __  __ _     \n / _ \\ / |  __| | _____   _/ |( _ ) / _ \\/ |  _    __ _  ___ / _ \\| ___|  ___ / _|/ _| |__  \n| | | || | / _` |/ _ \\ \\ / / |/ _ \\| | | | |_| |_ / _` |/ _ \\ (_) |___ \\ / _ \\ |_| |_| '_ \\ \n| |_| || || (_| |  __/\\ V /| | (_) | |_| | |_   _| (_| |  __/\\__, |___) |  __/  _|  _| |_) |\n \\___(_)_(_)__,_|\\___| \\_/ |_|\\___/ \\___/|_| |_|  \\__, |\\___|  /_/|____/ \\___|_| |_| |_.__/ \n                                                  |___/                                     \n")

.. tip::

    For more details on running tests see :ref:`contribute_testing`.

Fix Broken Tests
================

Before adding new tests, fix the failing tests by reviewing each failure one at a time. 

**First Failure**

Look at these lines in the first failure:

.. code-block::

    ======================================================================
    FAIL: test_add_version_parser (unit_tests.test_tethys_cli.test_version_command.VersionCommandTests.test_add_version_parser)
    ----------------------------------------------------------------------
    ...
    AssertionError: expected call not found.
    Expected: set_defaults(func=<function version_command at 0x7fcc28d69e40>)
    Actual: set_defaults(func=<function version_command at 0x7fcc28d69e40>, exciting=False)

The failure was caused by an ``AssertionError`` that was expecting the ``set_defaults()`` function to be called with a single argument (``func``), but instead it received two arguments: it wasn't expecting the new ``exciting`` argument that was added. The test needs to be updated to account for the new ``exciting`` option.

The header of the failure report indicates which test failed as a dot path. Open ``tests/unit_tests/test_tethys_cli/test_version_command.py`` and inspect the ``test_add_version_parser`` function. Notice that a ``MagicMock()`` object is passed to the ``subparser`` argument of the ``add_version_parser()`` call in the test. ``MagicMock`` has a method called ``assert_called_with()`` that is used here to verify that the correct ``subparser`` methods are called with the right arguments to setup the version command properly. For more details on mocking, see :ref:`contribute_testing_mocking`.

Update the ``test_add_version_parser`` function as follows to fix the test:

.. code-block:: python
    :emphasize-lines: 10

    def test_add_version_parser(self):
        mock_subparsers = mock.MagicMock()

        vc.add_version_parser(mock_subparsers)

        mock_subparsers.add_parser.assert_called_with(
            "version", help="Print the version of tethys_platform"
        )
        mock_subparsers.add_parser().set_defaults.assert_called_with(
            func=vc.version_command, exciting=False
        )

Run the tests again to verify that this fixed the test, but run them just for this file to speed up iteration:

.. code-block:: bash

    tethys test -f tests/unit_tests/test_tethys_cli/test_version_command.py

There are only two tests in this file, both of which were failing before. After our fix, only one test is failing now, which is an improvement:

.. code-block:

    Ran 2 tests in 0.074s

    FAILED (failures=1)

**Second Failure**

Look at the following lines of the second failure:

.. code-block::

    ======================================================================
    FAIL: test_version_command (unit_tests.test_tethys_cli.test_version_command.VersionCommandTests.test_version_command)
    ----------------------------------------------------------------------
    ...
    AssertionError: expected call not found.
    Expected: print('1.2.3')
    Actual: print("  ___   _      _            _  ___   ___  _                   ___  ____        __  __ _     \n / _ \\ / |  __| | _____   _/ |( _ ) / _ \\/ |  _    __ _  ___ / _ \\| ___|  ___ / _|/ _| |__  \n| | | || | / _` |/ _ \\ \\ / / |/ _ \\| | | | |_| |_ / _` |/ _ \\ (_) |___ \\ / _ \\ |_| |_| '_ \\ \n| |_| || || (_| |  __/\\ V /| | (_) | |_| | |_   _| (_| |  __/\\__, |___) |  __/  _|  _| |_) |\n \\___(_)_(_)__,_|\\___| \\_/ |_|\\___/ \\___/|_| |_|  \\__, |\\___|  /_/|____/ \\___|_| |_| |_.__/ \n                                                  |___/                                     \n")

The reason for this test failing is not obvious, though there is a clue: it appears that ``print`` was called with a string resembling the ASCII art output.

Examine the ``test_version_command()`` function. In this function a ``MagicMock`` is passed to ``args`` argument of the ``version_command()`` call. Since a value wasn't set for ``mock_args.exciting``, it will return another ``MagicMock``. This is part of the "magic" of ``MagicMock`` objects (see: `Python Docs | The Mock Class <https://docs.python.org/3/library/unittest.mock.html#the-mock-class>`_. This happens to be a truthy value, so execution ends up going down the path it would if ``args.exciting`` was set to ``True``. To restore the test to it's original assumptions, explicitly set ``mock_args.exciting`` to the default value (``False``) to test the default/original behavior:

.. code-block:: python
    :emphasize-lines: 5

    @mock.patch("tethys_cli.version_command.print")
    def test_version_command(self, mock_print):
        from tethys_portal import __version__

        mock_args = mock.MagicMock(exciting=False)
        vc.version_command(mock_args)
        mock_print.assert_called_with(__version__)

Run the tests again on the :file:`test_version_command.py` file to verify that both tests are fixed now (no failures). If you would like, you can also run the full test suite again to get a more accurate coverage report. This time it should show the lines in the ``if args.exciting:`` block as missing coverage:

.. code-block::

    TODO

Write a New Test
================

Add a new test to test the case when the ``exciting`` option is ``True``. Start by making a copy of the ``test_version_command`` function in ``test_version_command.py`` and then rename it to ``test_version_command_exciting``. Set the ``mock_args.exciting`` property to ``True``:

.. code-block:: python

    @mock.patch("tethys_cli.version_command.print")
    def test_version_command_exciting(self, mock_print):
        from tethys_portal import __version__

        mock_args = mock.MagicMock(exciting=True)
        vc.version_command(mock_args)
        mock_print.assert_called_with(__version__)

The ``mock_print.assert_called_with(__version__)`` line is the part of the test that verifies the expected functionality. As it is written, the test won't pass because ``version_command()`` with ``args.exciting`` set to ``True`` outputs the ASCII art version of the Tethys Platform name and version number, not the simple ``__version__`` value. The test needs to be updated with the expected output.

Coming up with the expected output value is not trivial, because the version number part of it is dynamic and will change as the version of Tethys Platform changes. One way to handle this would be to compute the ASCII art version of the output. Another way would be to use ``MagicMock`` on the ``pyfiglet.Figlet().renderText()`` and assert that it was called with the expected values and assert that ``print()`` was called with the expected values. The latter approach will be shown to illustrate how to use ``MagicMock``.

Mock Patching
-------------

First, use the ``mock.patch`` decorator to mock the ``Figlet`` class. This replaces the ``Figlet`` class with a ``MagicMock`` object that can be manipulated for testing purposes. The ``mock.patch`` decorator will pass the ``MagicMock`` object to the test function, so make sure to add a ``mock_Figlet`` argument to the list of arguments for the test function.

.. code-block:: python
    :emphasize-lines: 1, 3

    @mock.patch("tethys_cli.version_command.Figlet")
    @mock.patch("tethys_cli.version_command.print")
    def test_version_command_exciting(self, mock_print, mock_Figlet):
        ...

.. tip::

    Here are a few helpful tips for ``mock.patch``:

    1. Mock arguments should be listed in reverse order of the ``mock.patch`` decorators.
    2. When patching, patch the object where it is used (e.g.: ``tethys_cli.version_command.Figlet``), not where it is defined (e.g.: ``pyfiglet.Figlet``). Another way to think of this is that you are patching the object where it is imported, not where it is defined.

Mock Assertions
---------------

Next, add ``assert_called_with()`` and ``assert_any_call()`` calls for each of the expected calls to the ``Figlet`` class and ``renderText()``:

.. code-block:: python
    :emphasize-lines: 8-10

    @mock.patch("tethys_cli.version_command.Figlet")
    @mock.patch("tethys_cli.version_command.print")
    def test_version_command_exciting(self, mock_print, mock_Figlet):
        from tethys_portal import __version__

        mock_args = mock.MagicMock(exciting=True)
        vc.version_command(mock_args)
        mock_Figlet.assert_called_with(font='standard', width=300)
        mock_Figlet().renderText.assert_any_call('Tethys Platform')
        mock_Figlet().renderText.assert_any_call(__version__)
        mock_print.assert_called_with(__version__)

.. tip::

    The ``assert_called_with()`` method verifies the **last** call on that mock object, while ``assert_any_call()`` verifies **any** of the calls, or in other words that the mock object was called with the expected arguments at least once.

Finally, update the ``mock_print.assert_called_with()`` to verify that it was called with the result of calling ``renderText()`` on the ``Figlet`` object:

.. code-block:: python
    :emphasize-lines: 11

    @mock.patch("tethys_cli.version_command.Figlet")
    @mock.patch("tethys_cli.version_command.print")
    def test_version_command_exciting(self, mock_print, mock_Figlet):
        from tethys_portal import __version__

        mock_args = mock.MagicMock(exciting=True)
        vc.version_command(mock_args)
        mock_Figlet.assert_called_with(font='standard', width=300)
        mock_Figlet().renderText.assert_any_call('Tethys Platform')
        mock_Figlet().renderText.assert_any_call(__version__)
        mock_print.assert_called_with(mock_Figlet().renderText())

.. tip::

    When a mock object is called, it returns another mock object. Each mock object tracks its call path in its ``name`` property. For example, ``mock_Figlet()`` has a ``name`` of ``'Figlet()'`` and ``mock_Figlet().renderText()`` has a ``name`` of ``'Figlet().renderText()'``. The ``assert`` methods consider two mock objects equal if their ``name`` properties are equal.

Run the tests on the :file:`test_version_command.py` file to verify that the new test passes. If it does, run the full test suite to get an updated coverage report. The output should look similar to this:

.. code-block::

    Name    Stmts   Miss  Cover   Missing
    -------------------------------------
    TOTAL   11201      0   100%

Check Code Style
================

Run the linter from the root directory of the repository to ensure that the code adheres to code style requirements (see: :ref:`contribute_testing_linting`):

.. code-block:: bash

    flake8 .

If you copy-and-pasted the code examples above, there should be at least two issues:

.. code-block:: bash

    ./tethys_cli/version_command.py:12:10: E131 continuation line unaligned for hanging indent
    ./tethys_cli/version_command.py:21:12: E222 multiple spaces after operator

The output indicates the file, line number, and column number where the issue is located. Open the file in your text editor and fix the issues. After fixing the issues, run the linter again to verify that the issues have been resolved. There will be no output if the linter doesn't find any issues.

Run Formatter
=============

Run the formatter from the root directory of the repository to ensure that the code is properly formatted (see: :ref:`contribute_testing_linting`):

.. code-block:: bash

    black .

This should output a list of files that were reformatted:

.. code-block:: bash

    reformatted /path/to/tethys/tethys_cli/version_command.py
    reformatted /path/to/tethys/tests/unit_tests/test_tethys_cli/test_version_command.py

    All done! ✨ 🍰 ✨
    2 files reformatted, 480 files left unchanged.

.. tip::

    In practice, it is better to run the formatter before the linter, because the formatter will fix many spacing issues that the linter will complain about. Keep in mind that the formatter is not enforcing PEP 8, so you should still run the linter to catch any issues that the formatter doesn't fix.

Preview Your Changes
====================

Before committing your changes, it is a good idea to preview them to make sure that everything looks good. Run the following command to see the changes that you have made:

.. code-block:: bash

    git diff

Press the :kbd:`Enter` key to scroll through the changes. Press :kbd:`q` to exit the preview. Here is an example of what the output looks like for the :file:`site_settings.py` file:

.. code-block:: diff

    diff --git a/tethys_apps/templatetags/site_settings.py b/tethys_apps/templatetags/site_settings.py
    index b85e315a..decb8b4a 100644
    --- a/tethys_apps/templatetags/site_settings.py
    +++ b/tethys_apps/templatetags/site_settings.py
    @@ -43,7 +43,7 @@ def load_custom_css(var):
        # an OSError will be raised during the file path checks. This could also happen
        # if a lengthy file path is given or is otherwise invalid.
        except OSError as e:
    -        oserror_exception = ": " + str(e)
    +        oserror_exception = str(e)
        else:
            oserror_exception = ""
    +        "-e",
    +        "--exciting",
    +        help="Print the version of Tethys Platform in a more exciting way.",
    +        action="store_true",
    +        dest="exciting",
    +    )
    +    version_parser.set_defaults(func=version_command, exciting=False)
    
    
    def version_command(args):
    -    print(__version__)
    +    if args.exciting:
    +        f = Figlet(font="standard", width=300)
    +        print(f.renderText("Tethys Platform"))
    +        print(f.renderText(__version__))
    +    else:
    +        print(__version__)

Commit and Push Your Changes
============================

Once you are satisfied with your changes, commit them to your feature branch. First stage the changes using the following command:

.. code-block:: bash

    git add .

Use the ``git status`` command to verify that the changes have been staged to the correct branch:

.. code-block:: bash

    git status

This should print a message like the following:

.. code-block:: bash

    On branch cli-ascii-art
    Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
          modified:   environment.yml
          modified:   micro_environment.yml
          modified:   tests/unit_tests/test_tethys_cli/test_version_command.py
          modified:   tethys_cli/version_command.py

Then commit the changes with a descriptive message:

.. code-block:: bash

    git commit -m "Add exciting ASCII art option to the tethys version command"

Then push your changes to your fork on GitHub:

.. code-block:: bash

    git push origin cli-ascii-art

.. tip::

    Many IDEs provide built-in graphical tools for staging, committing, and pushing changes. If you are using an IDE, you can use these tools instead of the command line.

Make a Pull Request
===================

**Please don't do this for the tutorial**, but the next step would be to make a pull request. Review the steps in the :ref:`contribute_pull_request` documentation to learn how you would do this.

Next Steps
==========

Congratulations! You have learned how to make code contributions to Tethys Platform. Here is a list of things that you can do next:

  * Find something to work on and make your first contribution. Review the tips in the :ref:`contribute_getting_started_decide` section.
  * Review the :ref:`contribute_development_process` documentation for a more detailed explanation of the development process.
  * Learn more about the design and implementation of different Tethys Platform features in the :ref:`coding_principles` documentation.

If you decide coding isn't your thing, there are many other ways to contribute to Tethys Platform. Check out the :ref:`contribute_intro_ways` section for more ideas.







