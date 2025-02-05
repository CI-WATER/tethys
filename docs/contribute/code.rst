.. _contribute_code:

*****************
Contributing Code
*****************

**Last Updated:** December 2024

Getting Started Tutorial
========================

Use this step-by-step guide to guide you through the process of contributing to the Tethys Platform. It covers essential topics and initial steps to get you up and running quickly.

.. toctree::
   :maxdepth: 1

   code/getting_started

Setup Development Environment
=============================

Use these instructions to setup a new development environment for modifying Tethys Platform. It includes steps for cloning the repository, installing dependencies, and configuring the development environment. It also describes how to use the installation script to automate Tethys Platform development installations.

.. toctree::
   :maxdepth: 1

   code/dev_environment

Development Process
===================

Learn about the development process used for managing code contributions to Tethys Platform. This guide provides a high-level description of common development activities like creating a fork of the repository, making changes on a feature branch, and submitting a pull request for review.

.. toctree::
   :maxdepth: 1

   code/development_process

Docker Development
==================

Help us improve the Docker image for Tethys Platform. This guide includes information on how to build the Docker image, run the Docker container, and how to contribute to the Docker image.

.. toctree::
   :maxdepth: 1

   code/docker
   ../installation/production/docker/tethys_docker_reference

Writing Tests
=============

Understand the importance of writing tests for Tethys Platform and how to write tests for new features and bug fixes. This guide includes information on the different types of tests used in Tethys Platform, how to run tests, and how to write tests for new features.

.. toctree::
   :maxdepth: 1

   code/testing

Continuous Integration and Automation
=====================================

Learn about the continuous integration and automation tools used to test and deploy Tethys Platform. This guide includes information on the continuous integration services used by Tethys Platform and how to configure and maintain them.

.. toctree::
   :maxdepth: 1

   code/continuous_integration

Managing Issues
===============

Understand how Issues are used to track bugs, feature requests, and other tasks for Tethys Platform, and how they facilitate discussion, planning, and task assignment. This guide highlights the need to reference relevant issues in pull requests and the importance of labeling issues for better categorization and prioritization.

.. toctree::
   :maxdepth: 1

   code/issues

Coding Principles
=================

Learn the high-level explanations of the design, implementation, and motivations of various parts of Tethys Platform. This guide is best used as a primer for understanding specific areas of the code you plan to work on. For instance, if you are interested in adding a new backend for the Tethys Jobs API, you should review the Tethys Jobs documentation to learn how the current backends are implemented.

.. toctree::
   :maxdepth: 2

   code/coding_principles

Maintain Dependencies
=====================

Learn how to update and manage third party dependencies of Tethys Platform. This guide includes information on maintaining Tethys maintained dependencies, like Tethys Dataset Services, updating Tethys to be compatible with new versions of third-party dependencies, and maintaining the Conda-Forge packages for third-party dependencies.

.. toctree::
   :maxdepth: 1

   code/dependencies

Deploying New Versions
======================

Learn the process of releasing new versions of the Tethys Platform. This guide includes steps for updating version numbers, preparing the documentation for a new version, and ensuring that all necessary components are properly built and deployed.

.. toctree::
   :maxdepth: 1

   code/deploying_tethys
