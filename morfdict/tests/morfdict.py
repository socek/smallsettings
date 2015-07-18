from mock import patch

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


class AccessorsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = StringDict(
            {'name': 'one', 'two': {'mix': '10', 'second': '25'}})

    def test_simple_get(self):
        self.assertEqual('10', self.data['two:mix'])
        self.assertEqual('10', self.data['two']['mix'])

    def test_deep_setter(self):
        self.data['three:mix'] = '15'
        self.assertEqual('15', self.data['three:mix'])
        self.assertEqual('15', self.data['three']['mix'])

    def test_deep_setter_already_made(self):
        self.data['two:mix'] = '20'

        self.assertEqual('20', self.data['two:mix'])
        self.assertEqual('25', self.data['two:second'])
        self.assertEqual('20', self.data['two']['mix'])
        self.assertEqual('25', self.data['two']['second'])

    def test_paths(self):
        paths = PathDict()

        paths['one'] = 'xxx'
        paths['three:mix'] = ['%(one)s', '10', '15']
        self.assertEqual('xxx/10/15', paths['three:mix'])
        self.assertEqual('xxx/10/15', paths['three']['mix'])

    def test_cross_nameing(self):
        paths = PathDict()
        paths['project:home'] = 'myho'
        paths['project:application'] = ['%(project:home)s', 'application']
        paths['application:tests'] = ['%(project:application)s', 'tests']

        self.assertEqual('myho/application/tests', paths['application:tests'])


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

    @patch('morfdict.models.import_module')
    def test_get_path_dotted(self, mimport_module):
        mimport_module.return_value.__file__ = 'module/path/__init__.py'

        paths = PathDict()
        self.assertEqual(
            paths.get_path_dotted('test.me:something/elo'),
            'module/path/something/elo',
        )

    @patch('morfdict.models.import_module')
    def test_get_path_dotted_no_file(self, mimport_module):
        mimport_module.return_value.__file__ = 'module/path/__init__.py'

        paths = PathDict()
        self.assertEqual(
            paths.get_path_dotted('test.me'),
            'module/path/__init__.py',
        )


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

    def test_items(self):
        data = list(self.child.items())
        data.sort()
        expected_data = [
            ('child_key', 'child1'),
            ('morf2_parent', 'parent2 morf'),
            ('morf_parent', 'parent1 morf')]
        self.assertEqual(expected_data, data)

    def test_merge(self):
        newsettings = StringDict()
        newsettings['my_data'] = {}
        newsettings['my_data']['elf'] = '10'
        newsettings['mychild:second'] = '30'

        newsettings.merge(self.parent1)
        newsettings['parent_key'] = 'newpar'
        newsettings['parent3_key'] = 'par3'

        self.assertEqual({
            'my_data': {
                'elf': '10',
            },
            'morf_child': 'newpar morf morf child',
            'mychild': {
                'child_key': 'child1',
                'morf2_parent': 'parent2 morf',
                'morf3_parent': 'par3 morf',
                'morf_parent': 'newpar morf',
                'second': '30'},
            'parent_key': 'newpar',
            'parent3_key': 'par3',
        }, newsettings.to_dict())
