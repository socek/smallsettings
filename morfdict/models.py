import os


class MorfDict(dict):

    def __init__(self, data={}, morf=None):
        super(MorfDict, self).__init__()
        self._morf = morf or {}
        self._parents = []

        for name, value in data.items():
            self[name] = value

    def __getitem__(self, key):
        left, right = self.split_key(key)
        value = self._get_from_self_or_parent(left)
        if right:
            value = value[right]
        method = self._morf.get(key, self._default_morf)
        return method(self, value)

    def split_key(self, huge_key):
        try:
            left, right = huge_key.split(':', 1)
            return left, right
        except:
            return huge_key, None

    def _get_from_self_or_parent(self, key):
        for obj in [super(MorfDict, self)] + self._parents:
            try:
                return obj.__getitem__(key)
            except KeyError:
                continue
        raise KeyError(key)

    def append_parent(self, parent, key=None):
        self._parents.append(parent)
        if key:
            parent[key] = self

    def _default_morf(self, obj, value):
        return value

    def __setitem__(self, key, value):
        if type(value) is dict:
            value = self.__class__(value)
        if isinstance(value, MorfDict):
            value.append_parent(self)
        return super(MorfDict, self).__setitem__(key, value)

    def set_morf(self, key, morf):
        self._morf[key] = morf

    def del_morf(self, key):
        self._morf.pop(key)

    def get_morf(self, key):
        return self._morf[key]

    def to_dict(self):
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
            if key == error.args[0] and default:
                return default
            else:
                raise


class StringDict(MorfDict):

    def _default_morf(self, obj, value):
        if type(value) is str:
            return value % self
        else:
            return value


class PathDict(StringDict):

    def _default_morf(self, obj, values):
        if type(values) in (list, tuple):
            parsed_values = []
            for value in values:
                parsed_values.append(
                    value % self
                )
            return os.path.join(*parsed_values)
        else:
            return values

    def __setitem__(self, key, value):
        if type(value) is str:
            value = [value, ]
        return super(PathDict, self).__setitem__(key, value)

    def set_path(self, name, dirname, basename):
        if type(basename) not in (list, tuple):
            basename = [basename]

        if dirname is None:
            self[name] = basename
        else:
            self[name] = ['%%(%s)s' % (dirname,)] + basename
