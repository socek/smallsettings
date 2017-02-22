from collections import namedtuple
from importlib import import_module
from os import path
from os import sep

PathElement = namedtuple('PathElement', ['parent', 'value', 'is_root'])


class NoDefault:
    pass


class MorfDict(dict):

    def __init__(self, data={}, morf=None):
        """
        :param data: dict of normal data
        :param morf: dict of morf methods
        """
        super(MorfDict, self).__init__()
        self._morf = morf or {}
        self._parents = []

        for name, value in data.items():
            self[name] = value

    def __getitem__(self, key):
        left, right = self._split_key(key)
        value = self._get_from_self_or_parent(left)
        if right:
            value = value[right]
        method = self._morf.get(key, self._default_morf)
        return method(self, value)

    def _split_key(self, huge_key):
        try:
            left, right = huge_key.split(':', 1)
            return left, right
        except:
            return huge_key, None

    def _raw_get(self, key):
        return super().__getitem__(key)

    def _get_from_self_or_parent(self, key):
        for obj in [super(MorfDict, self)] + self._parents:
            try:
                return obj.__getitem__(key)
            except KeyError:
                continue
        raise KeyError(key)

    def append_parent(self, parent, key=None):
        """Add parent to this object."""
        self._parents.append(parent)
        if key:
            parent[key] = self

    def _default_morf(self, obj, value):
        return value

    def __setitem__(self, key, value):
        def convert_dict_to_morfdict_if_avalible(value):
            if type(value) is dict:
                return self.__class__(value)
            return value

        def append_parent_if_avalible(value):
            if isinstance(value, MorfDict):
                value.append_parent(self)

        def make_set(key, value):
            return super(MorfDict, self).__setitem__(key, value)

        def set_child_morfdict(left, right, value):
            # if there is key with ':' it should make child morf dict and
            # insert data to it
            if left not in self:
                data = self.__class__()
                data.append_parent(self)
            else:
                data = self[left]
            data[right] = value
            return make_set(left, data)

        value = convert_dict_to_morfdict_if_avalible(value)
        append_parent_if_avalible(value)

        left, right = self._split_key(key)
        if right is None:
            return make_set(key, value)
        else:
            return set_child_morfdict(left, right, value)

    def set_morf(self, key, morf):
        """Set morf method for this key."""
        self._morf[key] = morf

    def del_morf(self, key):
        """Delete morf method for this key."""
        self._morf.pop(key)

    def get_morf(self, key):
        """Get morf method for this key."""
        return self._morf[key]

    def to_dict(self):
        """Create simple dict object from this object."""
        data = {}
        for key in list(self):
            value = self[key]
            if isinstance(value, MorfDict):
                value = value.to_dict()
            data[key] = value
        return data

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as error:
            if key == error.args[0] and default is not NoDefault:
                return default
            else:
                raise

    def items(self):
        for key in self.keys():
            try:
                yield (key, self[key])
            except KeyError:
                continue

    def merge(self, data):
        for key in data.keys():
            value = data._raw_get(key)
            if isinstance(value, MorfDict):
                if key in self:
                    self[key].merge(value)
                else:
                    self[key] = value
            else:
                self[key] = value
        self._parents += data._parents


class StringDict(MorfDict):
    """Class which tries to interpolate itself on morf."""

    def _default_morf(self, obj, value):
        if type(value) is str:
            return value % self
        else:
            return value


class Paths(object):

    def __init__(self):
        self.paths = dict()

    def get(self, name):
        """
        Get path by name.
        """
        element = self.paths[name]
        if type(element) is PathElement:
            if element.parent:
                parent = self.get(element.parent)
            else:
                parent = ''
            if element.is_root:
                parent = sep + parent
            return path.join(parent, *element.value)
        else:
            return element(self)

    def set(self, name, value, parent=None, is_root=False):
        """
        Set path.
            - name: normalized name of the path
            - value: filename, dirname or list or those
            - parent: normalized name of parent path
            - is_root: if true, this path will start with heading slash
        """
        if not isinstance(value, (list, tuple)):
            value = [value]
        self.paths[name] = PathElement(parent, value, is_root)

    def set_generator(self, name, generator):
        """
        Set path method generator.
            - name: normalized name of the path
            - generator: generation function which accepts this object as first
                argument
        """
        self.paths[name] = generator

    def to_dict(self):
        """
        Generates all paths into dict object.
        """
        data = dict()
        for name in self.paths:
            data[name] = self.get(name)
        return data

    def get_path_from_module(self, module):
        """
        Get path from module.
        """
        args = module.split(':')
        module = import_module(args[0])
        if args[1:]:
            dirpath = path.dirname(module.__file__)
            return path.join(dirpath, *args[1:])
        else:
            return module.__file__
