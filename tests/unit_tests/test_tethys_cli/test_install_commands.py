from os import devnull, chdir
from pathlib import Path
from django.db import transaction
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from unittest import mock
from conda.cli.python_api import Commands
from tethys_cli import install_commands


FNULL = open(devnull, "w")


class TestServiceInstallHelpers(TestCase):
    def setUp(self):
        from tethys_apps.models import TethysApp

        self.app = TethysApp.objects.create(
            name="An App",
            package="an_app",
        )
        self.app.save()

    @mock.patch("tethys_cli.install_commands.exit")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_open_file_error(self, mock_pretty_output, mock_exit):
        mock_exit.side_effect = SystemExit

        mock_file_path = mock.MagicMock()
        mock_file_path.open.side_effect = IOError("test")

        self.assertRaises(SystemExit, install_commands.open_file, mock_file_path)
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual("test", po_call_args[0][0][0])
        self.assertIn(
            "An unexpected error occurred reading the file.",
            po_call_args[1][0][0],
        )

        mock_exit.assert_called_with(1)

    @mock.patch("tethys_cli.install_commands.input")
    def test_get_interactive_input(self, mock_input):
        install_commands.get_interactive_input()
        mock_input.assert_called_with("")

    @mock.patch("tethys_cli.install_commands.input")
    def test_get_service_name_input(self, mock_input):
        install_commands.get_service_name_input()
        mock_input.assert_called_with("")

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_print_unconfigured_settings(self, mock_pretty_output):
        class MockSetting:
            def __init__(self, name, required):
                self.name = name
                self.required = required

        app_name = "foo"
        mock_setting = [MockSetting("test_name", True)]
        install_commands.print_unconfigured_settings(app_name, mock_setting)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            f"\nThe following settings were not configured for app: {app_name}:\n",
            po_call_args[0][0][0],
        )
        self.assertIn("test_name", po_call_args[2][0][0])

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("tethys_cli.install_commands.call")
    def test_run_sync_stores(self, mock_call, mock_pretty_output):
        from tethys_apps.models import PersistentStoreConnectionSetting

        app_name = "foo"

        install_commands.run_sync_stores(app_name, [PersistentStoreConnectionSetting()])
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            f"Running syncstores for app {app_name}", po_call_args[0][0][0]
        )
        mock_call.assert_called_with(
            ["tethys", "syncstores", app_name],
        )

    @mock.patch("tethys_cli.install_commands.validate_service_id", return_value=True)
    @mock.patch(
        "tethys_cli.install_commands.get_setting_type_from_setting",
        return_value="setting_type",
    )
    @mock.patch("tethys_cli.install_commands.link_service_to_app_setting")
    def test_find_and_link(
        self, mock_link_service_to_app_setting, mock_gstfs, mock_vsi
    ):
        service_type = "service_type"
        setting_name = "setting_name"
        service_id = "service_name"
        app_name = "app_name"
        mock_setting = mock.MagicMock()

        install_commands.find_and_link(
            service_type, setting_name, service_id, app_name, mock_setting
        )

        mock_vsi.assert_called_with(service_type, service_id)
        mock_gstfs.assert_called_with(mock_setting)
        mock_link_service_to_app_setting.assert_called_with(
            service_type, service_id, app_name, "setting_type", setting_name
        )

    @mock.patch("tethys_cli.install_commands.validate_service_id", return_value=False)
    @mock.patch(
        "tethys_cli.install_commands.get_setting_type_from_setting",
        return_value="setting_type",
    )
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_find_and_link_warning(self, mock_pretty_output, _, __):
        service_type = "service_type"
        setting_name = "setting_name"
        service_id = "service_name"
        app_name = "app_name"
        mock_setting = mock.MagicMock()

        install_commands.find_and_link(
            service_type, setting_name, service_id, app_name, mock_setting
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            f'Warning: Could not find service of type: "{service_type}" with the Name/ID: "{service_id}"',
            po_call_args[0][0][0],
        )

    def test_get_setting_type(self):
        from tethys_apps.models import PersistentStoreDatabaseSetting

        self.assertEqual(
            "persistent",
            install_commands.get_setting_type(PersistentStoreDatabaseSetting()),
        )

    def test_validate_service_id_valid_id_int(self):
        from tethys_services.models import SpatialDatasetService

        test_service = SpatialDatasetService.objects.create(
            name="foo",
            engine=SpatialDatasetService.GEOSERVER,
            endpoint="https://example.com:8181/geoserver/rest/",
            username="admin",
            password="geoserver",
        )
        test_service.save()
        int_id = int(test_service.id)
        ret = install_commands.validate_service_id("spatial", int_id)
        self.assertTrue(ret)

    def test_validate_service_id_valid_id_str(self):
        from tethys_services.models import PersistentStoreService

        test_service = PersistentStoreService.objects.create(
            name="foo",
            engine="postgresql",
            host="example.com",
            port="5432",
            username="fake_user",
            password="password",
        )
        test_service.save()
        string_id = str(test_service.id)
        ret = install_commands.validate_service_id("persistent", string_id)
        self.assertTrue(ret)

    def test_validate_service_id_valid_name(self):
        from tethys_services.models import DatasetService

        service_name = "fake_service"
        test_service = DatasetService.objects.create(
            name=service_name,
            engine=DatasetService.CKAN,
            endpoint="https://example.com/api/3/action/",
            apikey="F8k@p1K3Y",
        )
        test_service.save()
        ret = install_commands.validate_service_id("dataset", service_name)
        self.assertTrue(ret)

    def test_validate_service_id_invalid(self):
        from tethys_services.models import WebProcessingService

        service_name = "fake_service"
        test_service = WebProcessingService.objects.create(
            name=service_name,
            endpoint="https://example.com/wps/WebProcessingService/",
            username="fake_user",
            password="password",
        )
        test_service.save()
        ret = install_commands.validate_service_id("wps", "does_not_exist")
        self.assertFalse(ret)

    def test_get_setting_type_from_setting_persistent_db(self):
        from tethys_apps.models import PersistentStoreDatabaseSetting

        with transaction.atomic():
            setting = PersistentStoreDatabaseSetting.objects.create(
                name="fake_db",
                description="The fake database.",
                initializer="fake.path.to.initializer",
                spatial=False,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_setting_type_from_setting(setting)

        self.assertEqual("ps_database", ret)

    def test_get_setting_type_from_setting_persistent_connection(self):
        from tethys_apps.models import PersistentStoreConnectionSetting

        with transaction.atomic():
            setting = PersistentStoreConnectionSetting.objects.create(
                name="fake_conn",
                description="The fake database connection.",
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_setting_type_from_setting(setting)

        self.assertEqual("ps_connection", ret)

    def test_get_setting_type_from_setting_spatial_dataset(self):
        from tethys_apps.models import SpatialDatasetServiceSetting

        with transaction.atomic():
            setting = SpatialDatasetServiceSetting.objects.create(
                name="fake_sds",
                description="The fake GeoServer dataset service.",
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_setting_type_from_setting(setting)

        self.assertEqual("ds_spatial", ret)

    def test_get_setting_type_from_setting_dataset(self):
        from tethys_apps.models import DatasetServiceSetting

        with transaction.atomic():
            setting = DatasetServiceSetting.objects.create(
                name="fake_ds",
                description="The fake CKAN dataset service.",
                engine=DatasetServiceSetting.CKAN,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_setting_type_from_setting(setting)

        self.assertEqual("ds_dataset", ret)

    def test_get_setting_type_from_setting_wps(self):
        from tethys_apps.models import WebProcessingServiceSetting

        with transaction.atomic():
            setting = WebProcessingServiceSetting.objects.create(
                name="fake_sds",
                description="The fake spatial dataset service.",
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_setting_type_from_setting(setting)

            self.assertEqual("wps", ret)

    def test_get_setting_type_from_setting_invalid_setting(self):
        not_a_setting = mock.MagicMock()
        with self.assertRaises(RuntimeError) as cm:
            install_commands.get_setting_type_from_setting(not_a_setting)

            self.assertIn(
                "Could not determine setting type for setting:",
                str(cm.exception),
            )

    def test_get_service_type_from_setting_persistent_db(self):
        from tethys_apps.models import PersistentStoreDatabaseSetting

        with transaction.atomic():
            setting = PersistentStoreDatabaseSetting.objects.create(
                name="fake_db",
                description="The fake database.",
                initializer="fake.path.to.initializer",
                spatial=False,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_service_type_from_setting(setting)

        self.assertEqual("persistent", ret)

    def test_get_service_type_from_setting_persistent_connection(self):
        from tethys_apps.models import PersistentStoreConnectionSetting

        with transaction.atomic():
            setting = PersistentStoreConnectionSetting.objects.create(
                name="fake_conn",
                description="The fake database connection.",
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_service_type_from_setting(setting)

        self.assertEqual("persistent", ret)

    def test_get_service_type_from_setting_spatial_dataset(self):
        from tethys_apps.models import SpatialDatasetServiceSetting

        with transaction.atomic():
            setting = SpatialDatasetServiceSetting.objects.create(
                name="fake_sds",
                description="The fake GeoServer dataset service.",
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_service_type_from_setting(setting)

        self.assertEqual("spatial", ret)

    def test_get_service_type_from_setting_dataset(self):
        from tethys_apps.models import DatasetServiceSetting

        with transaction.atomic():
            setting = DatasetServiceSetting.objects.create(
                name="fake_ds",
                description="The fake CKAN dataset service.",
                engine=DatasetServiceSetting.CKAN,
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_service_type_from_setting(setting)

        self.assertEqual("dataset", ret)

    def test_get_service_type_from_setting_wps(self):
        from tethys_apps.models import WebProcessingServiceSetting

        with transaction.atomic():
            setting = WebProcessingServiceSetting.objects.create(
                name="fake_sds",
                description="The fake spatial dataset service.",
                required=False,
                tethys_app=self.app,
            )

            ret = install_commands.get_service_type_from_setting(setting)

            self.assertEqual("wps", ret)

    def test_get_service_type_from_setting_invalid_setting(self):
        not_a_setting = mock.MagicMock()
        with self.assertRaises(RuntimeError) as cm:
            install_commands.get_service_type_from_setting(not_a_setting)

            self.assertIn(
                "Could not determine service type for setting:",
                str(cm.exception),
            )


class TestInstallServicesCommands(TestCase):
    def setUp(self):
        self.mock_path = mock.MagicMock()
        path_patcher = mock.patch(
            "tethys_cli.install_commands.Path", return_value=self.mock_path
        )
        path_patcher.start()
        self.addCleanup(path_patcher.stop)

    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.find_and_link")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("tethys_cli.install_commands.json.loads")
    @mock.patch("tethys_cli.install_commands.Path")
    @mock.patch("tethys_apps.models.CustomSettingBase")
    @mock.patch("tethys_apps.models.TethysApp")
    def test_configure_services_from_file(
        self,
        mock_TethysApp,
        mock_CustomSetting,
        mock_path,
        mock_json_loads,
        mock_pretty_output,
        mock_find_and_link,
        mock_gas,
    ):
        app_name = "foo"
        invalid_custom_setting_name = "custom_setting_name"
        invalid_custom_setting_value = "hello world"
        valid_custom_setting_name = "valid_setting"
        valid_custom_setting_value = False

        json_custom_setting_name = "json_setting"
        json_custom_setting_value = "fake/path/to/file"
        json_custom_setting_wrong_path_name = "wrong_path_json_setting"
        json_custom_setting_wrong_path_value = '{"name": "John", "age": 30, "city": "New York", "interests": ["music", "sports", "reading"], "education": {"degree": "Bachelor", "major": "Computer Science", "university": "ABC University"}, "work_experience": [{"position": "Software Engineer", "company": "XYZ Inc.", "duration": "3 years"}, {"position": "Senior Developer", "company": "ABC Corp.", "duration": "2 years"}], "projects": [{"name": "Project A", "description": "Lorem ipsum dolor sit amet", "status": "completed"}, {"name": "Project B", "description": "Consectetur adipiscing elit", "status": "in progress"}], "family_members": [{"name": "Jane", "relationship": "Spouse", "age": 28}, {"name": "Sarah", "relationship": "Sister", "age": 32}, {"name": "Michael", "relationship": "Brother", "age": 26}], "address": {"street": "123 Main Street", "city": "New York", "state": "NY", "postal_code": "10001"}, "phone_numbers": {"home": "555-1234", "work": "555-5678", "cell": "555-9876"}}'
        json_custom_setting_value_error_name = "value_error_json_setting"
        json_custom_setting_value_error_value = '{"name": "John", "age": 30,}'
        json_custom_setting_value_json_name = "json_custom_setting_which_is_json"
        json_custom_setting_value_json_value = {
            "name": "John",
            "age": 30,
            "city": "New York",
            "interests": ["music", "sports", "reading"],
            "education": {
                "degree": "Bachelor",
                "major": "Computer Science",
                "university": "ABC University",
            },
            "work_experience": [
                {
                    "position": "Software Engineer",
                    "company": "XYZ Inc.",
                    "duration": "3 years",
                },
                {
                    "position": "Senior Developer",
                    "company": "ABC Corp.",
                    "duration": "2 years",
                },
            ],
            "projects": [
                {
                    "name": "Project A",
                    "description": "Lorem ipsum dolor sit amet",
                    "status": "completed",
                },
                {
                    "name": "Project B",
                    "description": "Consectetur adipiscing elit",
                    "status": "in progress",
                },
            ],
            "family_members": [
                {"name": "Jane", "relationship": "Spouse", "age": 28},
                {"name": "Sarah", "relationship": "Sister", "age": 32},
                {"name": "Michael", "relationship": "Brother", "age": 26},
            ],
            "address": {
                "street": "123 Main Street",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
            },
            "phone_numbers": {
                "home": "555-1234",
                "work": "555-5678",
                "cell": "555-9876",
            },
        }
        json_custom_setting_not_dict_or_file_path_name = (
            "json_custom_setting_which_is_not_a_dict_or_file_path"
        )
        json_custom_setting_not_dict_or_file_path_value = 2
        secret_custom_setting_name = "secret_setting"
        secret_custom_setting_value = "SECRET:XXXX235235RSDGSDGAF_23523"

        persistent_setting_name = "persistent_setting_name"
        persistent_service_name = "persistent_service_name"
        no_val_persistent_setting_name = "no_val"
        setting_already_linked_name = "already_linked"

        services_file_contents = {
            "version": 1,
            "custom_settings": {
                invalid_custom_setting_name: invalid_custom_setting_value,
                valid_custom_setting_name: valid_custom_setting_value,
                "custom_setting_dne": 1,
                json_custom_setting_name: json_custom_setting_value,
                json_custom_setting_wrong_path_name: json_custom_setting_wrong_path_value,
                json_custom_setting_value_error_name: json_custom_setting_value_error_value,
                json_custom_setting_value_json_name: json_custom_setting_value_json_value,
                json_custom_setting_not_dict_or_file_path_name: json_custom_setting_not_dict_or_file_path_value,
                secret_custom_setting_name: secret_custom_setting_value,
            },
            "persistent": {
                persistent_setting_name: persistent_service_name,
                no_val_persistent_setting_name: None,
                setting_already_linked_name: persistent_service_name,
            },
        }

        # Saving raises a validation error
        mock_invalid_custom_setting = mock.MagicMock(
            value=None, type_custom_setting="SIMPLE"
        )
        mock_invalid_custom_setting.save.side_effect = ValidationError("error")

        # Saving will pass on the valid custom setting (not mocked to raise ValidationError)
        mock_valid_custom_setting = mock.MagicMock(
            value=None, type_custom_setting="SIMPLE"
        )

        # Json setting with correct path
        mock_json_custom_setting = mock.MagicMock(
            value=None, type_custom_setting="JSON"
        )

        # Json setting with incorrect path, but valid json
        mock_json_custom_setting_wrong_path = mock.MagicMock(
            value=None, type_custom_setting="JSON"
        )

        # Json setting with value error
        mock_json_custom_setting_value_error = mock.MagicMock(
            value=None, type_custom_setting="JSON"
        )

        # Json setting with valid dict
        mock_json_custom_setting_value_dict = mock.MagicMock(
            value=None, type_custom_setting="JSON"
        )

        # # json setting invalid value, in this case a number
        mock_json_custom_setting_invalid_value = mock.MagicMock(
            value=None, type_custom_setting="JSON"
        )
        # valid custom Secret setting
        mock_secret_custom_setting = mock.MagicMock(
            value=None, type_custom_setting="SECRET"
        )

        mock_CustomSetting.objects.filter.return_value.select_subclasses.return_value.get.side_effect = [
            mock_invalid_custom_setting,  #: Save raises Validation error
            mock_valid_custom_setting,  #: Should pass without errors
            ObjectDoesNotExist,  #: Setting not found
            mock_json_custom_setting,
            mock_json_custom_setting_wrong_path,
            mock_json_custom_setting_value_error,
            mock_json_custom_setting_value_dict,
            mock_json_custom_setting_invalid_value,
            mock_secret_custom_setting,
        ]
        mock_path().is_file.side_effect = [True, False, False]
        mock_path().read_text.return_value = '{"fake_json": "{}"}'

        mock_json_loads.side_effect = [
            ['{"fake_json": "{}"}'],
            json_custom_setting_wrong_path_value,
            ValueError,
        ]

        # This persistent setting exists and is listed in the file
        mock_persistent_database_setting = mock.MagicMock()
        mock_persistent_database_setting.name = persistent_setting_name

        # This setting exists, but there is no value assigned in the file
        mock_no_val_persistent_setting = mock.MagicMock()
        mock_no_val_persistent_setting.name = no_val_persistent_setting_name

        # This persistent setting is not listed in the file, but exists in the db
        mock_setting_unlisted = mock.MagicMock()
        mock_setting_unlisted.name = "this_setting_is_in_the_file_but_does_not_exist"

        mock_setting_already_linked = mock.MagicMock()
        mock_setting_already_linked.name = setting_already_linked_name

        mock_gas.return_value = {
            "unlinked_settings": [
                mock_setting_unlisted,  #: This persistent setting is not listed in the file, but exists in the db
                mock_persistent_database_setting,  #: This persistent setting exists and is listed with value
                mock_no_val_persistent_setting,  #: This setting exists and is listed in the file, but no value given
            ],
            "linked_settings": [
                mock_setting_already_linked,  #: This setting is already linked, and so it won't be configured again
            ],
        }
        install_commands.configure_services_from_file(services_file_contents, app_name)
        po_call_args = mock_pretty_output().__enter__().write.call_args_list

        self.assertIn(
            f"Incorrect value type given for custom setting '{invalid_custom_setting_name}'",
            po_call_args[0][0][0],
        )
        self.assertEqual(
            f'CustomSetting: "{valid_custom_setting_name}" was assigned the value: '
            f'"{valid_custom_setting_value}"',
            po_call_args[1][0][0],
        )
        self.assertEqual(
            'Custom setting named "custom_setting_dne" could not be found in app "foo". Skipping...',
            po_call_args[2][0][0],
        )

        self.assertEqual(
            'CustomSetting: "json_setting" was assigned the value: "fake/path/to/file"',
            po_call_args[3][0][0],
        )

        self.assertEqual(
            'CustomSetting: "wrong_path_json_setting" was assigned the value: "{"name": "John", "age": 30, "city": "New York", "interests": ["music", "sports", "reading"], "education": {"degree": "Bachelor", "major": "Computer Science", "university": "ABC University"}, "work_experience": [{"position": "Software Engineer", "company": "XYZ Inc.", "duration": "3 years"}, {"position": "Senior Developer", "company": "ABC Corp.", "duration": "2 years"}], "projects": [{"name": "Project A", "description": "Lorem ipsum dolor sit amet", "status": "completed"}, {"name": "Project B", "description": "Consectetur adipiscing elit", "status": "in progress"}], "family_members": [{"name": "Jane", "relationship": "Spouse", "age": 28}, {"name": "Sarah", "relationship": "Sister", "age": 32}, {"name": "Michael", "relationship": "Brother", "age": 26}], "address": {"street": "123 Main Street", "city": "New York", "state": "NY", "postal_code": "10001"}, "phone_numbers": {"home": "555-1234", "work": "555-5678", "cell": "555-9876"}}"',
            po_call_args[4][0][0],
        )
        self.assertEqual(
            'The current file path/JSON string: {"name": "John", "age": 30,} is not a file path or does not contain a valid JSONstring.',
            po_call_args[5][0][0],
        )
        self.assertEqual(
            'Custom setting named "value_error_json_setting" is not valid in app "foo". Skipping...',
            po_call_args[6][0][0],
        )
        self.assertEqual(
            "CustomSetting: \"json_custom_setting_which_is_json\" was assigned the value: \"{'name': 'John', 'age': 30, 'city': 'New York', 'interests': ['music', 'sports', 'reading'], 'education': {'degree': 'Bachelor', 'major': 'Computer Science', 'university': 'ABC University'}, 'work_experience': [{'position': 'Software Engineer', 'company': 'XYZ Inc.', 'duration': '3 years'}, {'position': 'Senior Developer', 'company': 'ABC Corp.', 'duration': '2 years'}], 'projects': [{'name': 'Project A', 'description': 'Lorem ipsum dolor sit amet', 'status': 'completed'}, {'name': 'Project B', 'description': 'Consectetur adipiscing elit', 'status': 'in progress'}], 'family_members': [{'name': 'Jane', 'relationship': 'Spouse', 'age': 28}, {'name': 'Sarah', 'relationship': 'Sister', 'age': 32}, {'name': 'Michael', 'relationship': 'Brother', 'age': 26}], 'address': {'street': '123 Main Street', 'city': 'New York', 'state': 'NY', 'postal_code': '10001'}, 'phone_numbers': {'home': '555-1234', 'work': '555-5678', 'cell': '555-9876'}}\"",
            po_call_args[7][0][0],
        )
        self.assertEqual(
            "The current value: 2 is not a dict or a valid file path",
            po_call_args[8][0][0],
        )
        self.assertEqual(
            'Custom setting named "json_custom_setting_which_is_not_a_dict_or_file_path" is not valid in app "foo". Skipping...',
            po_call_args[9][0][0],
        )
        self.assertEqual(
            'CustomSetting: "secret_setting" was assigned the value: "SECRET:XXXX235235RSDGSDGAF_23523"',
            po_call_args[10][0][0],
        )

        self.assertEqual(
            f'No service given for setting "{no_val_persistent_setting_name}". Skipping...',
            po_call_args[11][0][0],
        )
        self.assertIn(
            "already configured or does not exist in app",
            po_call_args[12][0][0],
        )

        mock_find_and_link.assert_called_with(
            "persistent",
            persistent_setting_name,
            persistent_service_name,
            app_name,
            mock_persistent_database_setting,
        )
        mock_TethysApp.objects.get.assert_called_once()

    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.find_and_link")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("tethys_apps.models.TethysApp")
    def test_configure_services_from_file_no_settings_for_app(
        self, mock_TethysApp, mock_pretty_output, mock_find_and_link, mock_gas
    ):
        app_name = "foo"
        persistent_setting_name = "persistent_setting_name"
        persistent_service_name = "persistent_service_name"

        services_file_contents = {
            "version": 1,
            "persistent": {persistent_setting_name: persistent_service_name},
        }

        # No settings found for this app
        mock_gas.return_value = None

        install_commands.configure_services_from_file(services_file_contents, app_name)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            f'No settings found for app "{app_name}". Skipping automated configuration...',
            po_call_args[0][0][0],
        )
        mock_find_and_link.assert_not_called()
        mock_TethysApp.objects.get.assert_called_once()

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_run_portal_install_path_none(self, _):
        self.mock_path.__truediv__().exists.return_value = False

        self.assertFalse(install_commands.run_portal_install("foo"))

    @mock.patch("tethys_cli.install_commands.configure_services_from_file")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("tethys_cli.install_commands.open_file")
    def test_run_portal_install(
        self, mock_open_file, mock_pretty_output, mock_configure_services
    ):
        app_name = "foo"
        services = {"persistent": {"test_setting": "test_service"}}
        portal_options_services = {"apps": {app_name: {"services": services}}}
        portal_options_empty_services = {"apps": {app_name: {"services": ""}}}
        portal_options_no_services = {"apps": {app_name: ""}}

        mock_open_file.side_effect = [
            portal_options_services,
            portal_options_empty_services,
            portal_options_no_services,
        ]
        self.mock_path.exists.return_value = True

        self.assertTrue(install_commands.run_portal_install(app_name))
        mock_configure_services.assert_called_with(services, app_name)
        self.assertFalse(install_commands.run_portal_install(app_name))
        self.assertFalse(install_commands.run_portal_install(app_name))

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn(
            f"No app configuration found for app: {app_name}",
            po_call_args[2][0][0],
        )
        self.assertIn(
            "No apps configuration found in portal config file.",
            po_call_args[4][0][0],
        )

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_run_services_path_none(self, mock_pretty_output):
        args = mock.MagicMock(
            services_file=None,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )

        self.mock_path.exists.return_value = False

        install_commands.run_services("foo", args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual("No Services file found.", po_call_args[0][0][0])

    @mock.patch("tethys_cli.install_commands.configure_services_from_file")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("tethys_cli.install_commands.open_file")
    def test_run_services(self, mock_open_file, mock_pretty_output, _):
        args = mock.MagicMock(
            services_file="services_file",
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )

        self.mock_path.exists.return_value = True
        mock_open_file.side_effect = ["service_file", ""]
        install_commands.run_services("foo", args)
        install_commands.run_services("foo", args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual("No Services listed in Services file.", po_call_args[0][0][0])


class TestInstallCommands(TestCase):
    def setUp(self):
        from tethys_apps.models import TethysApp

        self.src_dir = Path(__file__).parents[2]
        self.root_app_path = self.src_dir / "apps" / "tethysapp-test_app"
        self.app_model = TethysApp(name="test_app", package="test_app")
        self.app_model.save()
        self.cwd = str(Path.cwd())
        chdir(self.root_app_path)

    def tearDown(self):
        self.app_model.delete()
        chdir(self.cwd)

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("builtins.input", side_effect=["x", "n"])
    @mock.patch("tethys_cli.install_commands.call")
    def test_install_file_not_generate(self, mock_call, _, mock_pretty_output):
        chdir("..")  # move to a different directory that doesn't have an install.yml
        args = mock.MagicMock(
            file=None,
            quiet=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )

        install_commands.install_command(args)
        self.assertEqual(2, len(mock_call.call_args_list))
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual("WARNING: No install file found.", po_call_args[0][0][0])
        self.assertEqual("Generation of Install File cancelled.", po_call_args[1][0][0])
        self.assertEqual(
            "Continuing install without configuration.", po_call_args[2][0][0]
        )
        self.assertEqual("Running application install....", po_call_args[3][0][0])
        self.assertEqual("Successfully installed None.", po_call_args[4][0][0])

    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch("builtins.input", side_effect=["y"])
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.exit")
    def test_install_file_generate(self, mock_exit, mock_call, _, __):
        chdir("..")  # move to a different directory that doesn't have an install.yml
        args = mock.MagicMock(
            file=None,
            quiet=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        check_call = ["tethys", "gen", "install"]

        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, install_commands.install_command, args)
        mock_call.assert_called_with(check_call)
        mock_exit.assert_called_with(0)

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_no_conda_input_file(self, mock_pretty_output, _, __):
        file_path = self.root_app_path / "install-no-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            verbose=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )

        install_commands.install_command(args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 6)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertIn("Running application install....", po_call_args[1][0][0])
        self.assertIn(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[2][0][0],
        )
        self.assertIn("Services Configuration Completed.", po_call_args[3][0][0])
        self.assertIn("Skipping syncstores.", po_call_args[4][0][0])
        self.assertIn("Successfully installed test_app.", po_call_args[5][0][0])

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_input_file_with_post(self, mock_pretty_output, _, __):
        file_path = self.root_app_path / "install-with-post.yml"
        args = mock.MagicMock(
            file=file_path,
            verbose=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )

        install_commands.install_command(args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 9)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual(
            "Skipping package installation, Skip option found.",
            po_call_args[1][0][0],
        )
        self.assertIn("Running application install....", po_call_args[2][0][0])
        self.assertIn(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[3][0][0],
        )
        self.assertIn("Services Configuration Completed.", po_call_args[4][0][0])
        self.assertIn("Skipping syncstores.", po_call_args[5][0][0])
        self.assertIn("Running post installation tasks...", po_call_args[6][0][0])
        self.assertIn("Post Script Result: b'test", po_call_args[7][0][0])
        self.assertIn("Successfully installed test_app.", po_call_args[8][0][0])

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.run_sync_stores")
    @mock.patch("tethys_cli.install_commands.run_interactive_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.run_portal_install", return_value=False)
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_skip_input_file(self, mock_pretty_output, _, __, ___, ____, _____, ______):
        file_path = self.root_app_path / "install-skip-setup.yml"

        args = mock.MagicMock(
            file=file_path,
            verbose=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        args = mock.MagicMock(
            file=file_path,
            develop=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        args = mock.MagicMock(
            file=file_path,
            verbose=False,
            develop=False,
            force_services=False,
            quiet=False,
            no_sync_stores=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            "Skipping package installation, Skip option found.",
            po_call_args[1][0][0],
        )

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.conda_run", return_value=["", "", 1])
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_and_pip_package_install(
        self, mock_pretty_output, mock_conda_run, mock_call, _
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        mock_conda_run.assert_called_with(
            Commands.INSTALL,
            "-c",
            "tacaswell",
            "--freeze-installed",
            "geojson",
            use_exception_handler=False,
            stdout=None,
            stderr=None,
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 9)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual("Running conda installation tasks...", po_call_args[1][0][0])
        self.assertIn(
            "Warning: Packages installation ran into an error.",
            po_call_args[2][0][0],
        )
        self.assertEqual("Running pip installation tasks...", po_call_args[3][0][0])
        self.assertEqual("Running application install....", po_call_args[4][0][0])
        self.assertEqual(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[5][0][0],
        )
        self.assertEqual("Services Configuration Completed.", po_call_args[6][0][0])
        self.assertEqual("Skipping syncstores.", po_call_args[7][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[8][0][0])

        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[0][1][0])
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[1][1][0])
        self.assertEqual(["tethys", "db", "sync"], mock_call.mock_calls[2][1][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "y"])
    @mock.patch("tethys_cli.install_commands.write_warning")
    @mock.patch("tethys_cli.install_commands.has_module")
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_install_no_conda_proceed(
        self, mock_pretty_output, mock_call, _, mock_has_module, mock_warn, __
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            quiet=False,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        mock_has_module.return_value = False

        install_commands.install_command(args)

        mock_warn.assert_called_once()
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 8)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual("Running pip installation tasks...", po_call_args[1][0][0])
        self.assertEqual("Running application install....", po_call_args[2][0][0])
        self.assertIn("Running Interactive Service Mode.", po_call_args[3][0][0])
        self.assertEqual(
            "Hit return at any time to skip a step.", po_call_args[4][0][0]
        )
        self.assertEqual("Services Configuration Completed.", po_call_args[5][0][0])
        self.assertEqual("Skipping syncstores.", po_call_args[6][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[7][0][0])

        self.assertEqual(["pip", "install", "geojson"], mock_call.mock_calls[0][1][0])
        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[1][1][0])
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[2][1][0])
        self.assertEqual(["tethys", "db", "sync"], mock_call.mock_calls[3][1][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "y"])
    @mock.patch("tethys_cli.install_commands.write_warning")
    @mock.patch("tethys_cli.install_commands.has_module")
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_install_no_conda_proceed_quietly(
        self, mock_pretty_output, mock_call, _, mock_has_module, mock_warn, __
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        mock_has_module.return_value = False

        install_commands.install_command(args)

        mock_warn.assert_called_once()
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 7)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual("Running pip installation tasks...", po_call_args[1][0][0])
        self.assertEqual("Running application install....", po_call_args[2][0][0])
        self.assertEqual(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[3][0][0],
        )
        self.assertEqual("Services Configuration Completed.", po_call_args[4][0][0])
        self.assertEqual("Skipping syncstores.", po_call_args[5][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[6][0][0])

        self.assertEqual(["pip", "install", "geojson"], mock_call.mock_calls[0][1][0])
        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[1][1][0])
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[2][1][0])
        self.assertEqual(["tethys", "db", "sync"], mock_call.mock_calls[3][1][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "n"])
    @mock.patch("tethys_cli.install_commands.write_warning")
    @mock.patch("tethys_cli.install_commands.has_module")
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.exit")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_install_no_conda_cancel(
        self, mock_pretty_output, mock_exit, _, mock_has_module, mock_warn, __
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            quiet=False,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        mock_has_module.return_value = False
        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, install_commands.install_command, args)

        mock_warn.assert_called_once()
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 2)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual("\nInstall Command cancelled.", po_call_args[1][0][0])

        mock_exit.assert_called_with(0)

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "y"])
    @mock.patch("tethys_cli.install_commands.write_warning")
    @mock.patch("tethys_cli.install_commands.has_module")
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_install_no_conda_error(
        self, mock_pretty_output, mock_call, _, mock_has_module, mock_warn, __
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=False,
        )
        mock_has_module.return_value = False
        mock_call.side_effect = [Exception, None, None, None]
        install_commands.install_command(args)

        mock_warn.assert_called_once()
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 8)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual(
            "Installing conda packages with pip failed with the following exception: ",
            po_call_args[1][0][0],
        )
        self.assertEqual("Running pip installation tasks...", po_call_args[2][0][0])
        self.assertEqual("Running application install....", po_call_args[3][0][0])
        self.assertEqual(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[4][0][0],
        )
        self.assertEqual("Services Configuration Completed.", po_call_args[5][0][0])
        self.assertEqual("Skipping syncstores.", po_call_args[6][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[7][0][0])

        self.assertEqual(["pip", "install", "geojson"], mock_call.mock_calls[0][1][0])
        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[1][1][0])
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[2][1][0])
        self.assertEqual(["tethys", "db", "sync"], mock_call.mock_calls[3][1][0])

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.conda_run", return_value=["", "", 1])
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_without_dependencies(
        self, mock_pretty_output, mock_conda_run, mock_call, _
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=False,
            without_dependencies=True,
        )
        install_commands.install_command(args)

        # Ensure conda command wasn't called to install dependencies
        mock_conda_run.assert_not_called()

        # Make sure 'pip install' isn't in any of the calls
        self.assertFalse(
            any(
                ["pip install see" in " ".join(mc[1][0]) for mc in mock_call.mock_calls]
            )
        )

        # Validate output displayed to the user
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 7)
        self.assertEqual("Skipping package installation.", po_call_args[1][0][0])
        self.assertEqual("Running application install....", po_call_args[2][0][0])
        self.assertEqual(
            "Quiet mode: No additional service setting validation will be performed.",
            po_call_args[3][0][0],
        )
        self.assertEqual("Services Configuration Completed.", po_call_args[4][0][0])
        self.assertEqual("Skipping syncstores.", po_call_args[5][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[6][0][0])

        # Verify that the application install still happens
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[0][1][0])
        self.assertEqual(["tethys", "db", "sync"], mock_call.mock_calls[1][1][0])

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.conda_run", return_value=["", "", 1])
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_and_pip_package_install_only_dependencies(
        self, mock_pretty_output, mock_conda_run, mock_call, _
    ):
        chdir("..")
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=True,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        mock_conda_run.assert_called_with(
            Commands.INSTALL,
            "-c",
            "tacaswell",
            "--freeze-installed",
            "geojson",
            use_exception_handler=False,
            stdout=None,
            stderr=None,
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 6)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual("Running conda installation tasks...", po_call_args[1][0][0])
        self.assertIn(
            "Warning: Packages installation ran into an error.",
            po_call_args[2][0][0],
        )
        self.assertEqual("Running pip installation tasks...", po_call_args[3][0][0])
        self.assertEqual(
            "No public directory detected. Unable to process JavaScript dependencies.",
            po_call_args[4][0][0],
        )
        self.assertEqual(
            "Successfully installed dependencies for test_app.",
            po_call_args[5][0][0],
        )

        self.assertEqual(1, len(mock_call.mock_calls))
        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[0][1][0])

    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.conda_run", return_value=["", "", 1])
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_conda_and_pip_package_install_update_installed(
        self, mock_pretty_output, mock_conda_run, mock_call, _
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=True,
            no_db_sync=True,
            only_dependencies=False,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        mock_conda_run.assert_called_with(
            Commands.INSTALL,
            "-c",
            "tacaswell",
            "geojson",
            use_exception_handler=False,
            stdout=None,
            stderr=None,
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 7)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual(
            "Warning: Updating previously installed packages. This could break your Tethys environment.",
            po_call_args[1][0][0],
        )
        self.assertEqual("Running conda installation tasks...", po_call_args[2][0][0])
        self.assertIn(
            "Warning: Packages installation ran into an error.",
            po_call_args[3][0][0],
        )
        self.assertEqual("Running pip installation tasks...", po_call_args[4][0][0])
        self.assertEqual("Running application install....", po_call_args[5][0][0])
        self.assertEqual("Successfully installed test_app.", po_call_args[6][0][0])

        self.assertEqual(["pip", "install", "see"], mock_call.mock_calls[0][1][0])
        self.assertEqual(["pip", "install", "."], mock_call.mock_calls[1][1][0])

    @mock.patch("builtins.input", side_effect=["x", 5])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_custom_setting_set(self, mock_pretty_output, mock_gas, _):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}

        install_commands.run_interactive_services("foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertIn("Incorrect value type", po_call_args[5][0][0])
        self.assertIn("Enter the desired value", po_call_args[6][0][0])
        self.assertEqual(
            mock_cs.name + " successfully set with value: 5.",
            po_call_args[7][0][0],
        )

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "y"])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.getpass.getpass")
    @mock.patch("tethys_cli.install_commands.Path.exists")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.generate_salt_string")
    @mock.patch("tethys_cli.install_commands.yaml.safe_load")
    @mock.patch("tethys_cli.install_commands.yaml.dump")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.open",
        new_callable=lambda: mock.mock_open(read_data='{"secrets": "{}"}'),
    )
    def test_interactive_custom_setting_set_secret_no_previous_secret_file(
        self,
        mock_path_open,
        mock_pretty_output,
        mock_yml_dump,
        mock_yml_safe_load,
        mock_generate_salt_string,
        mock_subprocess_call,
        mock_path_exist,
        mock_get_pass,
        mock_gas,
        _,
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "SECRET"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_get_pass.return_value = "my_secret_string"
        mock_path_exist.side_effect = [False, True]
        mock_subprocess_call.return_value = mock.MagicMock()
        mock_generate_salt_string.return_value.decode.return_value = "my_salt_string"
        app_target_name = "foo"

        before_content = {
            "secrets": {
                app_target_name: {"custom_settings_salt_strings": {"mock_cs": ""}},
                "version": "1.0",
            }
        }

        after_content = {
            "secrets": {
                app_target_name: {
                    "custom_settings_salt_strings": {"mock_cs": "my_salt_string"}
                },
                "version": "1.0",
            }
        }

        mock_yml_safe_load.return_value = before_content

        install_commands.run_interactive_services("foo")

        mock_yml_dump.assert_called_once_with(
            after_content, mock_path_open.return_value
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("No secrets.yml found", po_call_args[4][0][0])
        self.assertIn("secrets file generated", po_call_args[5][0][0])
        self.assertIn("Successfully created salt string for", po_call_args[6][0][0])
        self.assertIn(
            "custom_settings_salt_strings created for setting",
            po_call_args[7][0][0],
        )
        self.assertIn("Enter the desired value", po_call_args[8][0][0])
        self.assertIn("Incorrect value type", po_call_args[9][0][0])
        self.assertIn("Enter the desired value", po_call_args[10][0][0])
        self.assertEqual(mock_cs.name + " successfully set", po_call_args[11][0][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "y"])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.getpass.getpass")
    @mock.patch("tethys_cli.install_commands.Path.exists")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.generate_salt_string")
    @mock.patch("tethys_cli.install_commands.yaml.safe_load")
    @mock.patch("tethys_cli.install_commands.yaml.dump")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.open",
        new_callable=lambda: mock.mock_open(read_data='{"secrets": "{}"}'),
    )
    def test_interactive_custom_setting_set_secret_with_previous_empty_secret_file(
        self,
        mock_path_open,
        mock_pretty_output,
        mock_yml_dump,
        mock_yml_safe_load,
        mock_generate_salt_string,
        mock_subprocess_call,
        mock_path_exist,
        mock_get_pass,
        mock_gas,
        _,
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "SECRET"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_get_pass.return_value = "my_secret_string"
        mock_path_exist.return_value = True
        mock_subprocess_call.return_value = mock.MagicMock()
        mock_generate_salt_string.return_value.decode.return_value = "my_salt_string"
        app_target_name = "foo"

        before_content_secret_empty = {"secrets": {"version": "1.0"}}

        after_content = {
            "secrets": {
                app_target_name: {
                    "custom_settings_salt_strings": {"mock_cs": "my_salt_string"}
                },
                "version": "1.0",
            }
        }

        mock_yml_safe_load.return_value = before_content_secret_empty

        install_commands.run_interactive_services("foo")

        mock_yml_dump.assert_called_once_with(
            after_content, mock_path_open.return_value
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("No custom_settings_salt_strings", po_call_args[4][0][0])
        self.assertIn("Successfully created salt string for", po_call_args[5][0][0])

        self.assertIn(
            "custom_settings_salt_strings created for setting",
            po_call_args[6][0][0],
        )

        self.assertIn("Enter the desired value", po_call_args[7][0][0])
        self.assertIn("Incorrect value type", po_call_args[8][0][0])
        self.assertIn("Enter the desired value", po_call_args[9][0][0])
        self.assertEqual(mock_cs.name + " successfully set", po_call_args[10][0][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "n"])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.getpass.getpass")
    @mock.patch("tethys_cli.install_commands.Path.exists")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.generate_salt_string")
    @mock.patch("tethys_cli.install_commands.yaml.safe_load")
    @mock.patch("tethys_cli.install_commands.yaml.dump")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.open",
        new_callable=lambda: mock.mock_open(read_data='{"secrets": "{}"}'),
    )
    def test_interactive_custom_setting_set_secret_without_salt_previous_empty_secret_file(
        self,
        mock_path_open,
        mock_pretty_output,
        mock_yml_dump,
        mock_yml_safe_load,
        mock_generate_salt_string,
        mock_subprocess_call,
        mock_path_exist,
        mock_get_pass,
        mock_gas,
        _,
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "SECRET"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_get_pass.return_value = "my_secret_string"
        mock_path_exist.return_value = True
        mock_subprocess_call.return_value = mock.MagicMock()
        mock_generate_salt_string.return_value.decode.return_value = "my_salt_string"
        app_target_name = "foo"
        before_content_secret_empty = {"secrets": {"version": "1.0"}}

        after_content = {
            "secrets": {
                app_target_name: {"custom_settings_salt_strings": {}},
                "version": "1.0",
            }
        }

        mock_yml_safe_load.return_value = before_content_secret_empty

        install_commands.run_interactive_services("foo")

        mock_yml_dump.assert_called_once_with(
            after_content, mock_path_open.return_value
        )
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn(
            "No custom_settings_salt_strings in the app definition",
            po_call_args[4][0][0],
        )
        self.assertIn(
            "custom_settings_salt_strings created for setting",
            po_call_args[5][0][0],
        )

        self.assertIn("Enter the desired value", po_call_args[6][0][0])
        self.assertIn("Incorrect value type", po_call_args[7][0][0])
        self.assertIn("Enter the desired value", po_call_args[8][0][0])
        self.assertEqual(mock_cs.name + " successfully set", po_call_args[9][0][0])

    @mock.patch("tethys_cli.install_commands.input", side_effect=["cat", "n"])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.getpass.getpass")
    @mock.patch("tethys_cli.install_commands.Path.exists")
    @mock.patch("tethys_cli.install_commands.call")
    @mock.patch("tethys_cli.install_commands.generate_salt_string")
    @mock.patch("tethys_cli.install_commands.yaml.safe_load")
    @mock.patch("tethys_cli.install_commands.yaml.dump")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.open",
        new_callable=lambda: mock.mock_open(read_data='{"secrets": "{}"}'),
    )
    def test_interactive_custom_setting_set_secret_with_salt_previous_empty_secret_file(
        self,
        mock_path_open,
        mock_pretty_output,
        mock_yml_dump,
        mock_yml_safe_load,
        mock_generate_salt_string,
        mock_subprocess_call,
        mock_path_exist,
        mock_get_pass,
        mock_gas,
        _,
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "SECRET"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_get_pass.return_value = "my_secret_string"
        mock_path_exist.return_value = True
        mock_subprocess_call.return_value = mock.MagicMock()
        mock_generate_salt_string.return_value.decode.return_value = "my_salt_string"
        app_target_name = "foo"

        before_content = {
            "secrets": {
                app_target_name: {"custom_settings_salt_strings": {"mock_cs": ""}},
                "version": "1.0",
            }
        }
        after_content = {
            "secrets": {
                app_target_name: {"custom_settings_salt_strings": {}},
                "version": "1.0",
            }
        }

        mock_yml_safe_load.return_value = before_content

        install_commands.run_interactive_services("foo")

        mock_yml_dump.assert_called_once_with(
            after_content, mock_path_open.return_value
        )

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn(
            "custom_settings_salt_strings created for setting",
            po_call_args[4][0][0],
        )
        self.assertIn("Enter the desired value", po_call_args[5][0][0])
        self.assertIn("Incorrect value type", po_call_args[6][0][0])
        self.assertIn("Enter the desired value", po_call_args[7][0][0])
        self.assertEqual(mock_cs.name + " successfully set", po_call_args[8][0][0])

    @mock.patch(
        "tethys_cli.install_commands.input",
        side_effect=[
            "cat",
            "y",
            "/fake/path/to/file",
            "y",
            "/fake/path/to/file",
        ],
    )
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.json.loads")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.open",
        new_callable=lambda: mock.mock_open(read_data='{"fake_json": "{}"}'),
    )
    def test_interactive_custom_setting_set_json_with_path(
        self, mock_path_open, mock_pretty_output, mock_json_loads, mock_gas, _
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "JSON"
        # mock_cs.save.side_effect = [mock.DEFAULT]
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_json_loads.return_value = mock_path_open.return_value
        install_commands.run_interactive_services("foo")
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertIn("Incorrect value type", po_call_args[5][0][0])
        self.assertIn("Enter the desired value", po_call_args[6][0][0])
        self.assertIn(mock_cs.name + " successfully set", po_call_args[7][0][0])

    @mock.patch(
        "tethys_cli.install_commands.input",
        side_effect=["cat", "y", "/fake/path/to/file"],
    )
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.json.loads")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    @mock.patch(
        "tethys_cli.install_commands.Path.read_text",
        return_value='{"fake_json": "{}"}',
    )
    def test_interactive_custom_setting_set_json_with_not_found_path(
        self, mock_read_text, mock_pretty_output, mock_json_loads, mock_gas, _
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "JSON"
        # mock_cs.save.side_effect = [mock.DEFAULT]
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        mock_json_loads.side_effect = [FileNotFoundError]
        install_commands.run_interactive_services("foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertIn("The current file path was not found", po_call_args[5][0][0])
        self.assertEqual("Skipping setup of " + mock_cs.name, po_call_args[6][0][0])

    @mock.patch(
        "tethys_cli.install_commands.input",
        side_effect=["cat", "n", '{"fake":"json"}', "n", '{"fake":"json"}'],
    )
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_custom_setting_set_json_without_path(
        self, mock_pretty_output, mock_gas, _
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "JSON"

        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        install_commands.run_interactive_services("foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertIn("Please provide a Json string", po_call_args[5][0][0])
        self.assertIn("Incorrect value type", po_call_args[6][0][0])
        self.assertIn("Enter the desired value", po_call_args[7][0][0])
        self.assertIn("Please provide a Json string", po_call_args[8][0][0])
        self.assertEqual(
            mock_cs.name + " successfully set with value: {'fake': 'json'}.",
            po_call_args[9][0][0],
        )

    @mock.patch(
        "tethys_cli.install_commands.input",
        side_effect=["cat", "n", "{'fake':'json'}"],
    )
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_custom_setting_set_json_without_path_error(
        self, mock_pretty_output, mock_gas, _
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.type_custom_setting = "JSON"

        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}
        install_commands.run_interactive_services("foo")
        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertIn("Please provide a Json string", po_call_args[5][0][0])
        self.assertIn("Invalid Json provided", po_call_args[6][0][0])
        self.assertIn("Skipping setup of mock_cs", po_call_args[7][0][0])

    @mock.patch("builtins.input", side_effect=[""])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_custom_setting_skip(self, mock_pretty_output, mock_gas, _):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}

        install_commands.run_interactive_services("foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertEqual(f"Skipping setup of {mock_cs.name}", po_call_args[5][0][0])

    @mock.patch("builtins.input", side_effect=KeyboardInterrupt)
    @mock.patch("tethys_cli.install_commands.exit")
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_custom_setting_interrupt(
        self, mock_pretty_output, mock_gas, mock_exit, _
    ):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_gas.return_value = {"unlinked_settings": [mock_cs]}

        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, install_commands.run_interactive_services, "foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn("Configuring mock_cs", po_call_args[2][0][0])
        self.assertIn("Type", po_call_args[3][0][0])
        self.assertIn("Enter the desired value", po_call_args[4][0][0])
        self.assertEqual("\nInstall Command cancelled.", po_call_args[5][0][0])

        mock_exit.assert_called_with(0)

    @mock.patch(
        "builtins.input",
        side_effect=["1", "1", "", "1", "1", KeyboardInterrupt],
    )
    @mock.patch(
        "tethys_cli.install_commands.validate_service_id",
        side_effect=[False, True],
    )
    @mock.patch(
        "tethys_cli.install_commands.get_setting_type",
        return_value="persistent",
    )
    @mock.patch(
        "tethys_cli.install_commands.get_setting_type_from_setting",
        side_effect=[
            "ps_database",
            "ps_database",
            "ps_database",
            RuntimeError("setting_type_not_found"),
        ],
    )
    @mock.patch(
        "tethys_cli.install_commands.get_service_type_from_setting",
        side_effect=[
            "persistent",
            "persistent",
            RuntimeError("service_type_not_found"),
            "persistent",
        ],
    )
    @mock.patch("tethys_cli.install_commands.exit")
    @mock.patch("tethys_cli.install_commands.services_list_command")
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.install_commands.link_service_to_app_setting")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_service_setting_all(
        self,
        mock_pretty_output,
        mock_lstas,
        mock_gas,
        mock_slc,
        mock_exit,
        _,
        __,
        ___,
        ____,
        _____,
    ):
        mock_ss = mock.MagicMock()
        del mock_ss.value
        mock_ss.name = "mock_ss"
        mock_ss.description = "This is a fake setting for testing."
        mock_ss.required = True
        mock_ss.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = {
            "unlinked_settings": [
                mock_ss,
                mock_ss,
                mock_ss,
                mock_ss,
                mock_ss,
                mock_ss,
            ]
        }

        mock_s = mock.MagicMock()
        mock_slc.side_effect = [
            [[]],
            [[mock_s]],
            [[mock_s]],
            [[mock_s]],
            [[mock_s]],
            [[mock_s]],
        ]

        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, install_commands.run_interactive_services, "foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(
            "Running Interactive Service Mode. Any configuration options in services.yml or "
            "portal_config.yml will be ignored...",
            po_call_args[0][0][0],
        )
        self.assertIn("Hit return at any time to skip a step.", po_call_args[1][0][0])
        self.assertIn("Configuring mock_ss", po_call_args[2][0][0])
        self.assertIn("Type: MagicMock", po_call_args[3][0][0])
        self.assertIn(f"Description: {mock_ss.description}", po_call_args[3][0][0])
        self.assertIn(f"Required: {mock_ss.required}", po_call_args[3][0][0])
        self.assertIn("No compatible services found.", po_call_args[4][0][0])
        self.assertIn("tethys services create persistent -h", po_call_args[4][0][0])
        self.assertIn("Enter the service ID/Name", po_call_args[7][0][0])
        self.assertIn(
            "Incorrect service ID/Name. Please try again.",
            po_call_args[8][0][0],
        )
        self.assertIn("Enter the service ID/Name", po_call_args[9][0][0])
        self.assertIn(f"Skipping setup of {mock_ss.name}", po_call_args[13][0][0])
        self.assertEqual("service_type_not_found Skipping...", po_call_args[17][0][0])
        self.assertEqual("setting_type_not_found Skipping...", po_call_args[21][0][0])
        self.assertEqual("\nInstall Command cancelled.", po_call_args[25][0][0])

        mock_lstas.assert_called_with(
            "persistent", "1", "foo", "ps_database", "mock_ss"
        )
        mock_exit.assert_called_with(0)

    @mock.patch("builtins.input", side_effect=["x", 5])
    @mock.patch("tethys_cli.install_commands.get_app_settings")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_interactive_no_settings(self, mock_pretty_output, mock_gas, _):
        mock_cs = mock.MagicMock()
        mock_cs.name = "mock_cs"
        mock_cs.save.side_effect = [ValidationError("error"), mock.DEFAULT]
        mock_gas.return_value = None

        install_commands.run_interactive_services("foo")

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertIn(
            'No settings found for app "foo". Skipping interactive configuration...',
            po_call_args[2][0][0],
        )

    @mock.patch("tethys_cli.install_commands.Path.exists", return_value=True)
    @mock.patch("tethys_cli.install_commands.Path.open")
    @mock.patch(
        "tethys_cli.install_commands.open_file",
        return_value={
            "name": "test_app",
            "requirements": {"npm": {"test": "1.1.1"}},
        },
    )
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.download_vendor_static_files")
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_npm_install(
        self,
        mock_pretty_output,
        mock_download,
        _,
        __,
        mock_open,
        mock_exists,
    ):
        file_path = self.root_app_path / "install-npm-dep.yml"
        import io

        mock_open.return_value.__enter__.return_value = mock.MagicMock(spec=io.StringIO)
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=True,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 2)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual(
            "Successfully installed dependencies for test_app.",
            po_call_args[1][0][0],
        )

        self.assertEqual(1, len(mock_download.mock_calls))
        self.assertEqual(
            {"cwd": str(Path("tethysapp/test_app/public"))},
            mock_download.mock_calls[0][2],
        )

        mock_exists.assert_called()

    @mock.patch(
        "tethys_cli.install_commands.open_file",
        return_value={
            "name": "test_app",
            "requirements": {"npm": {"test": "1.1.1"}},
        },
    )
    @mock.patch("tethys_cli.install_commands.run_services")
    @mock.patch("tethys_cli.install_commands.isinstance", return_value=False)
    @mock.patch("tethys_cli.cli_colors.pretty_output")
    def test_npm_install_formatting_error(
        self, mock_pretty_output, mock_isinstance, _, mock_open
    ):
        file_path = self.root_app_path / "install-dep.yml"
        args = mock.MagicMock(
            file=file_path,
            develop=False,
            verbose=False,
            services_file=None,
            update_installed=False,
            no_db_sync=False,
            only_dependencies=True,
            without_dependencies=False,
        )
        install_commands.install_command(args)

        po_call_args = mock_pretty_output().__enter__().write.call_args_list
        self.assertEqual(len(po_call_args), 3)
        self.assertEqual("Installing dependencies...", po_call_args[0][0][0])
        self.assertEqual(
            "The npm requirements are not formatted correctly. "
            'It should be provided as key-value (e.g. "package_name: 1.0").',
            po_call_args[1][0][0],
        )
        self.assertEqual(
            "Successfully installed dependencies for test_app.",
            po_call_args[2][0][0],
        )
