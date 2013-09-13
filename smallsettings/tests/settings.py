from .base import TestCase
from smallsettings import Settings, Paths, Merged


class SettingsTest(TestCase):

    def test_simple_assign(self):
        settings = Settings()
        settings['name'] = 'value'
        self.assertEqual('value', settings['name'])

    def test_assign_with_value_name(self):
        settings = Settings()
        settings['name'] = 'value'
        settings['name_two'] = '%(name)s value2'
        self.assertEqual('value value2', settings['name_two'])

    def test_assign_with_value_swith(self):
        settings = Settings()
        settings['name'] = 'value'
        settings['name_two'] = '%(name)s value2'
        settings['name'] = 'value3'
        self.assertEqual('value3 value2', settings['name_two'])

    def test_initial_data(self):
        settings = Settings({'name': 'value'})
        self.assertEqual('value', settings['name'])

    def test_contains_true(self):
        settings = Settings({'name': 'value'})
        self.assertTrue('name' in settings)

    def test_contains_false(self):
        settings = Settings({'name': 'value'})
        self.assertFalse('name2' in settings)

    def test_merging(self):
        settings = Settings({'name': 'value'})
        settings2 = Settings({'name2': 'value'})
        merged = settings.merged(settings2)
        self.assertEqual(Merged, type(merged))


class PathsTest(TestCase):

    def test_simple_assign(self):
        paths = Paths()
        paths['name'] = 'value'
        self.assertEqual('value', paths['name'])

    def test_assign_with_value_name(self):
        paths = Paths()
        paths['name'] = '/value'
        paths['name_two'] = ['%(name)s', 'value2']
        self.assertEqual('/value/value2', paths['name_two'])

    def test_assign_with_value_swith(self):
        paths = Paths()
        paths['name'] = '/value'
        paths['name_two'] = ['%(name)s', 'value2']
        paths['name'] = '/value3'
        self.assertEqual('/value3/value2', paths['name_two'])

    def test_initial_data(self):
        paths = Paths({'name': 'value'})
        self.assertEqual('value', paths['name'])

    def test_contains_true(self):
        paths = Paths({'name': 'value'})
        self.assertTrue('name' in paths)

    def test_contains_false(self):
        paths = Paths({'name': 'value'})
        self.assertFalse('name2' in paths)

    def test_merging(self):
        paths = Paths({'name': 'value'})
        paths2 = Paths({'name2': 'value'})
        merged = paths.merged(paths2)
        self.assertEqual(Merged, type(merged))


class MergedTest(TestCase):

    def setUp(self):
        super(MergedTest, self).setUp()
        self.sett1 = Settings({'one': 1})
        self.sett2 = Settings({'two': 2})
        self.merged = Merged([self.sett1, self.sett2])

    def test_getitem(self):
        self.assertEqual(1, self.merged['one'])
        self.assertEqual(2, self.merged['two'])

        self.assertRaises(KeyError, self.merged.__getitem__, 'three')

    def test_contains(self):
        self.assertTrue('one' in self.merged)
        self.assertTrue('two' in self.merged)
        self.assertFalse('three' in self.merged)

    def test_merge(self):
        sett3 = Paths()
        self.merged.merge(sett3)

        self.assertEqual(
            [self.sett1, self.sett2, sett3], self.merged.settings_list)
