"""
********************************************************************************
* Name: paths.py
* Author: Scott Christensen
* Created On: April 2024
* Copyright: (c) Tethys Geospatial Foundation 2024
* License: BSD 2-Clause
********************************************************************************
"""

import os
import shutil
import logging
from pathlib import Path

from django.conf import settings
from django.utils.functional import wraps
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject

from tethys_quotas.utilities import passes_quota, _get_storage_units

from .workspace import (
    get_app_workspace_old,
    get_user_workspace_old,
)

log = logging.getLogger(f"tethys.{__name__}")


class TethysPath:
    """
    Defines objects that represent paths (directories) for apps and users.

    Args:
      path (Path): The path to a directory. Cannot be overwritten.
    """

    def __init__(self, path, read_only=False):
        """
        Constructor
        """
        self._path = Path(path).resolve()
        if self._path.is_file():
            raise ValueError(
                f"TethysPath objects can only be created for directories. {path} is a file."
            )
        # Create the path if it doesn't already exist
        self._path.mkdir(parents=True, exist_ok=True)

        self._read_only = read_only

    def __repr__(self):
        """
        Rendering
        """
        return '<TethysPath path="{0}">'.format(self._path)

    @property
    def path(self):
        # Note that this is different from TethysWorkspace in that it now returns a python Path object
        return self._path

    @property
    def read_only(self):
        return self._read_only

    def files(self, names_only=False):
        """
        Return a list of files (as Path objects by default) that are in the TethysPath directory.

        Args:
          names_only(bool): Returns list of filenames as strings when True. Defaults to False.

        Returns:
          list: A list of files in the TethysPath directory.

        **Examples:**

        .. code-block:: python

            # List of Path objects for each file
            tethys_path.files()

            # List of file names
            tethys_path.files(names_only=True)

        """
        path, dirs, files = next(os.walk(self.path))
        if names_only:
            return files
        return [self.path / f for f in files]

    def directories(self, names_only=False):
        """
        Return a list of directories (as Path objects by default) that are in the TethysPath directory.

        Args:
          names_only(bool): Returns list of directory names  as strings when True. Defaults to False.

        Returns:
          list: A list of directories in the TethysPath directory.

        **Examples:**

        .. code-block:: python

            # List Path objects for each directory
            tethys_path.directories()

            # List of directory names
            tethys_path.directories(names_only=True)

        """
        path, dirs, files = next(os.walk(self.path))
        if names_only:
            return dirs
        return [self.path / d for d in dirs]

    def clear(self, exclude=None, exclude_files=False, exclude_directories=False):
        """
        Remove all files and directories in the TethysPath directory.

        Args:
          exclude(iterable): A list or tuple of file and directory names to exclude from clearing operation.
          exclude_files(bool): Excludes all files from clearing operation when True. Defaults to False.
          exclude_directories(bool): Excludes all directories from clearing operation when True. Defaults to False.

        **Examples:**

        .. code-block:: python

            # Clear everything
            tethys_path.clear()

            # Clear directories only
            tethys_path.clear(exclude_files=True)

            # Clear files only
            tethys_path.clear(exclude_directories=True)

            # Clear all but specified files and directories
            tethys_path.clear(exclude=['file1.txt', '/full/path/to/directory1', 'directory2', '/full/path/to/file2.txt'])

        """
        if self.read_only:
            raise RuntimeError("Read only TethysPaths cannot be cleared")

        if exclude is None:
            exclude = list()

        files = self.files()

        if not exclude_files:
            for file in files:
                if file not in exclude and file.name not in exclude:
                    file.unlink()

        if not exclude_directories:
            directories = self.directories()
            for directory in directories:
                if directory not in exclude and directory.name not in exclude:
                    shutil.rmtree(directory)

    def remove(self, item):
        """
        Remove a file or directory from the TethysPath directory.

        Args:
          item(str | Path): Name, string path, or Path object of the item to remove from the TethysPath directory.

        **Examples:**

        .. code-block:: python

            tethys_path.remove('file.txt')
            tethys_path.remove('/full/path/to/file.txt')
            tethys_path.remove('relative/path/to/file.txt')
            tethys_path.remove('directory')
            tethys_path.remove('/full/path/to/directory')
            tethys_path.remove('relative/path/to/directory')
            tethys_path.remove(path_object)

        **Note:** Though you can specify relative paths, the ``remove()`` method will not allow you to back into other directories using "../" or similar notation. Furthermore, absolute paths given must contain the path of the tethys_path to be valid.

        """  # noqa: E501
        if self.read_only:
            raise RuntimeError("Cannot remove files from read-only TethysPaths")
        item = Path(item).resolve()

        # ensure item is a subpath of self.path (raises ValueError if not)
        item.relative_to(self.path)

        if item.is_dir():
            shutil.rmtree(item)
        elif item.is_file():
            item.unlink()

    def get_size(self, units="b"):
        """
        Get the size on disk of the TethysPath directory.

        Args:
            units (str): Disk size units. One of "byte", "bytes", "KB", "MB", "GB", "TB", or "PB". Defaults to "b" (bytes).

        Returns:
            float: size on disk of TethysPath directory.
        """
        total_size = 0
        for file in self.files():
            total_size += os.path.getsize(file)

        if units.lower() == "b":
            conversion_factor = 1
        else:
            storage_units = _get_storage_units()
            conversion_factor = [
                item[0] for item in storage_units if units.upper() in item[1]
            ][0]

        return total_size / conversion_factor


def _resolve_app_class(app_or_request, bypass_quota=False):
    """
    Returns an app class

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        bypass_quota (bool): Whether to check the app's workspace/media quota.

    Raises:
        ValueError: if app_or_request is not correct type.
        AssertionError: if `bypass_quota` is False and quota for the app workspace/media directory has been exceeded.


    Returns: The TethysAppBase subclass from `app_or_request`

    """
    from tethys_apps.base.app_base import TethysAppBase
    from tethys_apps.models import TethysApp
    from tethys_apps.utilities import get_active_app, get_app_class

    # Get app
    if isinstance(app_or_request, TethysAppBase) or (
        isinstance(app_or_request, type) and issubclass(app_or_request, TethysAppBase)
    ):
        app = app_or_request
    elif isinstance(app_or_request, HttpRequest):
        app = get_active_app(app_or_request, get_class=True)
    elif isinstance(app_or_request, TethysApp):
        app = get_app_class(app_or_request)
    else:
        raise ValueError(
            f'Argument "app_or_request" must be of type TethysAppBase, TethysApp, or HttpRequest: '
            f'"{type(app_or_request)}" given.'
        )

    if not bypass_quota:
        assert passes_quota(app, "app_workspace_quota")

    return app


def _resolve_username(user_or_request, bypass_quota=False):
    """

    Args:
        user_or_request (User or HttpRequest): Either an HttpRequest with active user session or Django User object.
        bypass_quota (bool): Whether to check the user's workspace/media quota.

    Raises:
        ValueError: if user_or_request is not correct type.
        AssertionError: if `bypass_quota` is False and quota for the user workspace/media directory has been exceeded.

    Returns: username of user or request.user

    """
    from django.contrib.auth.models import User

    # Get user
    if isinstance(user_or_request, User) or isinstance(
        user_or_request, SimpleLazyObject
    ):
        user = user_or_request
    elif isinstance(user_or_request, HttpRequest):
        user = user_or_request.user
    else:
        raise ValueError(
            f'Argument "user_or_request" must be of type HttpRequest or User: '
            f'"{type(user_or_request)}" given.'
        )

    if not bypass_quota:
        assert passes_quota(user, "user_workspace_quota")

    return user.username


def _get_app_workspace_root(app):
    """
    Gets the root workspace directory for an app. Uses TETHYS_WORKSPACES_ROOT setting.
    """
    return Path(settings.TETHYS_WORKSPACES_ROOT) / app.package


def _get_app_workspace(app_or_request, bypass_quota=False) -> TethysPath:
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        bypass_quota (bool): Whether to check the user's workspace/media quota.

    Raises:
        ValueError: if app_or_request is not correct type.
        AssertionError: if `bypass_quota` is False and quota for the app workspace/media directory has been exceeded.

    Returns: TethysPath representing the app workspace.

    """
    app = _resolve_app_class(app_or_request, bypass_quota=bypass_quota)
    return TethysPath(_get_app_workspace_root(app) / "app_workspace")


def get_app_workspace(app_or_request) -> TethysPath:
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.

    Raises:
        ValueError: if app_or_request is not correct type.
        AssertionError: if quota for the app workspace/media directory has been exceeded.

    Returns: TethysPath representing the app workspace.

    """
    if settings.USE_OLD_WORKSPACES_API:
        return get_app_workspace_old(app_or_request)

    return _get_app_workspace(app_or_request)


def _get_user_workspace(app_or_request, user_or_request, bypass_quota=False):
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        user_or_request (User or HttpRequest): Either an HttpRequest with active user session or Django User object.
        bypass_quota (bool): Whether to check the user's workspace/media quota.

    Raises:
        ValueError: if app_or_request or user_or_request are not correct types.
        AssertionError: if `bypass_quota` is False and quota for the user workspace/media directory has been exceeded.

    Returns: TethysPath representing the user workspace.

    """
    app = _resolve_app_class(app_or_request)
    username = _resolve_username(user_or_request, bypass_quota=bypass_quota)
    return TethysPath(_get_app_workspace_root(app) / "user_workspaces" / username)


def get_user_workspace(
    app_or_request,
    user_or_request,
    bypass_quota=False,
) -> TethysPath:
    """
    Get the dedicated user workspace for the given app. If an HttpRequest is given, the workspace of the logged-in user will be returned (i.e. request.user).

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        user_or_request (User or HttpRequest): Either an HttpRequest with active user session or Django User object.
        bypass_quota (bool): Whether to check the user's workspace/media quota.

    Raises:
        ValueError: if app_or_request or user_or_request are not correct types.
        AssertionError: if quota for the user workspace/media directory has been exceeded.

    Returns:
        TethysPath representing the user's workspace directory.

    .. code-block:: python

        import os
        from tethys_sdk.workspaces import get_user_workspace
        from .app import App

        def some_function(user):
            user_workspace = get_user_workspace(App, user)
            ...
    """  # noqa: E501
    if settings.USE_OLD_WORKSPACES_API:
        return get_user_workspace_old(app_or_request, user_or_request)

    return _get_user_workspace(app_or_request, user_or_request, bypass_quota)


def _get_app_media_root(app):
    """
    Gets the root media directory for an app. Uses MEDIA_ROOT setting.
    """
    return Path(settings.MEDIA_ROOT) / app.package


def _get_app_media(app_or_request, bypass_quota=False):
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        bypass_quota (bool): Whether to check the apps's workspace/media quota.

    Raises:
        ValueError: if app_or_request is not correct type.
        AssertionError: if `bypass_quota` is False and quota for the app workspace/media directory has been exceeded.


    Returns: TethysPath representing the media directory for the app.

    """
    app = _resolve_app_class(app_or_request, bypass_quota=bypass_quota)
    return TethysPath(_get_app_media_root(app) / "app")


def get_app_media(app_or_request):
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.

    Raises:
        ValueError: if app_or_request is not correct type.
        AssertionError: if quota for the app workspace/media directory has been exceeded.


    Returns: TethysPath representing the media directory for the app.

    """
    return _get_app_media(app_or_request)


def _get_user_media(app_or_request, username_or_request, bypass_quota=False):
    """
    Private method to get the user media path with a quota bypass so the quota handler can get the path.

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        username_or_request (User or HttpRequest):
            A User instance or an authenticated request to get the media directory for.
        bypass_quota (bool): Whether to check the user's workspace/media quota.

    Raises:
        ValueError: if app_or_request or user_or_request are not correct types.
        AssertionError: if `bypass_quota` is False and quota for the user workspace/media directory has been exceeded.

    Returns: TethysPath representing the user's media directory for the app.

    """
    app = _resolve_app_class(app_or_request)
    username = _resolve_username(username_or_request, bypass_quota=bypass_quota)
    return TethysPath(_get_app_media_root(app) / "user" / username)


def get_user_media(app_or_request, username_or_request):
    """

    Args:
        app_or_request (TethysAppBase, TethysApp, or HttpRequest): The Tethys app class that is defined in app.py or HttpRequest to app endpoint.
        username_or_request (User or HttpRequest):
            A User instance or an authenticated request to get the media directory for.

    Raises:
        ValueError: if app_or_request or user_or_request are not correct types.
        AssertionError: if quota for the user workspace/media directory has been exceeded.

    Returns: TethysPath representing the user's media directory for the app.

    """
    return _get_user_media(app_or_request, username_or_request)


def get_app_resources(app_or_request):
    """
    Gets the resources directory of an app or extension as a read-only TethysPath

    Args:
        app_or_request (TethysAppBase, TethysApp, TethysExtensionBase, TethysExtension, or HttpRequest):
            The Tethys app class that is defined in app.py (or extension class in ext.py) or HttpRequest to app endpoint.

    Raises:
        ValueError: if app_or_request is not correct type.

    Returns: TethysPath representing the public directory of the app (or extension).

    """
    app = _resolve_app_class(app_or_request, bypass_quota=True)
    return app.resources_path


def get_app_public(app_or_request):
    """
    Gets the public directory of an app or extension as a read-only TethysPath

    Args:
        app_or_request (TethysAppBase, TethysApp, TethysExtensionBase, TethysExtension, or HttpRequest):
            The Tethys app class that is defined in app.py (or extension class in ext.py) or HttpRequest to app endpoint.

    Raises:
        ValueError: if app_or_request is not correct type.

    Returns: TethysPath representing the public directory of the app (or extension).

    """
    app = _resolve_app_class(app_or_request, bypass_quota=True)
    return app.public_path


def _add_path_decorator(argument_name):
    """Creates a decorator that adds the TethysPath for `argument_name`.

    Args:
        argument_name (str): The name of the argument to add to the controller that represents a TethysPath.
            Must be one of (app_workspace, user_workspace, app_media, user_media, app_public, app_resources).

    Returns: A decorator for a controller function.

    """

    def decorator(controller):
        @wraps(controller)
        def wrapper(*args, **kwargs):
            request = None
            for _, arg in enumerate(args):
                if isinstance(arg, HttpRequest):
                    request = arg
                    break

            if request is None:
                raise ValueError(
                    f"No request given. The {argument_name} decorator only works on controllers."
                )

            func_args = [request]
            if "user" in argument_name:
                func_args.append(request.user)

            func = globals()[f"get_{argument_name}"]
            the_path = func(*func_args)

            return controller(*args, **{argument_name: the_path}, **kwargs)

        return wrapper

    return decorator
