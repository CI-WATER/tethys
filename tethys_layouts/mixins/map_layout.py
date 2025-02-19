import collections
import copy
import logging
import json

from tethys_gizmos.gizmo_options import MVLayer

log = logging.getLogger(f"tethys.{__name__}")

_COLOR_RAMPS = {
    "Default": [
        "#fff100",
        "#ff8c00",
        "#e81123",
        "#ec008c",
        "#68217a",
        "#00188f",
        "#00bcf2",
        "#00b294",
        "#009e49",
        "#bad80a",
    ],
    "Blue": [
        "#f7fbff",
        "#deebf7",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#08519c",
        "#083582",
        "#022259",
    ],
    "Blue and Red": [
        "#a50026",
        "#d73027",
        "#f46d43",
        "#fdae61",
        "#fee090",
        "#e0f3f8",
        "#abd9e9",
        "#74add1",
        "#4575b4",
        "#313695",
    ],
    "Elevated": [
        "#96D257",
        "#278C39",
        "#2A7B45",
        "#829C41",
        "#DBB82E",
        "#AE4818",
        "#842511",
        "#61370F",
        "#806346",
        "#C2C2C2",
        "#FFFFFF",
    ],
    "Flower Field": [
        "#e60049",
        "#0bb4ff",
        "#50e991",
        "#e6d800",
        "#9b19f5",
        "#ffa300",
        "#dc0ab4",
        "#b3d4ff",
        "#00bfa0",
        "#f0cccc",
    ],
    "Galaxy Berries": [
        "#0040bf",
        "#a3cc52",
        "#b9a087",
        "#a01fcc",
        "#5bb698",
        "#5e851e",
        "#d1943f",
        "#96aedc",
        "#629ed9",
        "#8a64b3",
    ],
    "Heat Map": [
        "#90a1be",
        "#a761aa",
        "#af4980",
        "#b83055",
        "#c80000",
        "#d33300",
        "#de6600",
        "#e99900",
        "#f4cc00",
        "#ffff00",
    ],
    "Olive Harmony": [
        "#437a75",
        "#d9d78c",
        "#bf7860",
        "#72231f",
        "#afbfa2",
        "#5a9bc8",
        "#89a6a6",
        "#99905c",
        "#414b8c",
        "#a664a0",
    ],
    "Mother Earth": [
        "#a03500",
        "#d9b400",
        "#3264c8",
        "#72b38e",
        "#986ba1",
        "#b9a087",
        "#4c91bf",
        "#a5d236",
        "#96aedc",
        "#ad8516",
    ],
    "Rainbow": [
        "#fff100",
        "#ff8c00",
        "#e81123",
        "#ec008c",
        "#68217a",
        "#00188f",
        "#00bcf2",
        "#00b294",
        "#009e49",
        "#bad80a",
    ],
    "Rainforest Frogs": [
        "#dc4b00",
        "#3c6ccc",
        "#d9dc00",
        "#91d900",
        "#986ba1",
        "#d99f00",
        "#4db478",
        "#4cafdc",
        "#96aedc",
        "#d7a799",
    ],
    "Retro FLow": [
        "#007fd9",
        "#443dbf",
        "#881fc5",
        "#bf00bf",
        "#d43f70",
        "#d9874c",
        "#b6a135",
        "#adbf27",
        "#c4dc66",
        "#ebe498",
    ],
    "Sunset Fade": [
        "#b30000",
        "#7c1158",
        "#4421af",
        "#1a53ff",
        "#0d88e6",
        "#00b7c7",
        "#5ad45a",
        "#8be04e",
        "#c5d96d",
        "#ebdc78",
    ],
}

_THREDDS_PALETTES = [
    "boxfill/alg",
    "boxfill/alg2",
    "boxfill/ferret",
    "boxfill/greyscale",
    "boxfill/ncview",
    "boxfill/occam",
    "boxfill/occam_pastel-30",
    "boxfill/rainbow",
    "boxfill/redblue",
    "boxfill/sst_36",
]

_DEFAULT_TILE_GRID = {
    "resolutions": [
        156543.03390625,
        78271.516953125,
        39135.7584765625,
        19567.87923828125,
        9783.939619140625,
        4891.9698095703125,
        2445.9849047851562,
        1222.9924523925781,
        611.4962261962891,
        305.74811309814453,
        152.87405654907226,
        76.43702827453613,
        38.218514137268066,
        19.109257068634033,
        9.554628534317017,
        4.777314267158508,
        2.388657133579254,
        1.194328566789627,
        0.5971642833948135,
        0.2985821416974068,
        0.1492910708487034,
        0.0746455354243517,
        0.0373227677121758,
        0.0186613838560879,
        0.009330691928044,
        0.004665345964022,
        0.002332672982011,
        0.0011663364910055,
        0.0005831682455027,
        0.0002915841227514,
        0.0001457920613757,
    ],
    "extent": [-20037508.34, -20037508.34, 20037508.34, 20037508.34],
    "origin": [0.0, 0.0],
    "tileSize": [256, 256],
}


class MapLayoutMixin:
    """
    Provides helper methods for creating MVLayer objects with the extra attributes that are needed by the MapLayout. Use this Mixin to add this functionality to classes that may be used outside of the MapLayout scope (e.g. processing workflows that need to create layer objects for MapLayouts).
    """  # noqa: E501

    COLOR_RAMPS = copy.deepcopy(_COLOR_RAMPS)
    THREDDS_PALETTES = copy.deepcopy(_THREDDS_PALETTES)
    DEFAULT_TILE_GRID = copy.deepcopy(_DEFAULT_TILE_GRID)

    map_extent = None
    _default_popup_excluded_properties = ["id", "type", "layer_name"]

    @classmethod
    def get_vector_style_map(cls):
        raise NotImplementedError

    @classmethod
    def _build_mv_layer(
        cls,
        layer_source,
        layer_name,
        layer_title,
        layer_variable,
        options,
        layer_id=None,
        extent=None,
        visible=True,
        public=True,
        selectable=False,
        plottable=False,
        has_action=False,
        excluded_properties=None,
        popup_title=None,
        geometry_attribute=None,
        style_map=None,
        show_download=False,
        times=None,
        renamable=False,
        removable=False,
        show_legend=True,
        legend_url=None,
        label_options=None,
    ):
        """
        Build an MVLayer object with supplied arguments.
        Args:
            layer_source(str): OpenLayers Source to use for the MVLayer (e.g.: "TileWMS", "ImageWMS", "GeoJSON").
            layer_name(str): Name of GeoServer layer (e.g.: workspace:a-unique-layer-name).
            layer_title(str): Title of MVLayer (e.g.: Model Boundaries).
            layer_variable(str): Variable type of the layer (e.g.: model_boundaries).
            options(dict): A dictionary representation of the OpenLayers options object for ol.source.
            layer_id(UUID, int, str): layer_id for non geoserver layer where layer_name may not be unique.
            visible(bool): Layer is visible when True. Defaults to True.
            selectable(bool): Enable feature selection. Defaults to False.
            plottable(bool): Enable "Plot" button on pop-up properties. Defaults to False.
            has_action(bool): Enable "Action" button on pop-up properties. Defaults to False.
            extent(list): Extent for the layer. Optional.
            popup_title(str): Title to display on feature popups. Defaults to layer title.
            excluded_properties(list): List of properties to exclude from feature popups.
            geometry_attribute(str): Name of the geometry attribute. Optional.
            style_map(dict): Style map dictionary. See MVLayer documentation for examples of style maps. Optional.
            show_download(boolean): enable download layer. (only works for geojson layer).
            times(list): List of time steps if layer is time-enabled. Times should be represented as strings in
                ISO 8601 format (e.g.: ["20210322T112511Z", "20210322T122511Z", "20210322T132511Z"]). Currently
                only supported in CesiumMapView.
            renamable(bool): Show Rename option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            removable(bool): Show Remove option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            show_legend(bool): Show the legend for this layer when True and legends are enabled. Defaults to True.
            legend_url(str): URL of a legend image to display for the layer when legends are enabled.
            label_options(dict): Dictionary for labeling.  Possibilities include label_property (the name of the
                property to label), font (label font), alignment (alignment of the label), offset (x offset). Optional.

        Returns:
            MVLayer: the MVLayer object.
        """
        # Derive popup_title if not given
        if not popup_title:
            popup_title = layer_title

        data = {
            "layer_id": str(layer_id) if layer_id else layer_name,
            "layer_name": layer_name,
            "popup_title": popup_title,
            "layer_variable": layer_variable,
            "toggle_status": public,
            "renamable": renamable,
            "removable": removable,
            "show_legend": show_legend,
            "legend_url": legend_url,
        }

        # Process excluded properties
        properties_to_exclude = copy.deepcopy(cls._default_popup_excluded_properties)

        if plottable:
            properties_to_exclude.append("plot")

        if excluded_properties and isinstance(excluded_properties, (list, tuple)):
            for ep in excluded_properties:
                if ep not in properties_to_exclude:
                    properties_to_exclude.append(ep)

        data.update({"excluded_properties": properties_to_exclude})

        if plottable:
            data.update({"plottable": plottable})

        if has_action:
            data.update({"has_action": has_action})

        if not extent:
            extent = cls.map_extent

        # Build layer options
        layer_options = {"visible": visible, "show_download": show_download}

        if style_map:
            layer_options.update({"style_map": style_map})

        if label_options:
            layer_options.update({"label_options": label_options})

        mv_layer = MVLayer(
            source=layer_source,
            options=options,
            layer_options=layer_options,
            legend_title=layer_title,
            legend_extent=extent,
            legend_classes=[],
            data=data,
            feature_selection=selectable,
            times=times,
            geometry_attribute=geometry_attribute,
        )

        return mv_layer

    @classmethod
    def build_layer_group(
        cls,
        id,
        display_name,
        layers,
        layer_control="checkbox",
        visible=True,
        public=True,
        collapsed=False,
        renamable=False,
        removable=False,
    ):
        """
        Build a layer group object.

        Args:
            id(str): Unique identifier for the layer group.
            display_name(str): Name displayed in MapView layer selector/legend.
            layers(list<MVLayer>): List of layers to include in the layer group.
            layer_control(str): Type of control for layers. Either 'checkbox' or 'radio'. Defaults to checkbox.
            visible(bool): Whether layer group is initially visible. Defaults to True.
            public(bool): Enable public to see this layer group if True.
            collapsed(bool): Render layer group collapsed initially. Defaults to False.
            renamable(bool): Show Rename option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            removable(bool): Show Remove option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.

        Returns:
            dict: Layer group definition.
        """
        if layer_control not in ["checkbox", "radio"]:
            raise ValueError(
                'Invalid layer_control. Must be on of "checkbox" or "radio".'
            )

        layer_group = {
            "id": id,
            "display_name": display_name,
            "control": layer_control,
            "layers": layers,
            "visible": visible,
            "toggle_status": public,
            "collapsed": collapsed,
            "renamable": renamable,
            "removable": removable,
        }
        return layer_group

    @classmethod
    def build_param_string(cls, **kwargs):
        """
        Build a VIEWPARAMS or ENV string with given kwargs (e.g.: 'foo:1;bar:baz')

        Args:
            **kwargs: key-value pairs of paramaters.

        Returns:
            str: parameter string.
        """
        if not kwargs:
            return ""

        joined_pairs = []
        for k, v in kwargs.items():
            joined_pairs.append(":".join([k, str(v)]))

        param_string = ";".join(joined_pairs)
        return param_string

    @classmethod
    def build_legend(cls, layer, units=""):
        """
        Build Legend data for a given layer

        Args:
            layer (MVLayer): An MVLayer object built using MapLayout.build_wms_layer().
            units (str): unit for the legend.

        Returns:
            dict: Legend data associated with the layer.
        """
        legend = None
        layer_id = (
            layer.data.get("layer_id")
            if layer.data.get("layer_id")
            else layer.data.get("layer_name")
        )
        legend_id = f"legend-for-{layer_id}"

        if ":" in legend_id:
            legend_id = legend_id.replace(":", "_")

        if "," in legend_id:
            legend_id = legend_id.replace(",", "_")

        if layer.data.get("legend_url") is not None:
            legend = {
                "type": "image-url-legend",
                "legend_id": legend_id,
                "layer_id": layer_id,
                "title": layer.legend_title,
                "url": layer.data.get("legend_url"),
            }

        elif layer.data.get("color_ramp_division_kwargs") is not None:
            div_kwargs = layer.data.get("color_ramp_division_kwargs")
            min_value = div_kwargs["min_value"]
            max_value = div_kwargs["max_value"]
            color_ramp = (
                div_kwargs["color_ramp"]
                if "color_ramp" in div_kwargs.keys()
                else "Default"
            )
            prefix = div_kwargs["prefix"] if "prefix" in div_kwargs.keys() else "val"
            color_prefix = (
                div_kwargs["color_prefix"]
                if "color_prefix" in div_kwargs.keys()
                else "color"
            )
            first_division = (
                div_kwargs["first_division"]
                if "first_division" in div_kwargs.keys()
                else 1
            )

            legend = {
                "type": "custom-divisions",
                "legend_id": legend_id,
                "title": layer.legend_title,
                "divisions": dict(),
                "color_list": list(cls.COLOR_RAMPS.keys()),
                "layer_id": layer_id,
                "min_value": min_value,
                "max_value": max_value,
                "color_ramp": color_ramp,
                "prefix": prefix,
                "color_prefix": color_prefix,
                "first_division": first_division,
                "units": units,
                "select_options": [(c, c) for c in cls.COLOR_RAMPS.keys()],
                "initial_option": color_ramp,
            }

            divisions = cls.generate_custom_color_ramp_divisions(
                **layer.data["color_ramp_division_kwargs"]
            )

            for label in divisions.keys():
                if (
                    color_prefix in label
                    and int(label.replace(color_prefix, "")) >= first_division
                ):
                    legend["divisions"][
                        float(divisions[label.replace(color_prefix, prefix)])
                    ] = divisions[label]
            legend["divisions"] = collections.OrderedDict(
                sorted(legend["divisions"].items())
            )

        elif "options" in layer and layer.options.get("serverType", "").lower() in (
            "geoserver",
            "thredds",
        ):
            server_type = layer.options.get("serverType", "").lower()
            wms_url = layer.options.get("url")
            wms_params = layer.options.get("params")
            if not wms_params:
                log.error(
                    f"Legend Creation Error: No params found for given layer: {layer}"
                )
                return None

            wms_layer_name_param = wms_params.get("LAYERS", "")
            wms_styles_param = wms_params.get("STYLES", "")

            legend = {
                "legend_id": legend_id,
                "layer_id": layer_id,
                "title": layer.legend_title,
            }

            if server_type == "thredds":
                select_options = [("Default", "")]
                select_options.extend(
                    [
                        (p.replace("boxfill/", "").title(), p)
                        for p in cls.THREDDS_PALETTES
                    ]
                )
                default_palette = wms_params.get("STYLES") or "Default"
                legend.update(
                    {
                        "type": "thredds-wms-legend",
                        "palettes": cls.THREDDS_PALETTES,
                        "default_palette": default_palette,
                        "select_options": select_options,
                        "initial_option": default_palette,
                        "url": f"{wms_url}?REQUEST=GetLegendGraphic&LAYER={wms_layer_name_param}",
                    }
                )

            elif server_type == "geoserver":
                # Build legend select options from styles assigned to layer
                select_options = None
                wms_styles = []
                if wms_styles_param and len(wms_styles_param) > 0:
                    wms_styles = wms_styles_param.split(",")

                    # Only build select options if there is more than one style assigned
                    if len(wms_styles) > 1:
                        select_options = [("Default", "")]
                        for wms_style in wms_styles:
                            display_style = wms_style
                            if ":" in display_style:
                                display_style = display_style.split(":")[1]
                            display_style = (
                                display_style.replace("_", " ")
                                .replace("-", " ")
                                .title()
                            )
                            select_options.append((display_style, wms_style))

                legend.update(
                    {
                        "type": "geoserver-wms-legend",
                        "select_options": select_options,
                        "initial_option": "Default" if select_options else None,
                        "url": f"{wms_url}?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png"
                        f"&LEGEND_OPTIONS=bgColor:0xEFEFEF;labelMargin:10;dpi:100&LAYER={wms_layer_name_param}",
                    }
                )

        return legend

    @classmethod
    def build_geojson_layer(
        cls,
        geojson,
        layer_name,
        layer_title,
        layer_variable,
        layer_id="",
        visible=True,
        public=True,
        selectable=False,
        plottable=False,
        has_action=False,
        extent=None,
        popup_title=None,
        excluded_properties=None,
        show_download=False,
        renamable=False,
        removable=False,
        show_legend=True,
        legend_url=None,
        label_options=None,
    ):
        """
        Build an MVLayer object with supplied arguments.

        Args:
            geojson(dict): Python equivalent GeoJSON FeatureCollection.
            layer_name(str): Name of GeoServer layer (e.g.: workspace:a-unique-layer-name).
            layer_title(str): Title of MVLayer (e.g.: Model Boundaries).
            layer_variable(str): Variable type of the layer (e.g.: model_boundaries).
            layer_id(UUID, int, str): layer_id for non geoserver layer where layer_name may not be unique.
            visible(bool): Layer is visible when True. Defaults to True.
            public(bool): Layer is publicly accessible when app is running in Open Portal Mode if True. Defaults to True.
            selectable(bool): Enable feature selection. Defaults to False.
            plottable(bool): Enable "Plot" button on pop-up properties. Defaults to False.
            has_action(bool): Enable "Action" button on pop-up properties. Defaults to False.
            extent(list): Extent for the layer. Optional.
            popup_title(str): Title to display on feature popups. Defaults to layer title.
            excluded_properties(list): List of properties to exclude from feature popups.
            show_download(boolean): enable download geojson as shapefile. Default is False.
            renamable(bool): Show Rename option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            removable(bool): Show Remove option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            show_legend(bool): Show the legend for this layer when True and legends are enabled. Defaults to True.
            legend_url(str): URL of a legend image to display for the layer when legends are enabled.
            label_options(dict): Dictionary for labeling.  Possibilities include label_property (the name of the
                property to label), font (label font), text_align (alignment of the label), offset_x (x offset). Optional.

        Returns:
            MVLayer: the MVLayer object.
        """  # noqa: E501
        # Define default styles for layers
        style_map = cls.get_vector_style_map()

        # Bind geometry features to layer via layer name
        for feature in geojson["features"]:
            feature.setdefault("properties", {})
            feature["properties"]["layer_name"] = layer_name

        mv_layer = cls._build_mv_layer(
            layer_source="GeoJSON",
            layer_id=layer_id,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=layer_variable,
            options=geojson,
            extent=extent,
            visible=visible,
            public=public,
            selectable=selectable,
            plottable=plottable,
            has_action=has_action,
            popup_title=popup_title,
            excluded_properties=excluded_properties,
            style_map=style_map,
            show_download=show_download,
            renamable=renamable,
            removable=removable,
            show_legend=show_legend,
            legend_url=legend_url,
            label_options=label_options,
        )

        return mv_layer

    @classmethod
    def build_wms_layer(
        cls,
        endpoint,
        layer_name,
        layer_title,
        layer_variable,
        viewparams=None,
        env=None,
        visible=True,
        tiled=True,
        selectable=False,
        plottable=False,
        has_action=False,
        extent=None,
        public=True,
        geometry_attribute="geometry",
        layer_id="",
        excluded_properties=None,
        popup_title=None,
        color_ramp_division_kwargs=None,
        times=None,
        server_type="geoserver",
        cross_origin=None,
        styles=None,
        renamable=False,
        removable=False,
        show_legend=True,
        legend_url=None,
        cql_filter=None,
    ):
        """
        Build an WMS MVLayer object with supplied arguments.

        Args:
            endpoint(str): URL to GeoServer WMS interface.
            layer_name(str): Name of GeoServer layer (e.g.: workspace:a-unique-layer-name).
            layer_title(str): Title of MVLayer (e.g.: Model Boundaries).
            layer_variable(str): Variable type of the layer (e.g.: model_boundaries).
            layer_id(UUID, int, str): layer_id for non geoserver layer where layer_name may not be unique.
            viewparams(str): VIEWPARAMS string.
            env(str): ENV string.
            visible(bool): Layer is visible when True. Defaults to True.
            public(bool): Layer is publicly accessible when app is running in Open Portal Mode if True. Defaults to True.
            tiled(bool): Configure as tiled layer if True. Defaults to True.
            selectable(bool): Enable feature selection. Defaults to False.
            plottable(bool): Enable "Plot" button on pop-up properties. Defaults to False.
            has_action(bool): Enable "Action" button on pop-up properties. Defaults to False.
            extent(list): Extent for the layer. Optional.
            popup_title(str): Title to display on feature popups. Defaults to layer title.
            excluded_properties(list): List of properties to exclude from feature popups.
            geometry_attribute(str): Name of the geometry attribute. Defaults to "geometry".
            color_ramp_division_kwargs(dict): arguments from MapLayout.generate_custom_color_ramp_divisions
            times (list): List of time steps if layer is time-enabled. Times should be represented as strings in ISO 8601 format (e.g.: ["20210322T112511Z", "20210322T122511Z", "20210322T132511Z"]). Currently only supported in CesiumMapView.
            server_type (str): One of 'geoserver' or 'thredds'. Defaults to 'geoserver'.
            cross_origin (str): Value to pass to crossOrigin property. Defaults to None. See: https://openlayers.org/en/latest/apidoc/module-ol_source_TileWMS-TileWMS.html
            styles (str): Name of style to render the WMS. Defaults to None.
            renamable(bool): Show Rename option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            removable(bool): Show Remove option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            show_legend(bool): Show the legend for this layer when True and legends are enabled. Defaults to True.
            legend_url(str): URL of a legend image to display for the layer when legends are enabled.
            cql_filter(str): geoserver CQL filter string.

        Returns:
            MVLayer: the MVLayer object.
        """  # noqa: E501
        # Build params
        params = {"LAYERS": layer_name}

        if tiled:
            params.update({"TILED": True, "TILESORIGIN": "0.0,0.0"})

        if viewparams:
            params["VIEWPARAMS"] = viewparams

        if cql_filter:
            params["CQL_FILTER"] = cql_filter

        if styles:
            params["STYLES"] = styles

        if env:
            params["ENV"] = env

        if times:
            times = json.dumps(times)

        if color_ramp_division_kwargs:
            # Create color ramp and add them to ENV
            color_ramp_divisions = cls.generate_custom_color_ramp_divisions(
                **color_ramp_division_kwargs
            )
            if "ENV" in params.keys() and params["ENV"]:
                params["ENV"] += ";" + cls.build_param_string(**color_ramp_divisions)
            else:
                params["ENV"] = cls.build_param_string(**color_ramp_divisions)

        # Build options
        options = {
            "url": endpoint,
            "params": params,
            "serverType": server_type,
            "crossOrigin": cross_origin,
        }

        if tiled:
            options["tileGrid"] = cls.DEFAULT_TILE_GRID

        mv_layer = cls._build_mv_layer(
            layer_id=layer_id,
            layer_name=layer_name,
            layer_source="TileWMS" if tiled else "ImageWMS",
            layer_title=layer_title,
            layer_variable=layer_variable,
            options=options,
            extent=extent,
            visible=visible,
            public=public,
            selectable=selectable,
            plottable=plottable,
            has_action=has_action,
            popup_title=popup_title,
            excluded_properties=excluded_properties,
            geometry_attribute=geometry_attribute,
            times=times,
            renamable=renamable,
            removable=removable,
            show_legend=show_legend,
            legend_url=legend_url,
        )

        return mv_layer

    @classmethod
    def build_arc_gis_layer(
        cls,
        endpoint,
        layer_name,
        layer_title,
        layer_variable,
        layer_id=None,
        visible=True,
        selectable=False,
        extent=None,
        public=True,
        renamable=False,
        removable=False,
        show_legend=True,
        legend_url=None,
    ):
        """
        Build an AcrGIS Map Server MVLayer object with supplied arguments.

        Args:
            endpoint(str): Full ArcGIS REST URL for the layer (e.g.: "https://sampleserver1.arcgisonline.com/ArcGIS/rest/services/Specialty/ESRI_StateCityHighway_USA/MapServer").
            layer_name(str): Programmatic name of the layer (e.g.: "ESRI_StateCityHighway_USA").
            layer_title(str): Title of layer to display in Layer Picker (e.g.: "ESRI Highways").
            layer_variable(str): Variable type/class of the layer (e.g.: "highways").
            layer_id(UUID, int, str): layer_id for non geoserver layer where layer_name may not be unique.
            visible(bool): Layer is visible when True. Defaults to True.
            public(bool): Layer is publicly accessible when app is running in Open Portal Mode if True. Defaults to True.
            extent(list): Extent for the layer. Optional.
            renamable(bool): Show Rename option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            removable(bool): Show Remove option in layer context menu when True. Must implement the appropriate method to persist the change. Defaults to False.
            show_legend(bool): Show the legend for this layer when True and legends are enabled. Defaults to True.
            legend_url(str): URL of a legend image to display for the layer when legends are enabled.

        Returns:
            MVLayer: the MVLayer object.
        """  # noqa: E501
        # Build options
        mv_layer = cls._build_mv_layer(
            layer_id=layer_id,
            layer_name=layer_name,
            layer_source="TileArcGISRest",
            layer_title=layer_title,
            layer_variable=layer_variable,
            options={
                "url": endpoint,
                "params": {"LAYERS": "show:" + layer_name},
            },
            extent=extent,
            visible=visible,
            public=public,
            selectable=selectable,
            renamable=renamable,
            removable=removable,
            show_legend=show_legend,
            legend_url=legend_url,
        )

        return mv_layer

    @classmethod
    def build_custom_layer(
        cls,
        service_type,
        service_endpoint,
        layer_name,
        layer_id,
        layer_title,
        visible=True,
    ):
        """Rebuild a custom layer from saved attributes.

        Args:
            service_type (str): Type of map servce ("WMS" or "TileArcGISRest").
            service_endpoint (str): Endpoint of the map service.
            layer_name (str): Name of layer to render.add()
            layer_id (str): Unique id of the layer.add()
            layer_title (str): Display name of layer shown in legend and layer picker.
            visible (str): The layer will be displayed by default if True.

        Returns:
            MVLayer: the MVLayer object.
        """
        if service_type.lower() == "wms":
            return cls.build_wms_layer(
                endpoint=service_endpoint,
                server_type="thredds" if "thredds" in service_endpoint else "geoserver",
                layer_name=layer_name,
                layer_title=layer_title,
                layer_id=layer_id,
                layer_variable="custom",
                removable=True,
                visible=visible,
            )

        elif service_type.lower() == "tilearcgisrest":
            return cls.build_arc_gis_layer(
                endpoint=service_endpoint,
                layer_name=layer_name,
                layer_title=layer_title,
                layer_id=layer_id,
                layer_variable="custom",
                removable=True,
                visible=visible,
            )

    @classmethod
    def build_custom_layer_group(
        cls,
        display_name="Custom Layers",
        layers=None,
        layer_control="checkbox",
        visible=True,
        collapsed=False,
        renamable=False,
        removable=False,
    ):
        """Build the Custom Layers layer group.

        Args:
            layers(list<MVLayer>): List of layers to include in the layer group.
            layer_control(str): Type of control for layers. Either 'checkbox' or 'radio'. Defaults to checkbox.
            visible(bool): Whether layer group is initially visible. Defaults to True.
            collapsed(bool): Render layer group collapsed initially. Defaults to False.
            renamable(bool): Show Rename option in layer context menu when True.
            removable(bool): Show Remove option in layer context menu when True.

        Returns:
            dict: Layer group definition.
        """
        if layers is None:
            layers = []

        return cls.build_layer_group(
            id="custom_layers",
            display_name=display_name,
            layers=layers,
            layer_control=layer_control,
            visible=visible,
            collapsed=collapsed,
            renamable=renamable,
            removable=removable,
        )

    @classmethod
    def generate_custom_color_ramp_divisions(
        cls,
        min_value,
        max_value,
        num_divisions=10,
        value_precision=2,
        first_division=1,
        top_offset=0,
        bottom_offset=0,
        prefix="val",
        color_ramp=None,
        color_prefix="color",
        no_data_value=None,
    ):
        """
        Generate custom color ramp divisions.

        Args:
            min_value (float): minimum value.
            max_value (float): maximum value.
            num_divisions (int): number of divisions.
            value_precision (int): level of precision for legend values.
            first_division (int): first division number (defaults to 1).
            top_offset (float): offset from top of color ramp (defaults to 0).
            bottom_offset (float): offset from bottom of color ramp (defaults to 0).
            prefix (str): name of division variable prefix (i.e.: 'val' for pattern 'val1').
            color_ramp (str): color ramp name in COLOR_RAMPS dict. Options are 'Blue', 'Blue and Red', 'Flower Field', 'Galaxy Berries', 'Heat Map', 'Olive Harmony', 'Mother Earth', 'Rainforest Frogs', 'Retro FLow', or 'Sunset Fade'.
            color_prefix (str): name of color variable prefix (i.e.: 'color' for pattern 'color1').
            no_data_value (str): set no data value for the color ramp. (defaults to None).

        Returns:
            dict<name, value>: Color ramp division names and values.
        """  # noqa:E501
        divisions = {}

        # Equation of a Line
        max_div = first_division + num_divisions - 1
        min_div = first_division
        max_val = float(max_value - top_offset)
        min_val = float(min_value + bottom_offset)
        y2_minus_y1 = max_val - min_val
        x2_minus_x1 = max_div - min_div
        m = y2_minus_y1 / x2_minus_x1
        b = max_val - (m * max_div)

        for i in range(min_div, max_div + 1):
            divisions[f"{prefix}{i}"] = f"{(m * i + b):.{value_precision}f}"

            if color_ramp in cls.COLOR_RAMPS.keys():
                divisions[f"{color_prefix}{i}"] = (
                    f"{cls.COLOR_RAMPS[color_ramp][(i - first_division) % len(cls.COLOR_RAMPS[color_ramp])]}"
                )
            else:
                # use default color ramp
                divisions[f"{color_prefix}{i}"] = (
                    f"{cls.COLOR_RAMPS['Default'][(i - first_division) % len(cls.COLOR_RAMPS['Default'])]}"
                )
        if no_data_value is not None:
            divisions["val_no_data"] = no_data_value
        return divisions
