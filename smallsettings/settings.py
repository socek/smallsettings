import os


class Settings(object):

    def __init__(self, data={}):
        self.data = data

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key] % self


class Paths(Settings):

    def __getitem__(self, key):
        parsed_values = []
        for value in self.data[key]:
            parsed_values.append(
                value % self.data
            )
        return os.path.join(*parsed_values)

    def __setitem__(self, key, value):
        if type(value) not in (list, tuple):
            value = [value, ]
        self.data[key] = value


class Merged(object):

    def __init__(self, settings, paths):
        self.settings = settings
        self.paths = paths

    def __getitem__(self, key):
        if key in self.settings.data:
            return self.settings[key]
        elif key in self.paths.data:
            return self.paths[key]
        else:
            raise KeyError(key)
