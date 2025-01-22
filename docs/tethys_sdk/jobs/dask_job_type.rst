.. _tethys_job_dask:

*************
Dask Job Type
*************

**Last Updated:** January 2022

.. important::

    This feature requires the ``dask`` and ``tethys_dask_scheduler`` libraries to be installed. Starting with Tethys 5.0 or if you are using ``micro-tethys-platform``, you will need to install these libraries using conda or pip as follows:

    .. code-block:: bash

        # conda: conda-forge channel strongly recommended
        conda install -c conda-forge dask tethys_dask_scheduler

        # pip
        pip install dask tethys_dask_scheduler

A Dask Job Type wraps Dask functionality in a Tethys Jobs interface. The Tethys Dask Job type supports two different Dask APIs for creating Dask Tasks: ``dask.delayed`` and ``dask.distributed``.

Dask Delayed
============

For the ``dask.delayed`` API, simply import the ``delayed`` and call it with the ``target_function``, followed by a second call operator containing the arguments to pass to the ``target_function``.

The result will be a ``dask.Delayed`` instance and can be passed to subsequent ``delayed`` calls. See the `Dask Delayed documentation <http://docs.dask.org/en/latest/delayed.html>`_ for more details.

In the example below, we create a function that builds our delayed style job The function returns the final ``dask.Delayed`` object, which will be used by the Dask Job:

::

    import dask

    # Delayed Job
    def delayed_job():
        output = []
        for x in range(3):
            a = dask.delayed(foo, pure=False)(x)
            b = dask.delayed(bar, pure=False)(x)
            c = dask.delayed(baz, pure=False)(a, b)
            output.append(c)
        return dask.delayed(sum_up, pure=False)(output)

.. important::

    Do use ``dask.delayed`` or ``dask.distributed`` directly in a file containing Django imports, such as a controller or model file. This will produce confusing errors. Instead, define functions that build the Dask jobs in a separate file and call those functions in controllers.


The example below shows the pattern used to create Dask Jobs using the ``dask.delayed`` API:

::

    from tethysapp.my_first_app.job_functions import delayed_job
    from .app import App

    # 1. Get a Dask Scheduler
    scheduler = App.get_scheduler(name='dask_primary')

    # 2. Get job manager for this app
    job_manager = App.get_job_manager()

    # 3. Call function that builds the ``dask.delayed`` job, returning one ``dask.Delayed`` object
    delayed = delayed_job()

    # 4. Use job manager to create dask job
    dask = job_manager.create_job(
        job_type='DASK',
        name='dask_distributed',
        user=request.user,
        scheduler=scheduler
    )

    # 5. Call the ``DaskJob.execute`` method, giving it the ``dask.Delayed`` object
    dask.execute(delayed)

.. note::

    ``dask.delayed`` style jobs do not begin processing until the ``DaskJob.execute`` method is called.

Dask Distributed
================

For ``dask.distributed`` API, use the ``dask.distributed.Client.submit`` method to submit tasks to the distributed cluster. Call ``submit`` with ``target_function``, as the first argument, followed by any number of args and kwargs to pass to the ``target_function``.

The ``submit`` method submits the job immediately and returns a ``dask.distributed.Future`` instance. The ``Future`` instance can be passed as an argument to subsequent ``submit`` calls. See the `Dask Futures <http://docs.dask.org/en/latest/futures.html>`_ documentation for more details.

In the example below, we create a function that builds a ``dask.distributed`` style job. The function takes as an argument a ``dask.distributed.Client`` instance and returns the final ``dask.distributed.Future`` object which will be used by the Dask Job.

::

    import dask

    # Distributed Job
    def distributed_job(client):
        output = []
        for x in range(3):
            a = client.submit(foo, x, pure=False)
            b = client.submit(bar, x, pure=False)
            c = client.submit(baz, a, b, pure=False)
            output.append(c)
        return client.submit(sum_up, output)


The example below shows the pattern used to create Dask Jobs using the ``dask.distributed`` API. The ``dask.distributed.Client`` that is needed for distributed type jobs can be retrieved from any Dask Scheduler object. This example also illustrates how to use a custom ``process_results_function``, which is valid for any type of Tethys Job:

::

    from tethysapp.my_first_app.job_functions import distributed_job, convert_to_dollar_sign
    from .app import App

    # 1. Get a Dask Scheduler
    scheduler = App.get_scheduler(name='dask_primary')

    # 2. Get job manager for this app
    job_manager = App.get_job_manager()

    # 3. Get the dask.distributed.Client instance from the scheduler
    try:
        client = scheduler.client
    except DaskJobException:
        return redirect(reverse('dask_tutorial:error_message'))

    # 4. Call function that builds the dask.distributed job, returning one dask.distributed.Future object
    future = distributed_job(client)

    # 5. Use job manager to create Dask Job
    dask = job_manager.create_job(
        job_type='DASK',
        name='dask_distributed',
        user=request.user,
        scheduler=scheduler
    )

    # 6. Assign custom process results function (valid for any type of job, not just distributed jobs)
    dask.process_results_function = convert_to_dollar_sign

    # 7. Call the DaskJob.execute method, giving it the dask.distributed.Future object
    dask.execute(future)

.. note::

    ``dask.distributed`` style jobs begin processing as soon as ``dask.distributed.Client.submit`` is called, not when ``DaskJob.execute`` is called.

Multiple Leaf Jobs
==================

Frequently, Dask job tree end with multiple nodes, rather than a single node as illustrated above. This results in multiple ``dask.distributed.Future`` or ``dask.Delayed`` objects that need to be tracked. This section shows one strategy that can be used to track multi-leaf jobs using the Tethys Dask Job.

In the example below, we create a function that is almost identical to the ``dask.distributed`` example, but the aggregation step (``sum`` function call) is omitted, resulting in a list of ``Future`` objects, rather than just one as before.

::

    import dask

    # Multiple Leaf Distributed Job
    def muliple_leaf_job(client):
        output = []
        for x in range(3):
            a = client.submit(foo, x, pure=False)
            b = client.submit(bar, x, pure=False)
            c = client.submit(baz, a, b, pure=False)
            output.append(c)
        return output

The following example shows how to create multiple Dask Jobs to tracke a multi-leaf job:

::

    from tethysapp.my_first_app.job_functions import muliple_leaf_job
    from .app import App

    # 1. Get a Dask Scheduler
    scheduler = App.get_scheduler(name='dask_primary')

    # 2. Get job manager for this app
    job_manager = App.get_job_manager()

    # 3. Get the dask.distributed.Client instance from the scheduler
    try:
        client = scheduler.client
    except DaskJobException:
        return redirect(reverse('dask_tutorial:error_message'))

    # 4. Call function that builds the dask.distributed job, returning multiple dask.distributed.Future objects
    futures = multiple_leaf_job(client)

    # 5. Iterate through the list of futures, creating a new DaskJob for each one and calling DaskJob.execute on it.
    i = random.randint(1, 10000)

    for future in futures:
        i += 1
        name = 'dask_leaf' + str(i)
        dask = job_manager.create_job(
            job_type='DASK',
            name=name,
            user=request.user,
            scheduler=scheduler
        )
        dask.execute(future)

.. note::

    This strategy can be used for both the ``dask.delayed`` and ``dask.distributed`` approaches.

Results
=======

The result of a Dask job is serialized and stored in the database by default. To retrieve results stored in the database, get the Dask Job instance and call it's ``result`` property:

::

    # Get job
    job = job_manager.get_job(job_id=job_id)

    # Get result
    result = dask_job.result

This behavior may be overridden in two ways:

#. Provide a custom ``process_results_function``. For example, this could be used to write the results to a file, instead:

    ::

        dask = job_manager.create_job(
            job_type='DASK',
            name='dask_distributed',
            user=request.user,
            scheduler=scheduler
        )

        dask.process_results_function = custom_processing_function

#. Set the ``forget`` property of the Dask Job to ``True``. The results will not be retrieved or saved when ``forget`` is ``True``:

    ::

        dask = job_manager.create_job(
            job_type='DASK',
            name=name,
            user=request.user,
            scheduler=scheduler,
            forget=True
        )

.. important::

    If the custom ``process_results_function`` returns anything, it will be serialized and stored in the results field.

API Documentation
=================

.. autoclass:: tethys_sdk.jobs.DaskJob