from unittest import mock, TestCase

from django.test.utils import override_settings

from tethys_cli import settings_commands as cmds


class TestSettingsCommands(TestCase):

    def set_up(self):
        pass

    def tear_down(self):
        pass

    @mock.patch('tethys_cli.settings_commands.yaml.safe_load', return_value={'settings': {'test': 'test'}})
    def test_read_settings(self, _):
        settings = cmds.read_settings()
        self.assertDictEqual(settings, {'test': 'test'})

    @mock.patch('tethys_cli.settings_commands.Path.open', return_value='mock_file')
    @mock.patch('tethys_cli.settings_commands.yaml.safe_load', return_value={})
    @mock.patch('tethys_cli.settings_commands.yaml.safe_dump')
    def test_write_settings(self, mock_dump, _, __):
        cmds.write_settings({'test': 'test'})
        mock_dump.assert_called_with({'settings': {'test': 'test'}}, 'mock_file')

    @mock.patch('tethys_cli.settings_commands._get_dict_key_handle')
    @mock.patch('tethys_cli.settings_commands.write_settings')
    def test_set_settings(self, mock_write_settings, mock_get_key):
        test_settings = {}
        mock_get_key.return_value = (test_settings, 'test')
        cmds.set_settings(test_settings, [('test', 'test')])
        self.assertDictEqual(test_settings, {'test': 'test'})
        mock_write_settings.assert_called_with(test_settings)

    @mock.patch('tethys_cli.settings_commands.write_info')
    @mock.patch('tethys_cli.settings_commands._get_dict_key_handle')
    def test_get_setting(self, mock_get_key, mock_write_info):
        test_settings = {'test_key': 'test_value'}
        mock_get_key.return_value = (test_settings, 'test_key')
        cmds.get_setting(test_settings, 'test_key')
        mock_write_info.assert_called_with('test_key: test_value')

    @override_settings(test_key='test_value')
    @mock.patch('tethys_cli.settings_commands.write_info')
    def test_get_setting_from_django_settings(self, mock_write_info):
        test_settings = {'test_key': 'test_value'}
        cmds.get_setting(test_settings, 'test_key')
        mock_write_info.assert_called_with('test_key: test_value')

    @mock.patch('tethys_cli.settings_commands._get_dict_key_handle')
    @mock.patch('tethys_cli.settings_commands.write_settings')
    def test_remove_setting(self, mock_write_settings, mock_get_key):
        test_settings = {'test_key': 'test_value'}
        mock_get_key.return_value = (test_settings, 'test_key')
        cmds.remove_setting(test_settings, 'test_key')
        self.assertDictEqual(test_settings, {})
        mock_write_settings.assert_called_with(test_settings)

    def test__get_dict_key_handle(self):
        d = {'test': {'test1': 'test'}}
        result = cmds._get_dict_key_handle(d, 'test.test1')
        self.assertEqual(result, (d['test'], 'test1'))

    def test__get_dict_key_handle_key_not_exists(self):
        d = {'test': 'test'}
        result = cmds._get_dict_key_handle(d, 'test1', not_exists_okay=True)
        self.assertEqual(result, (d, 'test1'))
        result = cmds._get_dict_key_handle(d, 'test1.test2', not_exists_okay=True)
        self.assertEqual(result, ({}, 'test2'))

    @mock.patch('tethys_cli.settings_commands.write_error')
    def test__get_dict_key_handle_error(self, mock_write_error):
        d = {'test': 'test'}
        cmds._get_dict_key_handle(d, 'test1')
        mock_write_error.assert_called()

    @mock.patch('tethys_cli.settings_commands.set_settings')
    @mock.patch('tethys_cli.settings_commands.read_settings', return_value={})
    def test_settings_command_set(self, _, mock_set_settings):
        kwargs = [('key', 'value')]
        mock_args = mock.MagicMock(set_kwargs=kwargs)
        cmds.settings_command(mock_args)
        mock_set_settings.assert_called_with({}, kwargs)

    @mock.patch('tethys_cli.settings_commands.get_setting')
    @mock.patch('tethys_cli.settings_commands.read_settings', return_value={})
    def test_settings_command_get(self, _, mock_get_setting):
        get_key = ['key']
        mock_args = mock.MagicMock(set_kwargs=None, get_key=get_key)
        cmds.settings_command(mock_args)
        mock_get_setting.assert_called_with({}, get_key[0])

    @mock.patch('tethys_cli.settings_commands.remove_setting')
    @mock.patch('tethys_cli.settings_commands.read_settings', return_value={})
    def test_settings_command_rm(self, _, mock_remove_setting):
        rm_key = ['key']
        mock_args = mock.MagicMock(set_kwargs=None, get_key=None, rm_key=rm_key)
        cmds.settings_command(mock_args)
        mock_remove_setting.assert_called_with({}, rm_key[0])
