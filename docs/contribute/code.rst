.. _contribute_code:

*****************
Contributing Code
*****************

**Last Updated:** December 2024

Getting Started Tutorial
========================

Use this step-by-step guide to to guide you through the process of contributing to the Tethys Platform. It covers essential topics and initial steps to get you up and running quickly.

.. toctree::
   :maxdepth: 1

   getting_started

Setup Development Environment
=============================

Use these instructions to setup a new development environment for modifying Tethys Platform. It includes steps for cloning the repository, installing dependencies, and configuring the development environment. It also describes how to use the installation script to automate Tethys Platform development installations.

.. toctree::
   :maxdepth: 1

   dev_environment

Development Process
===================

This section describes the development process used for managing code contributions to Tethys Platform. It provides a a high-level description on common development activities like creating a fork of the repository, making changes on a feature branch, and submitting a pull request for review.

.. toctree::
   :maxdepth: 1

   development_process

Managing Issues
===============

This section explains how Issues are used to track bugs, feature requests, and other tasks for the Tethys Platform, and how they facilitate discussion, planning, and task assignment. It also highlights the need to reference relevant issues in pull requests and the importance of labeling issues for better categorization and prioritization.

.. toctree::
   :maxdepth: 1

   issues

Coding Principles
=================

This section provides high-level explanations of the design, implementation, and motivations of various parts of Tethys Platform. It best used as a primer for understanding specific areas of the code you plan to work on. For instance, if you are interested in adding a new backend for the Tethys Jobs API, you should review the Tethys Jobs documentation to learn how the current backends are implemented.

.. toctree::
   :maxdepth: 2

   coding_principles

Maintain Dependencies
=====================

This section provides instructions on managing and updating project dependencies. It includes information on maintaining Tethys maintained dependencies, like Tethys Dataset Services, updating Tethys to be compatible with new versions of third-party dependencies, and maintaining the Conda-Forge packages for third-party dependencies.

.. toctree::
   :maxdepth: 1

   dependencies

Deploying New Versions
======================

This section describes the process of releasing new versions of the Tethys Platform. It includes steps for updating version numbers, preparing the documentation for a new version, and ensuring that all necessary components are properly built and deployed.

.. toctree::
   :maxdepth: 1

   deploying_tethys
