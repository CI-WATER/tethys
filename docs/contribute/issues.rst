.. _contribute_maintaining_issues:

******************
Maintaining Issues
******************

**Last Updated:** January 2025

`GitHub Issues <https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues>`_ are an important tool for managing the development work in Tethys Platform. They are used to track bugs, feature requests, and other tasks related to the project (see: https://github.com/tethysplatform/tethys/issues). Issues are used to discuss, plan, and coordinate work, assign tasks to contributors, and track progress.

.. note::

    Don't confuse Issues with Discussions. Issues are used to track tasks and bugs, while Discussions are used for general conversations, questions, and technical support. For more on how Discussions are used in Tethys Platform, see :ref:`contribute_community_discussions`.

.. _contribute_issues_creating:

Creating Issues
===============

When you encounter a bug, have an idea for a new feature, or want to suggest an improvement, you can create a new Issue on the Tethys Platform GitHub repository. When creating a new Issue, it's important to provide a clear and detailed description of the problem or feature, including any relevant context, steps to reproduce, and potential solutions. We have provided templates for different types of issues with prompts to help you provide the necessary information.

To create a new Issue follow these steps:

1. Go to the `Issues <https://github.com/tethysplatform/tethys/issues>`_ tab on the Tethys Platform GitHub repository.
2. Click on the **New Issue** button.
3. Press the **Get Started** button next to the appropriate template for the type of Issue you want to create.
4. Add a descriptive title and fill in the Issue template with the necessary information.
5. Assign yourself as an Assignee if you plan to work on it yourself (see :ref:`contribute_issues_assigning`).
6. Add appropriate labels to categorize the Issue (see :ref:`contribute_issues_labels`).
7. Click the **Submit new issue** button to create the Issue.

.. _contribute_issues_referencing:

Referencing in Pull Requests
============================

When working on a new feature or fixing a bug, it's important to `reference <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls#issues-and-pull-requests>`_ the relevant Issue in your Pull Request. This helps maintain context and provides a link between the code changes and the issue being addressed. When creating a Pull Request, you can reference an issue by including the issue number in the Pull Request description or title. 

For example, if you are fixing a bug related to Issue #123, you can include "Fixes #123" in the Pull Request description. This will automatically link the Pull Request to the issue and close it once the Pull Request is merged. We also recommend naming the feature branch something like `issue-123` to help track the relationship between the issue and the branch.

.. _contribute_issues_labels:

Labeling Issues
===============

When creating a new issue, it's important to label it appropriately to help categorize and prioritize work. Labels help contributors identify issues that match their skills and interests and help maintainers prioritize and assign work. As a minimum, each issue should have one of the following labels:

* ``bug`` - For bugs or issues that need to be fixed.
* ``feature request`` - For new feature or enhancement proposals.
* ``docs`` - For issues related to documentation updates.
* ``maintain dependencies`` - For issues related to updating dependencies.
* ``continuous integration`` - For issues related to the continuous integration process.

In addition consider adding one of the following labels as a tip for contributors looking for their next task:

* ``help wanted`` - For issues that need help from the community.
* ``good first issue`` - For issues that are suitable for first-time contributors.

.. _contribute_issues_assigning:

Assigning Issues
================

When creating a new issue, consider assigning it to a contributor or maintainer who you think would be best to address the issue. If you plan to work on an issue, you can assign it to yourself to indicate that you are taking responsibility for it. It is ok to leave the issue unassigned if you are unsure who should work on it. Many assignments are made when issues are reviewed during the weekly scrum meeting.

.. _contribute_issues_commenting:

Commenting on Issues
====================

When working on an issue, it's important to provide regular updates and communicate with other contributors. This can include sharing progress, asking for feedback, or discussing potential solutions. Commenting on issues facilitates collaboration and provides important documentation for the future when investigating bugs or expanding on a feature. It's also an opportunity to ask questions, provide guidance, and share knowledge with other contributors. As with all communication on GitHub, it's important to be respectful, constructive, and inclusive in your comments (see: :ref:`contribute_intro_policies`).

.. _contribute_issues_closing:

Closing Issues
==============

Once an issue has been resolved, it should be closed to indicate that the work is complete. This helps maintainers track the progress of the project and identify which issues are still open and need attention. When closing an issue, it's important to include a brief description of the resolution, any relevant context, and any potential side effects. This helps maintainers understand the changes and provides valuable information for future reference. You can also reference related Pull Requests, Issues, or Discussions in the closing comment to provide additional context.

.. _contribute_issues_milestones:

Adding to Milestones
====================

`Milestones <https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones>`_ are used to group related issues and Pull Requests together and track progress towards a specific goal, usually a specific release. Each milestone represents a set of tasks that need to be completed within a specific timeframe, such as a release cycle. Milestones help maintainers prioritize work, assign tasks to contributors, and track progress towards project goals. They are also used to group and summarize the changes in the release notes when a new version of Tethys Platform is released.

When creating a new issue or Pull Request, consider assigning it to a milestone to indicate which release or sprint it belongs to. This helps maintainers track progress, prioritize work, and plan future releases. If you are unsure which milestone to assign an issue or Pull Request to, you can leave it unassigned, and it can be reviewed and assigned during the weekly scrum meeting.

.. _contribute_issues_security:

Security Vulnerabilities
========================

If you discover a security vulnerability in Tethys Platform, please report it responsibly. Do not report security vulnerabilities as normal issues on GitHub, as this can expose the vulnerability to malicious actors. Instead, use `GitHub's Security Advisories <https://docs.github.com/en/code-security/security-advisories>`_ feature to report security vulnerabilities privately to the Tethys Platform maintainers. This feature allows you to report security vulnerabilities confidentially and securely, ensuring that the vulnerability is addressed promptly and responsibly.
