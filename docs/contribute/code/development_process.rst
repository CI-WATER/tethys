.. _contribute_development_process:

*******************
Development Process
*******************

**Last Updated:** January 2025

.. _contribute_github_flow:

GitHub Flow
===========

Tethys Platform uses the `GitHub Flow <https://docs.github.com/en/get-started/using-github/github-flow>`_ workflow for managing code contributions. GitHub Flow is a branch-based workflow that allows many developers to work on the same codebase simultaneously. It leverages the features of Git version control system and GitHub to provide a simple and flexible workflow, allowing developers to collaborate and make changes to the codebase efficiently. 

.. _contribute_github_flow_summary:

Here is a summary of the GitHub Flow process:

0. :ref:`contribute_install_git`: Install Git on your local machine (first time only).
1. :ref:`contribute_forking`: Create a fork of the Tethys Platform repository under your GitHub account.
2. :ref:`contribute_clone_fork`: Clone your fork to your local machine to make changes.
3. :ref:`contribute_feature_branch`: Create a new branch from the `main` branch to work on your changes.
4. :ref:`contribute_make_changes`: Make your changes on the feature branch, following the project's coding standards and best practices.
5. :ref:`contribute_pull_request`: Push your branch to GitHub and open a Pull Request to merge your changes into the `main` branch.
6. :ref:`contribute_code_review`: Have your changes reviewed by other contributors to ensure they meet the project's standards.
7. :ref:`contribute_checks`: Ensure that your changes pass all automated checks, such as code style, testing, and documentation.
8. :ref:`contribute_merge`: Once the Pull Request has been approved, merge your changes back into the `main` branch.

.. _contribute_install_git:

Install Git
===========

To contribute to Tethys Platform, you will need to have `Git <https://git-scm.com/>`_ installed on your local machine. Git is a distributed version control system that allows you to track changes in your codebase, collaborate with others, and manage your code history. You can download Git from the `official website <https://git-scm.com/downloads>`_ and follow the installation instructions for your operating system.

.. _contribute_forking:

Create a Fork
=============

Most GitHub repositories, including Tethys Platform, restrict who can push changes directly to the repository. However, anyone can still contribute changes to Tethys Platform by creating a `Fork <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`_ of the repository. A fork is a copy of the repository under your GitHub account, allowing you to make and push changes to it.

To create a fork:

1. Navigate to the `Tethys Platform repository on GitHub <https://github.com/tethysplatform/tethys>`_
2. Click the **Fork** button in the top right corner.
3. Select your GitHub account as the **Owner**.
4. Update the repository name and description if desired.
5. Keep the **Copy the ``main`` branch only** option checked on.
6. Click **Create Fork** to create the fork.

This will create a copy of the repository under your account, which will allow you to make new branches and push changes.

If you already have a fork of the repository, ensure that it is up-to-date with the main repository before making changes. You can do this by syncing your fork with the main repository using the following steps:

1. Navigate to your fork of the repository on GitHub.
2. Click on the **Sync fork** button to update your fork with the latest changes from the main repository.

This will ensure that your fork contains the latest changes from the main repository, reducing the likelihood of merge conflicts when submitting a Pull Request.

.. _contribute_clone_fork:

Clone your Fork
===============

1. Navigate to your fork of the repository on GitHub.
2. Click on the **Code** button.
3. Select **HTTPS** or **SSH** from the dropdown menu as the clone method.
4. Copy the URL provided.
5. Open a terminal on your local machine and run:

.. code-block:: bash

    git clone <COPIED_URL>

.. note::

   The **SSH** option requires you to have set up SSH keys on your computer and to have uploaded the public key to your GitHub account. To learn more, see: `Connecting to GitHub with SSH <https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_.

.. _contribute_feature_branch:

Create a Feature Branch
=======================

The process begins with creating a new branch from the `main` branch, often referred to as a "feature branch". This branch is where you will make your changes, whether it's adding a new feature, fixing a bug, or updating documentation. Naming the branch descriptively helps others understand the purpose of the changes. Examples of good feature branch names include: `add-user-authentication`, `fix-404-error`, or `issue-987`.

.. _contribute_make_changes:

Make Changes
============

Once you have created a feature branch, you can start making your changes. This may involve adding new code, modifying existing code, fixing bugs, writing tests and/or updating documentation. It's important to follow the project's coding standards, best practices, and documentation guidelines to ensure that your changes are consistent with the rest of the codebase. Refer to the :ref:`contribute_checks` section below for a list of specific requirements. This helps maintain a clean and organized codebase and makes it easier for others to understand and contribute to the project.

See the :ref:`contribute_documentation` and :ref:`contribute_testing` sections for more information on writing documentation and tests, respectively.

.. _contribute_pull_request:

Open a Pull Request
===================

Once your changes are complete, you should push the branch to GitHub and open a `Pull Request (PR) <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests>`_. A Pull Request allows others to review your changes, discuss potential improvements, and ensure that the code meets the project's standards. It's also an opportunity to run automated tests to catch any issues before merging. 

.. _contribute_create_pull_request:

Create a Pull Request
---------------------

To create a pull request do the following:

1. Navigate to either `tethysplatform/tethys <https://github.com/tethysplatform/tethys>`_ or your fork of it on GitHub.
2. Select the **Pull requests** tab.
3. Click the **New pull request** button.
4. Select ``tethysplatform/tethys`` as the **base repository**
5. Select ``main`` as the **base branch**.
6. Select the repository where your feature branch is located as the **head repository**.
7. Select the feature branch as the **compare branch**.
8. Review the list of commits and changes to make sure everything looks good.
9. Click the **Create pull request** button.
10. Fill out the Pull Request template with the necessary information (see below).
11. Click the **Create pull request** button to submit the Pull Request.

Title and Description
---------------------

When creating a Pull Request, it's important to include a clear and concise title and description of the changes, including the motivation behind the changes, any relevant context, and any potential side effects. This helps reviewers understand the purpose of the changes and provide meaningful feedback. You should also `reference related Issues, Pull Requests, or Discussions <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls#issues-and-pull-requests>`_ in the description to provide additional context. A template has been provided to help guide you through the process.

Assignees
---------

Select yourself and other contributors that worked on the changes under **Assignees**.

.. _contribute_pull_request_labels:

Labels
------

Assign at least one of the following `Labels <https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels>`_. These labels are used to group and summarize the changes in the release notes when a new version of Tethys Platform is released.

* `experimental` - For experimental features or changes that are not yet stable.
* `enhancement` - For improvements to existing features.
* `minor feature` - For small feature additions.
* `major feature` - For significant new features or changes.
* `bugfix` - For bug fixes or issues that need to be resolved.
* `docs` - For documentation updates.
* `security` - For security-related changes or updates.

.. _contribute_code_review:

Code Review
===========

Once the Pull Request has been opened, it will be reviewed by other one or more of the project maintainers as per the requirements in the `Project By-Laws <https://www.tethysplatform.org/project-steering-committee>`_. Code reviews are an essential part of the development process, providing an opportunity to ensure that the code meets the project's standards, follows best practices, and is well-documented. Reviewers will provide feedback, suggest improvements, and ask questions to help improve the quality of the code. Please respond to the feedback in a timely manner and make any necessary changes to address the comments.

Code reviewers should follow these guide lines when providing feedback on Pull Requests:

  1. **Be Respectful and Inclusive**: Ensure your feedback is respectful and inclusive. Acknowledge the effort put into the changes and encourage a positive and collaborative atmosphere.

  2. **Be Constructive**: Provide feedback that is helpful and aimed at improving the code. Avoid personal comments that target the author and focus on the code itself.

  3. **Provide Specific Feedback**: Offer clear and specific feedback. Add comments to exact lines of code that need improvement and explain why. Provide examples or code suggestions when possible.

  4. **Ask Questions**: If something is unclear, ask questions to gain a better understanding of the changes. This can help clarify ambiguities and ensure that the code meets the project's requirements.

  5. **Consider the Context**: Take into account the context of the changes, the project's goals, and the needs of the users. Ensure that the changes align with the overall direction of the project.

  6. **Check for Consistency**: Ensure that the code follows the project's coding style standards and is constistent with the surrounding code. Consistent code is easier to read, maintain, and reduces the likelihood of errors.

  7. **Test the Changes**: If possible, test the changes locally to verify that they work as expected. Look for any potential issues or edge cases that may not have been considered.

  8. **Check for Tests and Documentation**: Most changes should include tests to verify the functionality and documentation to explain how to use the new feature or fix. Ensure that the tests are comprehensive and the documentation is clear and accurate.

  9. **Be Timely**: Provide feedback in a timely manner to keep the development process moving forward. Delays in code reviews can slow down the entire project.

.. _contribute_checks:

Checks
======

Tethys Platform makes use of GitHub Actions to automate various checks on Pull Requests. These checks help ensure that the code meets the project's standards, is well-tested, and is properly documented. When opening a Pull Request, the following checks will be run automatically:

Code Style
----------

The code style check ensures that the code follows the project's coding standards and best practices. This includes formatting, naming conventions, and code structure. The code style check helps maintain consistency across the codebase and makes the code easier to read and maintain. The following code style checks are run:

* **Formatting** - `Black <https://black.readthedocs.io/en/stable/>`_ is a code formatter that automatically formats the code to adhere to the project's coding standards. If running Black identifies any format changes that need to be made, the check will fail.

* **Linting** - The `Flake8 <https://flake8.pycqa.org/en/latest/>`_ linter is used to verify the code style conforms to Python best practices. If Flake8 identifies any code style issues, referred to as "lint", the check will fail.

Testing and Coverage
--------------------

The tests suite will be run every time a new pull request is made or new changes are pushed to an branch associated with an open pull request. In addition, a coverage tool is used to analyze the code coverage of the tests. The coverage tool will generate a report that shows which parts of the code are covered by the tests and which parts are not. The following checks are run:

* **Python Tests** - The Python test suite is run run once for each combination of supported Python version x Django version x operating system to ensure compatibility across different environments. If any of the Python tests fail, this check will fail.

* **Python Test Coverage** - The `coverage <https://coverage.readthedocs.io/en/6.0.1/>`_ tool is used to measure the code coverage of the tests and then it is published to `Coveralls <https://coveralls.io/github/tethysplatform/tethys>`_. This check will fail if the code coverage reports less than 100% test coverage on Python code.

Docker Build and Start-up Test
------------------------------

The Docker build check ensures that the Docker image can be built successfully. Upon successful build, the image is run to verify that it will start up with out issue. These checks helps ensure that the Docker image can be deployed and run without issues. The following checks are run:

* **Docker Build** - The Docker image is built using the Dockerfile in the repository. It is built once for each combination of supported Python version x Django version. If the build fails, this check will fail.
* **Docker Start-up Test** - Each Docker image built is run to verify that it starts up successfully. If any of the Salt steps fail during start-up, this check will fail.

Condor Build
------------

The Condor build check ensures that the Condor package can be built successfully. The following checks are run:

* **Condor Build** - The Conda package is built using a Conda recipe that is automatically generated. If the build fails, this check will fail.

Docs Build
----------

The docs build check ensures that the documentation can be built successfully. The updated documentation can be previewed on Read the Docs by clicking on the link on the check. The following checks are run:

* **Docs Build** - The documentation is built using `Sphinx <https://www.sphinx-doc.org/en/master/>`_. If the build fails, this check will fail.

.. _contribute_merge:

Merge into `main` Branch
========================

After the Pull Request has been reviewed and approved, it can be merged into the `main` branch. This ensures that the main branch always contains stable and tested code. Following the merge, the feature branch *should be deleted*, and the process can start again for the next set of changes. This iterative approach helps maintain a clean and organized codebase while facilitating continuous integration and delivery.
