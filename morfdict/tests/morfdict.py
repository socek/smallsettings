from .base import TestCase
from morfdict import StringDict, PathDict


class StringDictTest(TestCase):

    def test_simple_assign(self):
        settings = StringDict()
        settings['name'] = 'value'
        self.assertEqual('value', settings['name'])

    def test_assign_with_value_name(self):
        settings = StringDict()
        settings['name'] = 'value'
        settings['name_two'] = '%(name)s value2'
        self.assertEqual('value value2', settings['name_two'])

    def test_assign_with_value_swith(self):
        settings = StringDict()
        settings['name'] = 'value'
        settings['name_two'] = '%(name)s value2'
        settings['name'] = 'value3'
        self.assertEqual('value3 value2', settings['name_two'])

    def test_initial_data(self):
        settings = StringDict({'name': 'value'})
        self.assertEqual('value', settings['name'])

    def test_contains_true(self):
        settings = StringDict({'name': 'value'})
        self.assertTrue('name' in settings)

    def test_contains_false(self):
        settings = StringDict({'name': 'value'})
        self.assertFalse('name2' in settings)


class PathDictTest(TestCase):

    def test_simple_assign(self):
        paths = PathDict()
        paths['name'] = 'value'
        self.assertEqual('value', paths['name'])

    def test_assign_with_value_name(self):
        paths = PathDict()
        paths['name'] = '/value'
        paths['name_two'] = ['%(name)s', 'value2']
        self.assertEqual('/value/value2', paths['name_two'])

    def test_assign_with_value_swith(self):
        paths = PathDict()
        paths['name'] = '/value'
        paths['name_two'] = ['%(name)s', 'value2']
        paths['name'] = '/value3'
        self.assertEqual('/value3/value2', paths['name_two'])

    def test_initial_data(self):
        paths = PathDict({'name': 'value'})
        self.assertEqual('value', paths['name'])

    def test_contains_true(self):
        paths = PathDict({'name': 'value'})
        self.assertTrue('name' in paths)

    def test_contains_false(self):
        paths = PathDict({'name': 'value'})
        self.assertFalse('name2' in paths)


class MorfingTest(TestCase):

    def test_morfing(self):
        def simple_morf(obj, value):
            return value + '***'

        data = StringDict({'key': 'value', 'key2': 'v2'})
        self.assertEqual('value', data['key'])
        self.assertEqual('v2', data['key2'])

        data.set_morf('key', simple_morf)
        self.assertEqual('value***', data['key'])
        self.assertEqual('v2', data['key2'])
