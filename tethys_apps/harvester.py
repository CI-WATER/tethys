"""
********************************************************************************
* Name: app_harvester.py
* Author: Nathan Swain and Scott Christensen
* Created On: August 19, 2013
* Copyright: (c) Brigham Young University 2013
* License: BSD 2-Clause
********************************************************************************
"""

import inspect
import logging
import pkgutil

from django.db.utils import ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from tethys_apps.base import TethysAppBase, TethysExtensionBase
from tethys_apps.base.testing.environment import is_testing_environment

tethys_log = logging.getLogger("tethys." + __name__)


class SingletonHarvester:
    """
    Collects information for initiating apps
    """

    extensions = []
    extension_modules = {}
    app_modules = {}
    apps = []
    _instance = None
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

    def harvest(self):
        """
        Harvest apps and extensions.
        """
        self.harvest_extensions()
        self.harvest_apps()

    def harvest_extensions(self):
        """
        Searches for and loads Tethys extensions.
        """
        try:
            if not is_testing_environment():
                print(self.BLUE + "Loading Tethys Extensions..." + self.ENDC)

            import tethysext

            tethys_extensions = dict()
            for _, modname, ispkg in pkgutil.iter_modules(tethysext.__path__):
                if ispkg:
                    tethys_extensions[modname] = "tethysext.{}".format(modname)
            self._harvest_extension_instances(tethys_extensions)
        except Exception:
            """DO NOTHING"""

    def harvest_apps(self):
        """
        Searches the apps package for apps
        """
        # Notify user harvesting is taking place

        try:
            if not is_testing_environment():
                print(self.BLUE + "Loading Tethys Apps..." + self.ENDC)

            import tethysapp

            tethys_apps = dict()
            for _, modname, ispkg in pkgutil.iter_modules(tethysapp.__path__):
                if ispkg:
                    tethys_apps[modname] = "tethysapp.{}".format(modname)

            # Harvest App Instances
            self._harvest_app_instances(tethys_apps)

        except Exception:
            """DO NOTHING"""

    def get_url_patterns(self, url_namespaces=None):
        """
        Generate the url pattern lists for each app and namespace them accordingly.
        """
        app_url_patterns = dict()
        ext_url_patterns = dict()
        ws_url_patterns = dict()
        apps = self.apps
        if url_namespaces:
            apps = [app for app in apps if app.url_namespace in url_namespaces]

        for app in apps:
            app_url_patterns.update(app.url_patterns["http"])

        for app in apps:
            ws_url_patterns.update(app.url_patterns["websocket"])

        for extension in self.extensions:
            ext_url_patterns.update(extension.url_patterns["http"])

        url_patterns = {
            "app_url_patterns": app_url_patterns,
            "ext_url_patterns": ext_url_patterns,
            "ws_url_patterns": ws_url_patterns,
        }

        return url_patterns

    def get_handler_patterns(self, url_namespaces=None):
        """
        Generate the url handler pattern lists for each app and namespace them accordingly.
        """
        http_handler_patterns = dict()
        ws_handler_patterns = dict()
        apps = self.apps
        if url_namespaces:
            apps = [app for app in apps if app.url_namespace in url_namespaces]

        for app in apps:
            http_handler_patterns.update(app.handler_patterns["http"])

        for app in apps:
            ws_handler_patterns.update(app.handler_patterns["websocket"])

        handler_patterns = {
            "http_handler_patterns": http_handler_patterns,
            "ws_handler_patterns": ws_handler_patterns,
        }

        return handler_patterns

    def __new__(cls):
        """
        Make App Harvester a Singleton
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    @staticmethod
    def _validate_extension(extension):
        """
        Validate the given extension.
        Args:
            extension(module_obj): ext module object of the Tethys extension.

        Returns:
            module_obj or None: returns validated module object or None if not valid.
        """
        return extension

    @staticmethod
    def _validate_app(app):
        """
        Validate the app data that needs to be validated. Returns either the app if valid or None if not valid.
        """
        # Remove prepended slash if included
        if app.icon != "" and app.icon[0] == "/":
            app.icon = app.icon[1:]

        # Validate color
        if app.color != "" and app.color[0] != "#":
            # Add hash
            app.color = "#{0}".format(app.color)

        # Must be 6 or 3 digit hex color (7 or 4 with hash symbol)
        if len(app.color) != 7 and len(app.color) != 4:
            app.color = ""

        return app

    def _harvest_extension_instances(self, extension_packages):
        """
        Locate the extension class, instantiate it, and save for later use.

        Arg:
            extension_packages(dict<name, extension_package>): Dictionary where keys are the name of the extension and value is the extension package module object.
        """  # noqa:E501
        valid_ext_instances = []
        valid_extension_modules = {}
        loaded_extensions = []

        for extension_name, extension_package in extension_packages.items():
            try:
                # Import the "ext" module from the extension package
                ext_module = __import__(extension_package + ".ext", fromlist=[""])

                # Retrieve the members of the ext_module and iterate through
                # them to find the the class that inherits from TethysExtensionBase.
                for name, obj in inspect.getmembers(ext_module):
                    try:
                        # issubclass() will fail if obj is not a class
                        if (issubclass(obj, TethysExtensionBase)) and (
                            obj is not TethysExtensionBase
                        ):
                            # Assign a handle to the class
                            ExtensionClass = getattr(ext_module, name)

                            # Instantiate app and validate
                            ext_instance = ExtensionClass()
                            validated_ext_instance = self._validate_extension(
                                ext_instance
                            )

                            # sync app with Tethys db
                            ext_instance.sync_with_tethys_db()

                            # compile valid apps
                            if validated_ext_instance:
                                valid_ext_instances.append(validated_ext_instance)
                                valid_extension_modules[extension_name] = (
                                    extension_package
                                )

                                # Notify user that the app has been loaded
                                loaded_extensions.append(extension_name)

                            # We found the extension class so we're done
                            break

                    except TypeError:
                        continue
            except Exception:
                tethys_log.exception(
                    "Extension {0} not loaded because of the following error:".format(
                        extension_package
                    )
                )
                continue

        # Save valid apps
        self.extensions = valid_ext_instances
        self.extension_modules = valid_extension_modules

        # Update user
        if not is_testing_environment():
            print(
                self.BLUE
                + "Tethys Extensions Loaded: "
                + self.ENDC
                + "{0}".format(", ".join(loaded_extensions))
                + "\n"
            )

    def _harvest_app_instances(self, app_packages_list):
        """
        Search each app package for the app.py module. Find the AppBase class in the app.py
        module and instantiate it. Save the list of instantiated AppBase classes.
        """
        valid_app_instance_list = []
        valid_app_modules = {}
        loaded_apps = []
        for app_name, app_package in app_packages_list.items():
            # Skip these things
            if app_package in [
                "__init__.py",
                "__init__.pyc",
                ".gitignore",
                ".DS_Store",
            ]:
                continue

            try:
                # Import the app.py module from the custom app package programmatically
                # (e.g.: apps.apps.<custom_package>.app)

                app_module = __import__(app_package + ".app", fromlist=[""])

                for name, obj in inspect.getmembers(app_module):
                    # Retrieve the members of the app_module and iterate through
                    # them to find the class that inherits from AppBase.
                    try:
                        # issubclass() will fail if obj is not a class
                        if (issubclass(obj, TethysAppBase)) and (
                            obj is not TethysAppBase
                        ):
                            # Assign a handle to the class
                            AppClass = getattr(app_module, name)

                            # Instantiate app and validate
                            app_instance = AppClass()
                            validated_app_instance = self._validate_app(app_instance)

                            # sync app with Tethys db
                            app_instance.sync_with_tethys_db()

                            # load/validate app url patterns
                            try:
                                app_instance.url_patterns
                            except Exception:
                                tethys_log.exception(
                                    "App {0} not loaded because of an issue with loading urls:".format(
                                        app_package
                                    )
                                )
                                app_instance.remove_from_db()
                                continue

                            # load/validate app handler patterns
                            try:
                                app_instance.handler_patterns
                            except Exception:
                                tethys_log.exception(
                                    "App {0} not loaded because of an issue with loading handlers:".format(
                                        app_package
                                    )
                                )
                                app_instance.remove_from_db()
                                continue

                            # register app permissions
                            try:
                                app_instance.register_app_permissions()
                            except ProgrammingError:
                                tethys_log.warning(
                                    "Unable to register app permissions. django_content_type "
                                    "table does not exist"
                                )
                            except ObjectDoesNotExist as e:
                                tethys_log.warning(e)

                            # compile valid apps
                            if validated_app_instance:
                                valid_app_modules[app_name] = app_package
                                valid_app_instance_list.append(validated_app_instance)

                                # Notify user that the app has been loaded
                                loaded_apps.append(app_name)

                            # We found the app class so we're done
                            break

                    except TypeError:
                        continue
            except Exception:
                tethys_log.exception(
                    "App {0} not loaded because of the following error:".format(
                        app_package
                    )
                )
                continue

        # Save valid apps
        self.apps = valid_app_instance_list
        self.app_modules = valid_app_modules

        # Update user
        if not is_testing_environment():
            print(
                self.BLUE
                + "Tethys Apps Loaded: "
                + self.ENDC
                + "{0}".format(", ".join(loaded_apps))
                + "\n"
            )
