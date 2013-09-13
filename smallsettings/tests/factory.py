from mock import patch, MagicMock
from contextlib import nested

from smallsettings.tests.base import TestCase
from smallsettings import Factory


class FactoryTest(TestCase):

    def setUp(self):
        super(FactoryTest, self).setUp()
        self.factory = Factory('main_modulepath', 'settings_modulepath')

        self.patchers = {}
        self.mocks = {}

        self._init_patchers()
        self._start_patchers()

    def _start_patchers(self):
        for name, patcher in self.patchers.items():
            self.mocks[name] = patcher.start()

    def _init_patchers(self):
        self.patchers['import'] = patch.object(self.factory, '_import_wrapper')

    def test_init(self):
        self.assertEqual('main_modulepath', self.factory.main_modulepath)
        self.assertEqual(
            'settings_modulepath', self.factory.settings_modulepath)

    def test_import(self):
        self.factory.import_module('something')
        self.mocks['import'].assert_called_once_with(
            'main_modulepath.settings_modulepath.something')

    def test_run_module(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with patch.object(self.factory, 'import_module') as import_module:
            self.factory.run_module('some_name')

            import_module.assert_called_once_with('some_name')
            module = import_module.return_value
            module.make_settings.assert_called_once_with(
                self.factory.settings, self.factory.paths)

    def test_run_module_error(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with patch.object(self.factory, 'import_module') as import_module:
            module = import_module.return_value
            module.make_settings.side_effect = ImportError()

            self.assertRaises(
                ImportError, self.factory.run_module, 'some_name')

            module.make_settings.assert_called_once_with(
                self.factory.settings, self.factory.paths)
            import_module.assert_called_once_with('some_name')

    def test_run_module_without_errors(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with patch.object(self.factory, 'import_module') as import_module:
            self.factory.run_module_without_errors('some_name')

            import_module.assert_called_once_with('some_name')
            module = import_module.return_value
            module.make_settings.assert_called_once_with(
                self.factory.settings, self.factory.paths)

    def test_run_module_without_errors_error(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with patch.object(self.factory, 'import_module') as import_module:
            module = import_module.return_value
            module.make_settings.side_effect = ImportError()

            self.factory.run_module_without_errors('some_name')

            import_module.assert_called_once_with('some_name')
            module.make_settings.assert_called_once_with(
                self.factory.settings, self.factory.paths)

    def test_init_data(self):
        self.mocks['import'].return_value.__file__ = '/one/two/three.py'
        self.factory.init_data({'settings': 1}, {'paths': 'path'})

        self.assertEqual({'settings': 1}, self.factory.settings.data)
        self.assertEqual(
            {'paths': ['path', ], 'project_path': ['/one/two']}, self.factory.paths.data)

    def test_make_settings(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with nested(
                patch.object(self.factory, 'init_data'),
                patch.object(self.factory, 'run_module'),
                patch.object(self.factory, 'run_module_without_errors'),
        ) as (init_data, run_module, run_module_without_errors):
            result = self.factory.make_settings(
                {'settings': 1}, {'paths': 'path'}, additional_module_name='local1', additional_module_error=False)

            self.assertEqual((self.factory.settings, self.factory.paths), result)
            init_data.assert_called_once_with({'settings': 1}, {'paths': 'path'})
            run_module.assert_called_once_with('default')
            run_module_without_errors.assert_called_once_with('local1')

    def test_make_settings_with_error(self):
        self.factory.settings = MagicMock()
        self.factory.paths = MagicMock()
        with nested(
                patch.object(self.factory, 'init_data'),
                patch.object(self.factory, 'run_module'),
                patch.object(self.factory, 'run_module_without_errors'),
        ) as (init_data, run_module, run_module_without_errors):
            result = self.factory.make_settings(
                {'settings': 1}, {'paths': 'path'}, additional_module_name='local1', additional_module_error=True)

            self.assertEqual((self.factory.settings, self.factory.paths), result)
            init_data.assert_called_once_with({'settings': 1}, {'paths': 'path'})
            run_module.assert_called_with('local1')
            self.assertEqual(2, run_module.call_count)
            self.assertEqual(0, run_module_without_errors.call_count)
