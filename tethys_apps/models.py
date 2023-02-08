"""
********************************************************************************
* Name: models.py
* Author: Nathan Swain
* Created On: 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""
import yaml
import sqlalchemy
import os
from django.core import signing
from django.core.signing import Signer
from django.dispatch import receiver
import logging
import uuid
import json
import django.dispatch
from django.db import models
from django.core.exceptions import ValidationError
from model_utils.managers import InheritanceManager
from tethys_apps.exceptions import (
    TethysAppSettingNotAssigned,
    PersistentStorePermissionError,
    PersistentStoreInitializerError,
)
from sqlalchemy.orm import sessionmaker
from tethys_apps.base.mixins import TethysBaseMixin
from tethys_compute.models.condor.condor_scheduler import CondorScheduler
from tethys_compute.models.dask.dask_scheduler import DaskScheduler
from tethys_compute.models.scheduler import Scheduler
from tethys_sdk.testing import is_testing_environment, get_test_db_name
from django.contrib.auth.hashers import check_password

from tethys_apps.base.function_extractor import TethysFunctionExtractor
from tethys_apps.utilities import get_tethys_home_dir, get_active_app

log = logging.getLogger("tethys")

try:
    from tethys_services.models import (
        DatasetService,
        SpatialDatasetService,
        WebProcessingService,
        PersistentStoreService,
    )
except RuntimeError:  # pragma: no cover
    log.exception("An error occurred while trying to import tethys service models.")


class TethysApp(models.Model, TethysBaseMixin):
    """
    DB Model for Tethys Apps
    """

    # The package is enforced to be unique by the file system
    package = models.CharField(max_length=200, unique=True, default="")

    # Portal admin first attributes
    name = models.CharField(max_length=200, default="")
    description = models.TextField(max_length=1000, blank=True, default="")
    enable_feedback = models.BooleanField(default=False)
    feedback_emails = models.JSONField(default=list, null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True, default="")
    enabled = models.BooleanField(default=True)
    show_in_apps_library = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    # Developer first attributes
    index = models.CharField(max_length=200, default="")
    icon = models.CharField(max_length=200, default="")
    root_url = models.CharField(max_length=200, default="")
    color = models.CharField(max_length=10, default="")

    class Meta:
        verbose_name = "Tethys App"
        verbose_name_plural = "Installed Apps"

    def __str__(self):
        return self.name

    def add_settings(self, setting_list):
        """
        Associate setting with app in database
        """
        # breakpoint()
        if setting_list is not None:
            for setting in setting_list:
                # Don't add the same setting twice
                if self.settings_set.filter(name=setting.name):
                    continue

                # Associate setting with this app
                setting.tethys_app = self
                setting.save()

    def sync_settings(self, setting_list, existing_settings):
        """
        Ensure that all new settings are added to the db and obsolete settings are removed.
        Args:
            setting_list: List of current settings (as defined in app.py).
            existing_settings: List of existing settings in the DB.
        """
        # breakpoint()
        if setting_list is not None:
            self.add_settings(setting_list)
            setting_names = [setting.name for setting in setting_list]
            for setting in existing_settings:
                # Do not remove dynamically craeted settings
                if getattr(setting, "dynamic", False) and setting.dynamic:
                    continue

                if setting.name not in setting_names:
                    setting.delete()

    @property
    def settings(self):
        return self.settings_set.select_subclasses()

    @property
    def custom_settings(self):
        return self.settings_set.exclude(customsetting__isnull=True).select_subclasses(
            "customsetting"
        ).select_subclasses()

    @property
    def dataset_service_settings(self):
        return self.settings_set.exclude(
            datasetservicesetting__isnull=True
        ).select_subclasses("datasetservicesetting")

    @property
    def spatial_dataset_service_settings(self):
        return self.settings_set.exclude(
            spatialdatasetservicesetting__isnull=True
        ).select_subclasses("spatialdatasetservicesetting")

    @property
    def wps_services_settings(self):
        return self.settings_set.exclude(
            webprocessingservicesetting__isnull=True
        ).select_subclasses("webprocessingservicesetting")

    @property
    def scheduler_settings(self):
        return self.settings_set.exclude(
            schedulersetting__isnull=True
        ).select_subclasses("schedulersetting")

    @property
    def persistent_store_connection_settings(self):
        return self.settings_set.exclude(
            persistentstoreconnectionsetting__isnull=True
        ).select_subclasses("persistentstoreconnectionsetting")

    @property
    def persistent_store_database_settings(self):
        return self.settings_set.exclude(
            persistentstoredatabasesetting__isnull=True
        ).select_subclasses("persistentstoredatabasesetting")

    @property
    def configured(self):
        required_settings = [s for s in self.settings if s.required]
        for setting in required_settings:
            try:
                setting.get_value()
            except TethysAppSettingNotAssigned:
                return False
        return True


class TethysExtension(models.Model, TethysBaseMixin):
    """
    DB Model for Tethys Extension
    """

    # The package is enforced to be unique by the file system
    package = models.CharField(max_length=200, unique=True, default="")

    # Portal admin first attributes
    name = models.CharField(max_length=200, default="")
    description = models.TextField(max_length=1000, blank=True, default="")

    # Developer first attributes
    root_url = models.CharField(max_length=200, default="")

    # Portal admin only attributes
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tethys Extension"
        verbose_name_plural = "Installed Extensions"

    def __str__(self):
        return self.name


class TethysAppSetting(models.Model):
    """
    DB Model for Tethys App Settings
    """

    objects = InheritanceManager()

    tethys_app = models.ForeignKey(
        TethysApp, on_delete=models.CASCADE, related_name="settings_set"
    )
    name = models.CharField(max_length=200, default="")
    description = models.TextField(max_length=1000, blank=True, default="")
    required = models.BooleanField(default=True)
    initializer = models.CharField(max_length=1000, default="")
    initialized = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def initializer_function(self):
        """
        The function pointed to by the initializer attribute.

        Returns:
            A handle to a Python function that will initialize the database or None if function is not valid.
        """
        func_ext = TethysFunctionExtractor(self.initializer)
        return func_ext.function

    def initialize(self):
        """
        Initialize.
        """
        self.initializer_function(self.initialized)
        self.initialized = True

    def get_value(self, *args, **kwargs):
        raise NotImplementedError()



class CustomSetting(TethysAppSetting):
    # value = models.CharField(max_length=1024, blank=True, default="")
    # default = models.CharField(max_length=1024, blank=True, default="")
    objects = InheritanceManager()
    type_custom_setting = models.CharField(max_length=1024, blank=True, default="")
    def get_value(self):
        pass

class CustomSecretSetting(CustomSetting):
    value = models.CharField(max_length=1024, blank=True, default="")
    def clean(self):
        """
        Validate prior to saving changes.
        """        

        if self.value == "" and self.required:
            raise ValidationError("Required.")
   
        if self.value != "" :
            try:
                TETHYS_HOME = get_tethys_home_dir()
                signer = Signer()
                if not os.path.exists(os.path.join(TETHYS_HOME, "secrets.yml")):
                    self.value = signer.sign_object(self.value)
                else:   
                    with open(os.path.join(TETHYS_HOME, "secrets.yml")) as secrets_yaml:
                        secret_app_settings = yaml.safe_load(secrets_yaml).get("secrets", {}) or {}
                        if bool(secret_app_settings):
                            if self.tethys_app.package in secret_app_settings:
                                if 'custom_settings_salt_strings' in secret_app_settings[self.tethys_app.package]:
                                    app_specific_settings = secret_app_settings[self.tethys_app.package]['custom_settings_salt_strings']
                                    if self.name in app_specific_settings:
                                        app_custom_setting_salt_string = app_specific_settings[self.name]
                                        if app_custom_setting_salt_string != '':
                                            signer = Signer(salt=app_custom_setting_salt_string)
                                        
                                        self.value = signer.sign_object(self.value)
                                    else:
                                        self.value = signer.sign_object(self.value)

                        else:
                            log.info(
                                "There is not a an apps portion in the secrets.yml, please create one by running the following command"
                            )
                            self.value = signer.sign_object(self.value)

            except Exception:
                raise ValidationError("Validation Error for Secret Custom Setting")
    def get_value(self):
        """
        Get the value, automatically casting it to the correct type.
        """
        # breakpoint()

        if self.value == "" or self.value is None:
            if self.required:
                raise TethysAppSettingNotAssigned(
                    f'The required setting "{self.name}" for app "{self.tethys_app.package}":'
                    f"has not been assigned."
                )

            # None is a valid value to return in the case the value has not been set for this setting type
            return None

        TETHYS_HOME = get_tethys_home_dir()
        signer = Signer()
        secret_unsigned = ''
        # breakpoint()
        
        try:
            if not os.path.exists(os.path.join(TETHYS_HOME, "secrets.yml")):
                secret_unsigned = signer.unsign_object(f'{self.value}')
            else:  
                with open(os.path.join(TETHYS_HOME, "secrets.yml")) as secret_yaml:
                    secrets_app_settings = yaml.safe_load(secret_yaml).get("secrets", {}) or {}
                    if bool(secrets_app_settings):
                        app_specific_settings = secrets_app_settings[self.tethys_app.package]['custom_settings_salt_strings']
                        if self.name in app_specific_settings:
                            app_custom_setting_salt_string = app_specific_settings[self.name]
                            if app_custom_setting_salt_string != '':
                                signer = Signer(salt=app_custom_setting_salt_string)
                            secret_unsigned= signer.unsign_object(f'{self.value}')
                        else:
                            secret_unsigned = signer.unsign_object(f'{self.value}')

                    else:
                        log.info(
                            "There is not a an apps portion in the secrets.yml, please create one by running the following command"
                        )
                        secret_unsigned = signer.unsign_object(f'{self.value}')
                
        except signing.BadSignature:

            raise TethysAppSettingNotAssigned(
                f'The salt string for the setting {self.name} has been changed or lost, please enter the secret custom settings in the application settings again.'
            )

        except Exception:
            log.exception(
                "There was an error while attempting to read the settings from the secrets.yml file."
            )

        return secret_unsigned


class CustomSimpleSetting(CustomSetting):
    """
    Used to define a Custom Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        type(enum): The type of the custom setting. Either CustomSetting.TYPE_STRING, CustomSetting.TYPE_INTEGER, CustomSetting.TYPE_FLOAT, CustomSetting.TYPE_BOOLEAN, CustomSetting.TYPE_UUID
        description(str): Short description of the setting.
        required(bool): A value will be required if True.
        default(str): Value as a string that may be provided as a default.

    **Example:**

    ::

        from tethys_sdk.app_settings import CustomSetting

        default_name_setting = CustomSetting(
            name='default_name',
            type=CustomSetting.TYPE_STRING
            description='Default model name.',
            required=True,
            default="Name_123"
        )

        max_count_setting = CustomSetting(
            name='max_count',
            type=CustomSetting.TYPE_INTEGER,
            description='Maximum allowed count in a method.',
            required=False
        )

        change_factor_setting = CustomSetting(
            name='change_factor',
            type=CustomSetting.TYPE_FLOAT,
            description='Change factor that is applied to some process.',
            required=True
        )

        enable_feature_setting = CustomSetting(
            name='enable_feature',
            type=CustomSetting.TYPE_BOOLEAN,
            description='Enable this feature when True.',
            required=True
        )

        feature_id_setting = CustomSetting(
            name='feature_id',
            type=CustomSetting.TYPE_UUID,
            description='Feature ID.',
            required=True
        )

    """  # noqa: E501

    TYPE_STRING = "STRING"
    TYPE_INTEGER = "INTEGER"
    TYPE_FLOAT = "FLOAT"
    TYPE_BOOLEAN = "BOOLEAN"
    TYPE_UUID = "UUID"

    VALID_TYPES = (TYPE_STRING, TYPE_INTEGER, TYPE_FLOAT, TYPE_BOOLEAN, TYPE_UUID)
    VALID_BOOL_STRINGS = ("true", "false", "yes", "no", "t", "f", "y", "n", "1", "0")
    TRUTHY_BOOL_STRINGS = ("true", "yes", "t", "y", "1")
    TYPE_CHOICES = (
        (TYPE_STRING, "String"),
        (TYPE_INTEGER, "Integer"),
        (TYPE_FLOAT, "Float"),
        (TYPE_BOOLEAN, "Boolean"),
        (TYPE_UUID, "UUID"),
    )
    value = models.CharField(max_length=1024, blank=True, default="")
    default = models.CharField(max_length=1024, blank=True, default="")

    type = models.CharField(max_length=200, choices=TYPE_CHOICES, default=TYPE_STRING)

    def clean(self):
        """
        Validate prior to saving changes.
        """        
        if self.default != "":
            if self.value == "":
                self.value = self.default
        else:
            if self.value == "" and self.required:
                raise ValidationError("Required.")

        if self.value != "" and self.type == self.TYPE_FLOAT:
            try:
                float(self.value)
            except Exception:
                raise ValidationError("Value must be a float.")

        elif self.value != "" and self.type == self.TYPE_INTEGER:
            try:
                int(self.value)
            except Exception:
                raise ValidationError("Value must be an integer.")

        elif self.value != "" and self.type == self.TYPE_BOOLEAN:
            if self.value.lower() not in self.VALID_BOOL_STRINGS:
                raise ValidationError("Value must be a boolean.")

        elif self.value != "" and self.type == self.TYPE_UUID:
            try:
                uuid.UUID(self.value)
            except Exception:
                raise ValidationError("Value must be a uuid.")

    def get_value(self):
        # breakpoint()
        """
        Get the value, automatically casting it to the correct type.
        """
        if self.default != "":
            if self.value == "":
                self.value = self.default

        if self.value == "" or self.value is None:
            if self.required:
                raise TethysAppSettingNotAssigned(
                    f'The required setting "{self.name}" for app "{self.tethys_app.package}":'
                    f"has not been assigned."
                )

            # None is a valid value to return in the case the value has not been set for this setting type
            return None

        if self.type == self.TYPE_STRING:
            return self.value

        if self.type == self.TYPE_FLOAT:
            return float(self.value)

        if self.type == self.TYPE_INTEGER:
            return int(self.value)

        if self.type == self.TYPE_BOOLEAN:
            return self.value.lower() in self.TRUTHY_BOOL_STRINGS

        if self.type == self.TYPE_UUID:
            return uuid.UUID(self.value)

class CustomJSONSetting(CustomSetting):
    value = models.JSONField(blank=True, default=dict)
    default = models.JSONField(blank=True, default=dict)
    def clean(self):
        """
        Validate prior to saving changes.
        """        
        if self.default:
            if not self.value:
                self.value = self.default
        else:
            if not self.default and self.required:
                raise ValidationError("Required.")
                
        if type(self.value) is not dict:
            
            try:
                json.dumps(self.value)
            except Exception:
                raise ValidationError("Value must be a valid JSON string.")
                
    def get_value(self):
        """
        Get the value, automatically casting it to the correct type.
        """
        

        if self.default:
            if not self.value:
                self.value = self.default

        if not self.value or self.value is None:
            if self.required:
                raise TethysAppSettingNotAssigned(
                    f'The required setting "{self.name}" for app "{self.tethys_app.package}":'
                    f"has not been assigned."
                )

            # None is a valid value to return in the case the value has not been set for this setting type
            return None
        
        return self.value


@receiver(models.signals.post_init, sender=CustomSimpleSetting)
@receiver(models.signals.post_init, sender=CustomJSONSetting)
def set_default_value(sender, instance, *args, **kwargs):
    """
    Set the default value for `value` on the `instance` of Setting.
    This signal receiver will process it as soon as the object is created for use

    Attributes:
        sender(CustomSetting): The `CustomSetting` class that sent the signal.
        instance(CustomSetting): The `CustomSetting` instance that is being initialised.

    Returns:
        None
    """
    # breakpoint()
    if not instance.value or instance.value == "":
        instance.value = instance.default

# @django.dispatch.receiver(models.signals.post_init, sender=CustomSetting)
@receiver(models.signals.post_init, sender=CustomSimpleSetting)
def set_default_custom_simple_setting_type(sender, instance, *args, **kwargs):
    """
    Set the default value for `value` on the `instance` of Setting.
    This signal receiver will process it as soon as the object is created for use

    Attributes:
        sender(CustomSetting): The `CustomSetting` class that sent the signal.
        instance(CustomSetting): The `CustomSetting` instance that is being initialised.

    Returns:
        None
    """
    if instance.type_custom_setting == "":
        instance.type_custom_setting = "SIMPLE"

@receiver(models.signals.post_init, sender=CustomSecretSetting)
def set_default_custom_secret_setting_type(sender, instance, *args, **kwargs):
    """
    Set the default value for `value` on the `instance` of Setting.
    This signal receiver will process it as soon as the object is created for use

    Attributes:
        sender(CustomSetting): The `CustomSetting` class that sent the signal.
        instance(CustomSetting): The `CustomSetting` instance that is being initialised.

    Returns:
        None
    """
    if instance.type_custom_setting == "":
        instance.type_custom_setting = "SECRET"


@receiver(models.signals.post_init, sender=CustomJSONSetting)
def set_default_custom_json_setting_type(sender, instance, *args, **kwargs):
    """
    Set the default value for `value` on the `instance` of Setting.
    This signal receiver will process it as soon as the object is created for use

    Attributes:
        sender(CustomSetting): The `CustomSetting` class that sent the signal.
        instance(CustomSetting): The `CustomSetting` instance that is being initialised.

    Returns:
        None
    """
    if instance.type_custom_setting == "":
        instance.type_custom_setting = "JSON"

class DatasetServiceSetting(TethysAppSetting):
    """
    Used to define a Dataset Service Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        engine(enum): Either DatasetServiceSetting.CKAN or DatasetServiceSetting.HYDROSHARE
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import DatasetServiceSetting

        primary_ckan_setting = DatasetServiceSetting(
            name='primary_ckan',
            description='Primary CKAN service for app to use.',
            engine=DatasetServiceSetting.CKAN,
            required=True,
        )

        hydroshare_setting = DatasetServiceSetting(
            name='hydroshare',
            description='HydroShare service for app to use.',
            engine=DatasetServiceSetting.HYDROSHARE,
            required=False
        )

    """

    CKAN = DatasetService.CKAN
    HYDROSHARE = DatasetService.HYDROSHARE

    dataset_service = models.ForeignKey(
        DatasetService, on_delete=models.CASCADE, blank=True, null=True
    )
    engine = models.CharField(
        max_length=200,
        choices=DatasetService.ENGINE_CHOICES,
        default=DatasetService.CKAN,
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.dataset_service and self.required:
            raise ValidationError("Required.")

    def get_value(self, as_public_endpoint=False, as_endpoint=False, as_engine=False):

        if not self.dataset_service:
            raise TethysAppSettingNotAssigned(
                f"Cannot create engine or endpoint for DatasetServiceSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no DatasetService assigned."
            )

        # Order here matters. Think carefully before changing.
        if as_engine:
            return self.dataset_service.get_engine()

        if as_endpoint:
            return self.dataset_service.endpoint

        if as_public_endpoint:
            return self.dataset_service.public_endpoint

        return self.dataset_service


class SpatialDatasetServiceSetting(TethysAppSetting):
    """
    Used to define a Spatial Dataset Service Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        engine(enum): One of SpatialDatasetServiceSetting.GEOSERVER or SpatialDatasetServiceSetting.THREDDS at this time.
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import SpatialDatasetServiceSetting

        primary_geoserver_setting = SpatialDatasetServiceSetting(
            name='primary_geoserver',
            description='spatial dataset service for app to use',
            engine=SpatialDatasetServiceSetting.GEOSERVER,
            required=True,
        )

    """  # noqa: E501

    GEOSERVER = SpatialDatasetService.GEOSERVER
    THREDDS = SpatialDatasetService.THREDDS

    spatial_dataset_service = models.ForeignKey(
        SpatialDatasetService, on_delete=models.CASCADE, blank=True, null=True
    )

    engine = models.CharField(
        max_length=200,
        choices=SpatialDatasetService.ENGINE_CHOICES,
        default=SpatialDatasetService.GEOSERVER,
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.spatial_dataset_service and self.required:
            raise ValidationError("Required.")

    def get_value(
        self,
        as_public_endpoint=False,
        as_endpoint=False,
        as_wms=False,
        as_wfs=False,
        as_engine=False,
        as_wcs=False,
    ):

        if not self.spatial_dataset_service:
            raise TethysAppSettingNotAssigned(
                f"Cannot create engine or endpoint for SpatialDatasetServiceSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no SpatialDatasetService assigned."
            )

        # Order here matters. Think carefully before changing.
        if as_engine:
            return self.spatial_dataset_service.get_engine()

        endpoint = self.spatial_dataset_service.endpoint

        if as_public_endpoint:
            endpoint = self.spatial_dataset_service.public_endpoint

        if self.engine == self.GEOSERVER:
            if as_wms:
                return endpoint.split("/rest")[0] + "/wms"

            if as_wfs:
                return endpoint.split("/rest")[0] + "/ows"

            if as_wcs:
                return endpoint.split("/rest")[0] + "/wcs"

        elif self.engine == self.THREDDS:
            if as_wms:
                return endpoint.rstrip("/") + "/wms"

            if as_wcs:
                return endpoint.rstrip("/") + "/wcs"

            if as_wfs:
                raise ValueError("THREDDS does not support the WFS interface.")

        if as_endpoint or as_public_endpoint:
            return endpoint

        return self.spatial_dataset_service


class WebProcessingServiceSetting(TethysAppSetting):
    """
    Used to define a Web Processing Service Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import WebProcessingServiceSetting

        primary_52n_setting = WebProcessingServiceSetting(
            name='primary_52n',
            description='WPS service for app to use',
            required=True,
        )

    """

    web_processing_service = models.ForeignKey(
        WebProcessingService, on_delete=models.CASCADE, blank=True, null=True
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.web_processing_service and self.required:
            raise ValidationError("Required.")

    def get_value(self, as_public_endpoint=False, as_endpoint=False, as_engine=False):
        wps_service = self.web_processing_service

        if not wps_service:
            raise TethysAppSettingNotAssigned(
                f"Cannot create engine or endpoint for WebProcessingServiceSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no WebProcessingService assigned."
            )

        # Order here matters. Think carefully before changing.
        if as_engine:
            return wps_service.get_engine()

        if as_endpoint:
            return wps_service.endpoint

        if as_public_endpoint:
            return wps_service.public_endpoint

        return wps_service


class PersistentStoreConnectionSetting(TethysAppSetting):
    """
    Used to define a Peristent Store Connection Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import PersistentStoreConnectionSetting

        primary_db_conn_setting = PersistentStoreConnectionSetting(
            name='primary',
            description='Connection with superuser role needed.',
            required=True
        )

    """

    persistent_store_service = models.ForeignKey(
        PersistentStoreService, on_delete=models.CASCADE, blank=True, null=True
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.persistent_store_service and self.required:
            raise ValidationError("Required.")

    def get_value(self, as_url=False, as_sessionmaker=False, as_engine=False):
        """
        Get the SQLAlchemy engine from the connected persistent store service
        """
        ps_service = self.persistent_store_service

        # Validate connection service
        if ps_service is None:
            raise TethysAppSettingNotAssigned(
                f"Cannot create engine or endpoint for PersistentStoreConnectionSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no PersistentStoreService assigned."
            )

        # Order here matters. Think carefully before changing.
        if as_engine:
            return ps_service.get_engine()

        if as_sessionmaker:
            return sessionmaker(bind=ps_service.get_engine())

        if as_url:
            return ps_service.get_url()

        return ps_service


class PersistentStoreDatabaseSetting(TethysAppSetting):
    """
    Used to define a Peristent Store Database Setting.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        initializer(str): Dot-notation path to function used to initialize the database.
        spatial(bool): Enable the PostGIS extension on the database during creation when True.
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import PersistentStoreDatabaseSetting

        spatial_db_setting = PersistentStoreDatabaseSetting(
            name='spatial_db',
            description='for storing important spatial stuff',
            required=True,
            initializer='appsettings.init_stores.init_spatial_db',
            spatial=True,
        ),

        temp_db_setting = PersistentStoreDatabaseSetting(
            name='temp_db',
            description='for storing temporary stuff',
            required=False,
            initializer='appsettings.init_stores.init_temp_db',
            spatial=False,
        )
    """

    spatial = models.BooleanField(default=False)
    dynamic = models.BooleanField(default=False)
    persistent_store_service = models.ForeignKey(
        PersistentStoreService, on_delete=models.CASCADE, blank=True, null=True
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.persistent_store_service and self.required:
            raise ValidationError("Required.")

    def initialize(self):
        """
        Initialize persistent store database setting.
        """
        self.create_persistent_store_database()

    def get_namespaced_persistent_store_name(self):
        """
        Return the namespaced persistent store database name (e.g. my_first_app_db).
        """
        # Convert name given by user to database safe name
        safe_name = self.name.lower().replace(" ", "_")

        # If testing environment, the engine for the "test" version of the persistent store should be fetched
        if is_testing_environment():
            safe_name = get_test_db_name(safe_name)

        return "_".join((self.tethys_app.package, safe_name))

    def get_value(
        self, with_db=False, as_url=False, as_sessionmaker=False, as_engine=False
    ):
        """
        Get the SQLAlchemy engine from the connected persistent store service
        """
        ps_service = self.persistent_store_service

        # Validate connection service
        if ps_service is None:
            raise TethysAppSettingNotAssigned(
                f"Cannot create engine or endpoint for PersistentStoreDatabaseSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no PersistentStoreService assigned."
            )

        if with_db:
            ps_service.database = self.get_namespaced_persistent_store_name()

        # Order here matters. Think carefully before changing.
        if as_engine:
            return ps_service.get_engine()

        if as_sessionmaker:
            return sessionmaker(bind=ps_service.get_engine())

        if as_url:
            return ps_service.get_url()

        return ps_service

    def persistent_store_database_exists(self):
        """
        Returns True if the persistent store database exists.
        """
        # Get the database engine
        engine = self.get_value(as_engine=True)
        namespaced_name = self.get_namespaced_persistent_store_name()

        # Cannot create databases in a transaction: connect and commit to close transaction
        connection = engine.connect()

        # Check for Database
        existing_query = """
                         SELECT d.datname as name
                         FROM pg_catalog.pg_database d
                         LEFT JOIN pg_catalog.pg_user u ON d.datdba = u.usesysid
                         WHERE d.datname = '{0}';
                         """.format(
            namespaced_name
        )

        existing_dbs = connection.execute(existing_query)
        connection.close()

        for existing_db in existing_dbs:
            if existing_db.name == namespaced_name:
                return True

        return False

    def drop_persistent_store_database(self):
        """
        Drop the persistent store database.
        """
        if not self.persistent_store_database_exists():
            return

        # Provide update for user
        log = logging.getLogger("tethys")
        log.info(
            'Dropping database "{0}" for app "{1}"...'.format(
                self.name, self.tethys_app.package
            )
        )

        # Get the database engine
        engine = self.get_value(as_engine=True)

        # Connection
        drop_connection = None

        namespaced_ps_name = self.get_namespaced_persistent_store_name()

        # Drop db
        drop_db_statement = 'DROP DATABASE IF EXISTS "{0}"'.format(namespaced_ps_name)

        try:
            drop_connection = engine.connect()
            drop_connection.execute("commit")
            drop_connection.execute(drop_db_statement)
        except Exception as e:
            if "being accessed by other users" in str(e):
                # Force disconnect all other connections to the database
                disconnect_sessions_statement = """
                                                SELECT pg_terminate_backend(pg_stat_activity.pid)
                                                FROM pg_stat_activity
                                                WHERE pg_stat_activity.datname = '{0}'
                                                AND pg_stat_activity.pid <> pg_backend_pid();
                                                """.format(
                    namespaced_ps_name
                )
                if drop_connection:
                    drop_connection.execute(disconnect_sessions_statement)

                    # Try again to drop the database
                    drop_connection.execute("commit")
                    drop_connection.execute(drop_db_statement)
            else:
                raise e
        finally:
            drop_connection and drop_connection.close()

    def create_persistent_store_database(self, refresh=False, force_first_time=False):
        """
        Provision all persistent stores for all apps or for only the app name given.
        """
        # Get looger
        log = logging.getLogger("tethys")

        # Connection engine
        url = self.get_value(as_url=True)
        engine = self.get_value(as_engine=True)
        namespaced_ps_name = self.get_namespaced_persistent_store_name()
        db_exists = self.persistent_store_database_exists()

        # -------------------------------------------------------------------------------------------------------------#
        # 1. Drop database if refresh option is included
        # -------------------------------------------------------------------------------------------------------------#
        if db_exists and refresh:
            self.drop_persistent_store_database()
            self.initialized = False
            self.save()
            db_exists = False

        # -------------------------------------------------------------------------------------------------------------#
        # 2. Create the database if it does not already exist
        # -------------------------------------------------------------------------------------------------------------#
        if not db_exists:
            # Provide Update for User
            log.info(
                'Creating database "{0}" for app "{1}"...'.format(
                    self.name, self.tethys_app.package
                )
            )

            # Cannot create databases in a transaction: connect and commit to close transaction
            create_connection = engine.connect()

            # Create db
            create_db_statement = """
                                  CREATE DATABASE "{0}"
                                  WITH OWNER {1}
                                  TEMPLATE template0
                                  ENCODING 'UTF8'
                                  """.format(
                namespaced_ps_name, url.username
            )

            # Close transaction first and then execute
            create_connection.execute("commit")
            try:
                create_connection.execute(create_db_statement)

            except sqlalchemy.exc.ProgrammingError:
                raise PersistentStorePermissionError(
                    'Database user "{0}" has insufficient permissions to create '
                    'the persistent store database "{1}": must have CREATE DATABASES '
                    "permission at a minimum.".format(url.username, self.name)
                )
            finally:
                create_connection.close()

        # -------------------------------------------------------------------------------------------------------------#
        # 3. Enable PostGIS extension
        # -------------------------------------------------------------------------------------------------------------#
        if self.spatial:
            # Connect to new database
            new_db_engine = self.get_value(with_db=True, as_engine=True)
            new_db_connection = new_db_engine.connect()

            # Notify user
            log.info(
                'Enabling PostGIS on database "{0}" for app "{1}"...'.format(
                    self.name,
                    self.tethys_app.package,
                )
            )

            enable_postgis_statement = "CREATE EXTENSION IF NOT EXISTS postgis"

            # Execute postgis statement
            try:
                new_db_connection.execute(enable_postgis_statement)
            except sqlalchemy.exc.ProgrammingError:
                raise PersistentStorePermissionError(
                    'Database user "{0}" has insufficient permissions to enable '
                    'spatial extension on persistent store database "{1}": must be a '
                    "superuser.".format(url.username, self.name)
                )
            finally:
                new_db_connection.close()

        # -------------------------------------------------------------------------------------------------------------#
        # 4. Run initialization function
        # -------------------------------------------------------------------------------------------------------------#
        if self.initializer:
            log.info(
                'Initializing database "{0}" for app "{1}" with initializer "{2}"...'.format(
                    self.name, self.tethys_app.package, self.initializer
                )
            )
            try:
                if force_first_time:
                    self.initializer_function(
                        self.get_value(with_db=True, as_engine=True), True
                    )
                else:
                    self.initializer_function(
                        self.get_value(with_db=True, as_engine=True),
                        not self.initialized,
                    )
            except Exception as e:
                raise PersistentStoreInitializerError(e)

        # Update initialization
        self.initialized = True
        self.save()


class SchedulerSetting(TethysAppSetting):
    """
    Used to define a Scheduler setting for Job processing services like HTCondor and Dask.

    Attributes:
        name(str): Unique name used to identify the setting.
        description(str): Short description of the setting.
        engine(enum): One of SchedulerSetting.HTCONDOR (default) or SchedulerSetting.DASK.
        required(bool): A value will be required if True.

    **Example:**

    ::

        from tethys_sdk.app_settings import SchedulerSetting

        primary_geoserver_setting = SchedulerSetting(
            name='primary_dask_scheduler',
            description='spatial dataset service for app to use',
            engine=SpatialDatasetServiceSetting.GEOSERVER,
            required=True,
        )

    """  # noqa: E501

    HTCONDOR = "htcondor"
    DASK = "dask"

    scheduler_service = models.ForeignKey(
        Scheduler, on_delete=models.CASCADE, blank=True, null=True
    )

    engine = models.CharField(
        max_length=200,
        choices=((HTCONDOR, "HTCondor"), (DASK, "Dask")),
        default=HTCONDOR,
    )

    def clean(self):
        """
        Validate prior to saving changes.
        """
        if not self.scheduler_service and self.required:
            raise ValidationError("Required.")

        # Validate type
        if self.scheduler_service:
            scheduler = self.get_value()
            if self.engine == self.HTCONDOR and not isinstance(
                scheduler, CondorScheduler
            ):
                raise ValidationError("Please select a Condor Scheduler.")
            elif self.engine == self.DASK and not isinstance(scheduler, DaskScheduler):
                raise ValidationError("Please select a Dask Scheduler.")

    def get_value(self):
        if not self.scheduler_service:
            raise TethysAppSettingNotAssigned(
                f"Cannot find Scheduler for SchedulerSetting "
                f'"{self.name}" for app "{self.tethys_app.package}": '
                f"no Scheduler assigned."
            )

        # Query scheduler manually to get as subclass (ForeignKey fields don't support select_subclasses)
        scheduler = Scheduler.objects.select_subclasses().get(
            pk=self.scheduler_service.pk
        )
        return scheduler


class ProxyApp(models.Model):
    """
    DB model for Proxy Apps which allows you to redirect an app to another host.
    """

    name = models.CharField(max_length=100, unique=True)
    endpoint = models.URLField(max_length=512)
    logo_url = models.URLField(max_length=512, blank=True)
    back_url = models.URLField(max_length=512, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    tags = models.CharField(max_length=200, blank=True, default="")
    enabled = models.BooleanField(default=True)
    show_in_apps_library = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Proxy App"
        verbose_name_plural = "Proxy Apps"

    @property
    def proxied(self):
        return True

    @property
    def url(self):
        return self.endpoint

    @property
    def icon(self):
        return self.logo_url

    def __str__(self):
        return self.name




    