.. _tethys_jobs_condor:

***************
Condor Job Type
***************

**Last Updated:** January 2022

.. important::

    This feature requires the ``condorpy`` library to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install ``condorpy`` using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge condorpy

        # pip
        pip install condorpy


The :doc:`condor_job_type` (and :doc:`condor_workflow_type`) are used to create jobs to be run by a pool of cluster resources managed by HTCondor. HTCondor makes it possible for jobs to be offloaded from the main web server to a scalable computing cluster, which in turn enables very large scale jobs to be processed.

.. seealso::

    The Condor Job and the Condor Workflow job types use the CondorPy library to submit jobs to HTCondor compute pools. For more information on CondorPy and HTCondor see the `CondorPy documentation <http://condorpy.readthedocs.org/en/latest/>`_ and specifically the `Overview of HTCondor <http://condorpy.readthedocs.org/en/latest/htcondor.html>`_.


Creating a Condor Job
=====================

To create a job call the ``create_job`` method on the job manager. The required parameters are ``name``, ``user`` and ``job_type``. Any other job attributes can also be passed in as `kwargs`.

.. code-block::

    from tethys_sdk.routing import controller
    from .app import App

    job_manager = App.get_job_manager()

    @controller(
        app_workspace=True,
    )
    def some_controller(request, app_workspace):
        # create a new job from the job manager
        job = job_manager.create_job(
            name='myjob_{id}',  # required
            user=request.user,  # required
            job_type='CONDOR',  # required

            # any other properties can be passed in as kwargs
            attributes=dict(
                transfer_input_files=('../input_1', '../input_2'),
                transfer_output_files=('example_output1', example_output2),
            ),
            condorpy_template_name='vanilla_transfer_files',
            remote_input_files=(
                os.path.join(app_workspace, 'my_script.py'),
                os.path.join(app_workspace, 'input_1'),
                os.path.join(app_workspace, 'input_2')
            )
        )

        # properties can also be added after the job is created
        job.extended_properties = {'one': 1, 'two': 2}

        # each job type may provided methods to further specify the job
        job.set_attribute('executable', 'my_script.py')

        # get a scheduler for the job
        job.scheduler = app.get_scheduler('condor_primary')

        # save or execute the job
        job.save()
        # or
        job.execute()

Before a controller returns a response the job must be saved, otherwise, all of the changes made to the job will be lost (executing the job automatically saves it). If submitting the job takes a long time (e.g. if a large amount of data has to be uploaded to a remote scheduler) then it may be best to use AJAX to call the controller that executes the job.

API Documentation
=================

.. autoclass:: tethys_compute.models.CondorJob
