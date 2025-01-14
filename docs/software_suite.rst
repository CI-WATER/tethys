.. _software_suite:

**************
Software Suite
**************

**Last Updated:** January 2020

The Tethys Software Suite is a collection of recommended software that can be used with Tethys Platform. The primary motivation of creating the Tethys Software Suite was overcome the hurdle associated with selecting a GIS software stack to support spatial capabilities in apps.

.. figure:: images/features/tethys_platform_diagram.png
    :width: 600px
    :align: center

A majority of the software projects included in the Tethys Software Suite are web GIS projects that can be used to acquire, modify, store, visualize, and analyze spatial data, but it also includes other software to address computing and plotting needs of spatial web apps.


Spatial Database Storage
========================

.. image:: images/software/postgis.png
   :width: 170px
   :align: right

Tethys Platform includes support for the `PostgreSQL <http://www.postgresql.org/>`_ database with `PostGIS <http://postgis.net/>`_, a spatial database extension, to provide spatial data storage capabilities for Tethys web apps. PostGIS adds spatial column types including raster, geometry, and geography. The extension also provides database functions for basic analysis of GIS objects.

To use a PostgreSQL database in your app use the :doc:`./tethys_sdk/tethys_services/persistent_store`. To use a spatially enabled database with PostGIS use the :doc:`./tethys_sdk/tethys_services/spatial_persistent_store`.

Map Publishing
==============

.. image:: images/software/geoserver.png
   :width: 200px
   :align: right

Tethys Platform provides support for `GeoServer <http://geoserver.org/>`_ as one option for publishing spatial data as web services. GeoServer is used to publish common spatial files such as Shapefiles and GeoTIFFs in web-friendly formats.

To use the map publishing capabilities of GeoServer in your app refer to the :doc:`./software_suite/geoserver` documentation and use the :doc:`./tethys_sdk/tethys_services/spatial_dataset_services`.

THREDDS Data Server
-------------------

Tethys Platform supports the `THREDDS Data Server <https://www.unidata.ucar.edu/software/tds/current/>`_ as an alternative option for publishing spatial data as web services. "The THREDDS Data Server (TDS) is a web server that provides metadata and data access for scientific datasets, using OPeNDAP, OGC WMS and WCS, HTTP, and other remote data access protocols. The TDS is developed and supported by Unidata, a division of the University Corporation for Atmospheric Research, and is sponsored by the National Science Foundation."

To use the map publishing capabilities of the THREDDS Data Server in your app refer to :doc:`./software_suite/thredds` documentation and use the :doc:`./tethys_sdk/tethys_services/spatial_dataset_services`.

Geoprocessing
=============

.. image:: images/software/52n-logo.gif
   :width: 150px
   :align: right

`52°North Web Processing Service (WPS) <http://52north.org/communities/geoprocessing/wps/>`_ is supported in Tethys Platform as one means for supporting geoprocessing needs in water resources web app development. It can be linked with geoprocessing libraries such as `GRASS <http://grass.osgeo.org/>`_, `Sextante <http://www.wikiwand.com/es/SEXTANTE_(SIG)>`_, and `ArcGIS® Server <http://www.esri.com/software/arcgis/arcgisserver>`_ for out-of-the-box geoprocessing capabilities.

The PostGIS extension, included in the software suite, can also provide geoprocessing capabilities on data that is stored in a spatially-enabled database. PostGIS includes SQL geoprocessing functions for splicing, dicing, morphing, reclassifying, and collecting/unioning raster and vector types. It also includes functions for vectorizing rasters, clipping rasters with vectors, and running stats on rasters by geometric region.

To use 52°North WPS or other WPS geoprocessing services in your app use the :doc:`./tethys_sdk/tethys_services/web_processing_services`.

Visualization
=============

.. image:: images/software/openlayers.png
   :width: 75px
   :align: right

`OpenLayers <http://openlayers.org/>`_ is a JavaScript web-mapping client library for rendering interactive maps on a web page. It is capable of displaying 2D maps of OGC web services and a myriad of other spatial formats and sources including GeoJSON, KML, GML, TopoJSON, ArcGIS REST, and XYZ.

To use an OpenLayers map in your app use the **Map View Gizmo** of the :doc:`./tethys_sdk/gizmos`.

.. image:: images/software/cesium_color_black.png
   :width: 75px
   :align: right

`Cesium JS™ <https://cesium.com/>`_ is an open-source Javascript library for creating world-class 3D globes and maps with the best possible performance, precision, visual quality and ease of use.


To use a Cesium map in your app use the **Cesium Map View Gizmo** of the :doc:`./tethys_sdk/gizmos`.

.. image:: images/software/highcharts.png
   :width: 75px
   :align: right

Plotting capabilities are provided by `Highcharts <http://www.highcharts.com/>`_, a JavaScript library created by Highsoft AS. The plots created using Highcharts are interactive with hovering effects, pan and zoom capabilities, and the ability to export the plots as images.

To use an Highcharts in your app use the **Plot View Gizmo** of the :doc:`./tethys_sdk/gizmos`.

.. image:: images/software/plotly_logo.jpeg
   :width: 75px
   :align: right

The `Plotly Python Library <https://plot.ly/python/>`_ makes interactive, publication-quality graphs. Examples of how to make line plots, scatter plots, area charts, bar charts, error bars, box plots, histograms, heatmaps, subplots, multiple-axes, polar charts, and bubble charts. Plotly.py is free and open source and you can view the source, report issues or contribute on GitHub.

To use an Plotly in your app use the **Plotly View Gizmo** of the :doc:`./tethys_sdk/gizmos`.

Distributed Computing
=====================

.. image:: images/software/htcondor.png
   :width: 300px
   :align: right

To facilitate the large-scale computing that is often required by water resources applications, Tethys Platform leverages the computing management middleware `HTCondor <http://research.cs.wisc.edu/htcondor/>`_ and `Dask Distributed <http://distributed.dask.org/en/stable/>`_.

To use the HTCondor or Dask and the computing capabilities in your app use the :doc:`./tethys_sdk/jobs`.

File Dataset Storage
====================

Tethys Platform does not include software for handling flat file storage. However, Tethys SDK provides APIs for working with CKAN and HydroShare to address flat file storage needs. Descriptions of CKAN and HydroShare are provided here for convenience.

.. image:: images/software/ckan.png
   :width: 150px
   :align: right

`CKAN <http://ckan.org/>`_ is an open source data sharing platform that streamlines publishing, sharing, finding, and using data. There is no central CKAN hub or portal, rather data publishers setup their own instance of CKAN to host the data for their organization.

.. image:: images/software/hydroshare.png
   :width: 200px
   :align: right

`HydroShare <http://hydroshare.cuahsi.org/>`_ is an online hydrologic model and data sharing portal being developed by CUAHSI. It builds on the sharing capabilities of CUAHSI’s Hydrologic Information System by adding support for sharing models and using social media functionality.

To use a CKAN instance for flat file storage in your app use the :doc:`./tethys_sdk/tethys_services/dataset_services`. HydroShare is not fully supported at this time, but when it is you will use the :doc:`./tethys_sdk/tethys_services/dataset_services` to access HydroShare resources.

WebSocket Communication
=======================

.. image:: images/software/django-channels.png
   :width: 200px
   :align: right

Tethys Platform supports WebSocket connections using `Django Channels <https://channels.readthedocs.io/en/latest/>`_. Django Channels is an official Django project that brings asynchronous and long-running connections to the synchronous Django.

The WebSocket protocol provides a persistent connection between the client and the server. In contrast to the traditional HTTP protocol, the webscoket protocol allows for bidirectional communication between the client and the server (i.e. the server can trigger a response without the client sending a request). Django Channels uses Consumers to structure code and handle client/server communication in a similar way Controllers are used with the HTTP protocol. When creating a WebSocket connection, a "handshake" needs to be established between the client and server.

For more information about Django Channels and Consumers visit `the Django Channels docummentation <https://channels.readthedocs.io/en/latest/>`_.

For more information on establishing a WebSocket connection see `the JavaScript WebSocket API <https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/>`_. Alternatively, other existing JavaScript or Python WebSocket clients can we used.

To create a URL mapping using the WebSocket protocol see the example provided in the `App Base Class API documentation <./tethys_sdk/app_class.html#override-methods>`_.

Docker Installation
===================

.. image:: images/software/docker.png
   :width: 300px
   :align: right

Tethys Platform uses `Docker <https://www.docker.com/>`_ virtual container system as an optional component to simplify the installation of some elements. Docker images are created and used to create containers, which are essentially stripped down virtual machines running only the software included in the image. Unlike virtual machines, the Docker containers do not partition the resources of your computer (processors, RAM, storage), but instead run as processes with full access to the resources of the computer.

Four Docker images are supported as part of Tethys Platform including:

* PostgreSQL with PostGIS
* 52° North WPS
* GeoServer
* THREDDS

The installation procedure for each software has been encapsulated in a Docker image reducing the installation procedure to three simple steps:

1. Install Docker
2. Download the Docker images
3. Deploy the Docker images as containers

SDK Relationships
=================

Tethys Platform provides a software development kit (SDK) that provides application programming interfaces (APIs) for interacting with each of the software included in teh Software Suite. The appropriate APIs are referenced in each section above, but a summary table of the relationship between the Software Suite and the SDK is provided as a reference.

=====================================  ===============================================================  ============================================
Software                               API                                                              Functionality
=====================================  ===============================================================  ============================================
PostgreSQL                             :doc:`./tethys_sdk/tethys_services/persistent_store`             SQL Database Storage
PostGIS                                :doc:`./tethys_sdk/tethys_services/spatial_persistent_store`     Spatial Database Storage and Geoprocessing
GeoServer                              :doc:`./tethys_sdk/tethys_services/spatial_dataset_services`     Spatial File Publishing
THREDDS Data Server                    :doc:`./tethys_sdk/tethys_services/spatial_dataset_services`     Spatial File Publishing
52° North WPS                          :doc:`./tethys_sdk/tethys_services/web_processing_services`      Geoprocessing Services
OpenLayers, Google Maps, HighCharts    :doc:`./tethys_sdk/gizmos`                                       Spatial and Tabular Visualization
HTCondor, Dask                         :doc:`./tethys_sdk/jobs`
CKAN, HydroShare                       :doc:`./tethys_sdk/tethys_services/dataset_services`             Flat File Storage
=====================================  ===============================================================  ============================================

References
==========

.. toctree::
   :maxdepth: 1

   software_suite/geoserver
   software_suite/thredds
