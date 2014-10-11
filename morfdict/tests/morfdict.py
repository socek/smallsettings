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


class ParrentsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.parent1 = StringDict({'parent_key': 'parent1'})
        self.parent2 = StringDict({'parent2_key': 'parent2'})
        self.child = StringDict({'child_key': 'child1'})
        self.child['morf_parent'] = '%(parent_key)s morf'
        self.child['morf2_parent'] = '%(parent2_key)s morf'
        self.child['morf3_parent'] = '%(parent3_key)s morf'

        self.child.append_parent(self.parent1)
        self.parent2['child'] = self.child

        self.parent1['mychild'] = self.child
        self.parent1['morf_child'] = '%(mychild:morf_parent)s morf child'

    def test_morf_parent(self):
        self.assertEqual('parent1 morf', self.child['morf_parent'])
        self.assertEqual('parent2 morf', self.child['morf2_parent'])

    def test_morf_error(self):
        self.assertRaises(KeyError, self.child.get, 'morf3_parent')

    def test_morf_child(self):
        self.assertEqual('parent1 morf morf child', self.parent1['morf_child'])

    def test_get_default_error(self):
        self.assertRaises(KeyError, self.child.get, 'morf3_parent', 'default')

    def test_get_default(self):
        self.assertEqual([], self.child.get('jinja2.extensions', []))

    def test_to_dict(self):
        paths = PathDict()
        paths.append_parent(self.parent1, 'paths')
        paths['root'] = ['/tmp', 'elo']
        paths.set_path('my', 'root', 'self')
        del self.child['morf3_parent']

        self.assertEqual({
            'morf_child': 'parent1 morf morf child',
            'mychild': {
                'child_key': 'child1',
                'morf2_parent': 'parent2 morf',
                'morf_parent': 'parent1 morf'},
            'parent_key': 'parent1',
            'paths': {
                'my': '/tmp/elo/self',
                'root': '/tmp/elo'}
        }, self.parent1.to_dict())

    def test_setter(self):
        self.assertEqual(True, self.parent2 in self.child._parents)
