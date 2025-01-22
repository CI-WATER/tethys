.. _tds_geoserver_reference:

****************************************
GeoServer SpatialDatasetEngine Reference
****************************************

**Last Updated**: December 2019

This guide provides and overview the ``GeoServerSpatialDatasetEngine``, which implements the ``SpatialDatasetEngine`` pattern.

Key Concepts
============

There are quite a few concepts to understand before working with GeoServer and spatial dataset services. Definitions of each are provided here for quick reference.

**Resources** are the spatial datasets. These can vary in format ranging from a single file or multiple files to database tables depending on the type resource.

**Feature Type**: is a type of *resource* containing vector data or data consisting of discreet features such as points, lines, or polygons and any tables of attributes that describe the features.

**Coverage**: is a type of *resource* containing raster data or numeric gridded data.

**Layers**: are *resources* that have been published. Layers associate styles and other settings with the *resource* that are needed to generate maps of the *resource* via OGC services.

**Layer Groups**: are preset groups of *layers* that can be served as WMS services as though they were one *layer*.

**Stores**: represent repositories of spatial datasets such as database tables or directories of shapefiles. A *store* containing only *feature types* is called a **Data Store** and a *store* containing only *coverages* is called a **Coverage Store**.

**Workspaces**: are arbitrary groupings of data to help with organization of the data. It would be a good idea to store all of the spatial datasets for your app in a workspace resembling the name of your app to avoid conflicts with other apps.

**Styles**: are a set of rules that dictate how a *layer* will be rendered when accessed via WMS. A *layer* may be associated with many styles and a style may be associated with many *layers*. Styles on GeoServer are written in `Styled Layer Descriptor (SLD) <http://www.opengeospatial.org/standards/sld>`_ format.

**Styled Layer Descriptor (SLD)**:  An XML-based markup language that can be used to specify how spatial datasets should be rendered. See GeoServer's `SLD Cookbook <http://docs.geoserver.org/stable/en/user/styling/sld-cookbook/index.html#sld-cookbook>`_ for a good primer on SLD.

**Web Feature Service (WFS)**: An OGC standard for exchanging vector data (i.e.: feature types) over the internet. WFS can be used to not only query for the features (points, lines, and polygons) but also the attributes associated with the features.

**Web Coverage Service (WCS)**: An OGC standard for exchanging raster data (i.e.: coverages) over the internet. WCS is roughly the equivalent of WFS but for *coverages*, access to the raw coverage information, not just the image.

**Web Mapping Service (WMS)**: An OGC standard for generating and exchanging maps of spatial data over the internet. WMS can be used to compose maps of several different spatial dataset sources and formats.

Example Usage
=============

Consider the following example for uploading a shapefile to a GeoServer spatial dataset service:

Upload Shapefile
----------------

::

    from .app import App

    # First get an engine
    engine = App.get_spatial_dataset_service('primary_geoserver', as_engine=True)

    # Create a workspace named after our app
    engine.create_workspace(workspace_id='my_app', uri='http://www.example.com/apps/my-app')

    # Path to shapefile base for foo.shp, side cars files (e.g.: .shx, .dbf) will be
    # gathered in addition to the .shp file.
    shapefile_base = '/path/to/foo'

    # Notice the workspace in the store_id parameter
    result = dataset_engine.create_shapefile_resource(store_id='my_app:foo', shapefile_base=shapefile_base)

    # Check if it was successful
    if not result['success']:
        raise


A new shapefile Data Store will be created called 'foo' in workspace 'my_app' and a resource will be created for the shapefile called 'foo'. A layer will also automatically be configured for the new shapefile resource.

Retrieve Services for a Layer
-----------------------------

Publishing the spatial dataset with a spatial dataset service would be pointless without using the service to render the data on a map. This can be done by querying the data using the OGC web services WFS, WCS, or WMS. The dictionary that is returned when retrieving layers, layer groups, or resources includes a key for each OGC service available for the object returned. Feature type resources will provide a "wfs" key, coverage resources will provide a "wcs" key, and layers and layergroups will provide a "wms" key. The value will be another dictionary of OGC queries for different endpoints. For example:

::

    # Get a feature type layer
    response = engine.get_layer(layer_id='sf:roads', debug=True)

    # Response dictionary includes "wms" key with links to maps in various formats
    {'result': {'advertised': True,
                'attribution': None,
                'catalog': 'http://localhost:8181/geoserver/',
                'default_style': 'simple_roads',
                'enabled': None,
                'href': 'http://localhost:8181/geoserver/rest/layers/sf%3Aroads.xml',
                'name': 'sf:roads',
                'resource': 'sf:roads',
                'resource_type': 'layer',
                'styles': ['sf:line'],
                'wms': {'georss': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=rss',
                        'geotiff8': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/geotiff8',
                        'geptiff': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/geotiff',
                        'gif': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/gif',
                        'jpeg': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/jpeg',
                        'kml': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=kml',
                        'kmz': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=kmz',
                        'openlayers': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=application/openlayers',
                        'pdf': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=application/pdf',
                        'png': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/png',
                        'png8': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/png8',
                        'svg': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/svg',
                        'tiff': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/tiff',
                        'tiff8': 'http://localhost:8181/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=sf:roads&styles=simple_roads&transparent=true&tiled=no&srs=EPSG:26713&bbox=589434.8564686741,4914006.337837095,609527.2102150217,4928063.398014731&width=731&height=512&format=image/tiff8'}},
     'success': True}

These links can be passed to a web mapping client like OpenLayers or Google Maps to render the map interactively on a web page. Note that the OGC mapping services are very powerful and the links provided represent only a simple query. You can construct custom OGC URLs queries without much difficulty. For excellent primers on WFS, WCS, and WMS with GeoServer, visit these links:

* `GeoServer Web Feature Service Overview <http://docs.geoserver.org/stable/en/user/services/wfs/index.html>`_
* `GeoServer Web Coverage Service Overview <http://docs.geoserver.org/stable/en/user/services/wcs/index.html>`_
* `GeoServer Web Map Service Overview <http://docs.geoserver.org/stable/en/user/services/wms/index.html>`_

.. tip::

    When you are learning how to use the spatial dataset engine methods, run the commands with the debug parameter set to true. This will automatically pretty print the result dictionary to the console so that you can inspect its contents:

    .. code-block:: python

      # Example method with debug option
      engine.list_layers(debug=True)

API
===

The following reference provides a summary the class used to define the ``GeoServerSpatialDatasetEngine`` objects.

.. autoclass:: tethys_dataset_services.engines.GeoServerSpatialDatasetEngine
    :members:
