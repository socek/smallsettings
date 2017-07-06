from mock import patch
from os import sep

from .base import TestCase
from morfdict import Paths
from morfdict import StringDict


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

    def test_error(self):
        settings = StringDict({'name': 'value'})
        self.assertEqual([], settings.get_errors())

        settings['error'] = '%(errorkey)s'
        self.assertEqual(KeyError, type(settings.get_errors()[0]))


class AccessorsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.data = StringDict(
            {'name': 'one', 'two': {'mix': '10', 'second': '25'}})

    def test_simple_get(self):
        self.assertRaises(KeyError, lambda: self.data['two:mix'])
        self.assertEqual('10', self.data['two']['mix'])

    def test_deep_setter(self):
        self.data['three:mix'] = '15'
        self.assertEqual('15', self.data['three:mix'])
        self.assertRaises(KeyError, lambda: self.data['three']['mix'])

    def test_deep_setter_already_made(self):
        self.data['two:mix'] = '20'

        self.assertEqual('20', self.data['two:mix'])
        self.assertRaises(KeyError, lambda: self.data['two:second'])
        self.assertEqual('10', self.data['two']['mix'])
        self.assertEqual('25', self.data['two']['second'])


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
        self.assertRaises(KeyError, lambda: self.parent1['morf_child'])

    def test_get_default_error(self):
        self.assertRaises(KeyError, self.child.get, 'morf3_parent', 'default')

    def test_get_default(self):
        self.assertEqual([], self.child.get('jinja2.extensions', []))

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

        self.parent1['morf_child'] = 'none'
        newsettings.merge(self.parent1)
        newsettings['parent_key'] = 'newpar'
        newsettings['parent3_key'] = 'par3'

        self.assertEqual({
            'my_data': {
                'elf': '10',
            },
            'morf_child': 'none',
            'mychild': {
                'child_key': 'child1',
                'morf2_parent': 'parent2 morf',
                'morf3_parent': 'par3 morf',
                'morf_parent': 'parent1 morf'},
            'mychild:second': '30',
            'parent_key': 'newpar',
            'parent3_key': 'par3',
        }, newsettings.to_dict())


class PathsTest(TestCase):

    def test_get_set(self):
        paths = Paths()
        paths.set('mypath', 'elo')
        paths.set('mypath2', 'elo2', 'mypath')
        paths.set('mypath3', 'elo3', None, True)

        self.assertEqual('elo', paths.get('mypath'))
        self.assertEqual('elo' + sep + 'elo2', paths.get('mypath2'))
        self.assertEqual(sep + 'elo3', paths.get('mypath3'))

    def test_set_generator(self):
        paths = Paths()
        paths.set('mypath', 'elo')
        paths.set_generator(
            'myelo',
            lambda parent: parent.get('mypath') + 'two',
            parent='mypath',
            is_root=True)

        self.assertEqual(paths.get('myelo'), '/elo/elotwo')

    def test_set_long_path(self):
        paths = Paths()
        paths.set('mypath', ['elo', 'some', 'thing'])

        self.assertEqual(paths.get('mypath'), 'elo{0}some{0}thing'.format(sep))

    def test_to_dict(self):
        paths = Paths()
        paths.set('Nfirst', 'one')
        paths.set('Nsecond', 'two', 'Nfirst')
        paths.set('Nthird', 'three', is_root=True)
        paths.set('Nfourth', 'four', 'Nthird')
        paths.set_generator(
            'Nfifth', lambda parent: parent.get('Nfourth') + 'five')

        self.assertEqual(paths.to_dict(), {
            'Nfirst': 'one',
            'Nsecond': 'one{0}two'.format(sep),
            'Nthird': '{0}three'.format(sep),
            'Nfourth': '{0}three{0}four'.format(sep),
            'Nfifth': '{0}three{0}fourfive'.format(sep),
        })

    @patch('morfdict.models.import_module')
    def test_get_path_from_module(self, mimport_module):
        mimport_module.return_value.__file__ = 'module/path/__init__.py'

        paths = Paths()
        self.assertEqual(
            paths.get_path_from_module('test.me:something/elo'),
            'module/path/something/elo',
        )

    @patch('morfdict.models.import_module')
    def test_get_path_from_module_no_file(self, mimport_module):
        mimport_module.return_value.__file__ = 'module/path/__init__.py'

        paths = Paths()
        self.assertEqual(
            paths.get_path_from_module('test.me'),
            'module/path/__init__.py',
        )

    def test_errors(self):
        paths = Paths()

        self.assertEqual([], paths.get_errors())

        paths.set('name', 'val', is_root=True)
        self.assertEqual([], paths.get_errors())

        paths.set('name', 'val', parent='me')
        self.assertEqual(KeyError, type(paths.get_errors()[0]))

        paths.set('me', 'val')
        self.assertEqual([], paths.get_errors())


class PathsContextTest(TestCase):

    def setUp(self):
        self.paths = Paths()

        with self.paths.set('base', '/tmp', is_root=True) as base:
            with base.set('hello', 'hello') as hello:
                hello.set('name', 'name1')
                hello.set('name2', 'name2')

    def test_get(self):
        assert self.paths.get('name') == '/tmp/hello/name1'
        assert self.paths.get('name2') == '/tmp/hello/name2'

    def test_set_by_context(self):
        with self.paths.set('hello', 'hello', parent='base') as hello:
            hello.set('name', 'name3')
            hello.set('name2', 'name4')

        assert self.paths.get('name') == '/tmp/hello/name3'
        assert self.paths.get('name2') == '/tmp/hello/name4'

    def test_switch_context(self):
        with self.paths.context('base') as base:
            with base.context('hello') as hello:
                hello.set('name', 'name5')
                hello.set('name2', 'name6')

                assert hello.get('name') == '/tmp/hello/name5'
                assert hello.get('name2') == '/tmp/hello/name6'

        assert self.paths.get('name') == '/tmp/hello/name5'
        assert self.paths.get('name2') == '/tmp/hello/name6'


class TestTreePaths(TestCase):

    def test_empty_paths(self):
        paths = Paths()
        self.assertEqual(paths.to_tree(), '')

    def test_one_root(self):
        paths = Paths()
        paths.set('maineme', '', is_root=True)
        self.assertEqual(
            '''/: #maineme
''',
            paths.to_tree())

    def test_simple_tree(self):
        paths = Paths()
        paths.set('maineme', 'main')
        paths.set('m2', 'second', 'maineme')
        paths.set('m3', 'third', 'maineme')
        paths.set('m4', 'fourth', 'm3')
        self.assertEqual(
            '''main: #maineme
    second: #m2
    third: #m3
        fourth: #m4
''',
            paths.to_tree())

    def test_big_paths(self):
        paths = Paths()
        paths.set('cwd', 'src')
        paths.set('pyproject', 'home')
        paths.set('pyptemplates', 'templates', 'pyproject')

        paths.set('package:src', 'src', 'cwd')
        paths.set_generator(
            'package:main', lambda paths: 'samlepackage', 'package:src')
        paths.set(
            'template_setuppy',
            'setuppy.jinja2',
            'pyptemplates',
        )
        paths.set('setuppy', 'setup.py', 'cwd')

        paths.set('virtualenv:bin', 'bin', 'virtualenv:base')
        paths.set('exe:python', 'python', 'virtualenv:bin')
        paths.set('exe:pip', 'pip', 'virtualenv:bin')
        paths.set_generator(
            'virtualenv:base',
            lambda paths: 'venv_{0}'.format('samlepackage'),
            'cwd',
        )
        paths.set('report', '.bael.yml', 'cwd')

        self.assertEqual(
            '''src: #cwd
    src: #package:src
        samlepackage: #package:main
    setup.py: #setuppy
    venv_samlepackage: #virtualenv:base
        bin: #virtualenv:bin
            python: #exe:python
            pip: #exe:pip
    .bael.yml: #report
home: #pyproject
    templates: #pyptemplates
        setuppy.jinja2: #template_setuppy
''',
            paths.to_tree(),)
