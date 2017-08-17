"""
********************************************************************************
* Name: utilities.py
* Author: Nathan Swain
* Created On: 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""
import logging
import os
from collections import OrderedDict as SortedDict

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join
from tethys_apps.app_harvester import SingletonAppHarvester
from tethys_apps.base import permissions
from tethys_apps.models import TethysApp

tethys_log = logging.getLogger('tethys.' + __name__)


def register_app_permissions():
    """
    Register and sync the app permissions.
    """
    from guardian.shortcuts import assign_perm, remove_perm, get_perms
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission, Group

    # Get the apps
    harvester = SingletonAppHarvester()
    apps = harvester.apps
    all_app_permissions = {}
    all_groups = {}

    for app in apps:
        perms = app.permissions()

        # Name spaced prefix for app permissions
        # e.g. my_first_app:view_things
        # e.g. my_first_app | View things
        perm_codename_prefix = app.package + ':'
        perm_name_prefix = app.package + ' | '

        if perms is not None:
            # Thing is either a Permission or a PermissionGroup object

            for thing in perms:
                # Permission Case
                if isinstance(thing, permissions.Permission):
                    # Name space the permissions and add it to the list
                    permission_codename = perm_codename_prefix + thing.name
                    permission_name = perm_name_prefix + thing.description
                    all_app_permissions[permission_codename] = permission_name

                # PermissionGroup Case
                elif isinstance(thing, permissions.PermissionGroup):
                    # Record in dict of groups
                    group_permissions = []
                    group_name = perm_codename_prefix + thing.name

                    for perm in thing.permissions:
                        # Name space the permissions and add it to the list
                        permission_codename = perm_codename_prefix + perm.name
                        permission_name = perm_name_prefix + perm.description
                        all_app_permissions[permission_codename] = permission_name
                        group_permissions.append(permission_codename)

                    # Store all groups for all apps
                    all_groups[group_name] = {'permissions': group_permissions, 'app_package': app.package}

    # Get the TethysApp content type
    tethys_content_type = ContentType.objects.get(
        app_label='tethys_apps',
        model='tethysapp'
    )

    # Remove any permissions that no longer exist
    db_app_permissions = Permission.objects.filter(content_type=tethys_content_type).all()

    for db_app_permission in db_app_permissions:
        # Delete the permission if the permission is no longer required by an app
        if db_app_permission.codename not in all_app_permissions:
            db_app_permission.delete()

    # Create permissions that need to be created
    for perm in all_app_permissions:
        # Create permission if it doesn't exist
        try:
            # If permission exists, update it
            p = Permission.objects.get(codename=perm)

            p.name = all_app_permissions[perm]
            p.content_type = tethys_content_type
            p.save()

        except Permission.DoesNotExist:
            p = Permission(
                name=all_app_permissions[perm],
                codename=perm,
                content_type=tethys_content_type
            )
            p.save()

    # Remove any groups that no longer exist
    db_groups = Group.objects.all()
    db_apps = TethysApp.objects.all()
    db_app_names = [db_app.package for db_app in db_apps]

    for db_group in db_groups:
        db_group_name_parts = db_group.name.split(':')

        # Only perform maintenance on groups that belong to Tethys Apps
        if (len(db_group_name_parts) > 1) and (db_group_name_parts[0] in db_app_names):

            # Delete groups that is no longer required by an app
            if db_group.name not in all_groups:
                db_group.delete()

    # Create groups that need to be created
    for group in all_groups:
        # Look up the app
        db_app = TethysApp.objects.get(package=all_groups[group]['app_package'])

        # Create group if it doesn't exist
        try:
            # If it exists, update the permissions assigned to it
            g = Group.objects.get(name=group)

            # Get the permissions for the group and remove all of them
            perms = get_perms(g, db_app)

            for p in perms:
                remove_perm(p, g, db_app)

            # Assign the permission to the group and the app instance
            for p in all_groups[group]['permissions']:
                assign_perm(p, g, db_app)

        except Group.DoesNotExist:
            # Create a new group
            g = Group(name=group)
            g.save()

            # Assign the permission to the group and the app instance
            for p in all_groups[group]['permissions']:
                assign_perm(p, g, db_app)


def get_app_url_patterns():
    """
    Generate the url pattern lists for each app and namespace them accordingly.
    """

    # Get controllers list from app harvester
    harvester = SingletonAppHarvester()
    apps = harvester.apps
    app_url_patterns = dict()

    for app in apps:
        app_url_patterns.update(app.url_patterns)

    return app_url_patterns


def get_directories_in_tethys_apps(directory_names, with_app_name=False):
    # Determine the tethysapp directory
    tethysapp_dir = safe_join(os.path.abspath(os.path.dirname(__file__)), 'tethysapp')

    # Assemble a list of tethysapp directories
    tethysapp_contents = os.listdir(tethysapp_dir)
    tethysapp_match_dirs = []

    for item in tethysapp_contents:
        item_path = safe_join(tethysapp_dir, item)

        # Check each directory combination
        for directory_name in directory_names:
            # Only check directories
            if os.path.isdir(item_path):
                match_dir = safe_join(item_path, directory_name)

                if match_dir not in tethysapp_match_dirs and os.path.isdir(match_dir):
                    if not with_app_name:
                        tethysapp_match_dirs.append(match_dir)
                    else:
                        tethysapp_match_dirs.append((item, match_dir))

    return tethysapp_match_dirs


class TethysAppsStaticFinder(BaseFinder):
    """
    A static files finder that looks in each app in the tethysapp directory for static files.
    This finder search for static files in a directory called 'public' or 'static'.
    """

    def __init__(self, apps=None, *args, **kwargs):
        # List of locations with static files
        self.locations = get_directories_in_tethys_apps(('static', 'public'), with_app_name=True)

        # Maps dir paths to an appropriate storage instance
        self.storages = SortedDict()

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage

        super(TethysAppsStaticFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the Tethys apps static or public directories
        """
        matches = []
        for prefix, root in self.locations:
            matched_path = self.find_location(root, path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]
        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


def get_active_app(request=None, url=None):
    """
    Get the active TethysApp object based on the request or URL.
    """
    apps_root = 'apps'

    if request is not None:
        the_url = request.path
    elif url is not None:
        the_url = url
    else:
        return None

    url_parts = the_url.split('/')
    app = None

    # Find the app key
    if apps_root in url_parts:
        # The app root_url is the path item following (+1) the apps_root item
        app_root_url_index = url_parts.index(apps_root) + 1
        app_root_url = url_parts[app_root_url_index]

        if app_root_url:
            try:
                # Get the app from the database
                app = TethysApp.objects.get(root_url=app_root_url)
            except ObjectDoesNotExist:
                tethys_log.warning('Could not locate app with root url "{0}".'.format(app_root_url))
            except MultipleObjectsReturned:
                tethys_log.warning('Multiple apps found with root url "{0}".'.format(app_root_url))
    return app
