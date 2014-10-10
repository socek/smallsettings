import os


class MorfDict(dict):

    def __init__(self, data={}, morf=None):
        super(MorfDict, self).__init__()
        self._morf = morf or {}

        for name, value in data.items():
            self[name] = value

    def __getitem__(self, key):
        value = super(MorfDict, self).__getitem__(key)
        method = self._morf.get(key, self._default_morf)
        return method(self, value)

    def _default_morf(self, obj, value):
        return value

    def __setitem__(self, key, value):
        if type(value) is dict:
            value = self.__class__(value)
        return super(MorfDict, self).__setitem__(key, value)

    def set_morf(self, key, morf):
        self._morf[key] = morf

    def del_morf(self, key):
        self._morf.pop(key)

    def get_morf(self, key):
        return self._morf[key]


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
