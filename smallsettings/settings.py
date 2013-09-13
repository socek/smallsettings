import os


class Settings(object):

    def __init__(self, data={}):
        self.data = data

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        value = self.data[key]
        if type(value) in (str, unicode):
            return value % self
        else:
            return value

    def __contains__(self, key):
        return key in self.data

    def merged(self, settings):
        return Merged([self, settings])


class Paths(Settings):

    def __init__(self, data={}):
        self.data = {}
        for name, value in data.items():
            self[name] = value

    def __getitem__(self, key):
        parsed_values = []
        for value in self.data[key]:
            parsed_values.append(
                value % self
            )
        return os.path.join(*parsed_values)

    def __setitem__(self, key, value):
        if type(value) not in (list, tuple):
            value = [value, ]
        self.data[key] = value

    def merged(self, settings):
        return Merged([self, settings])


class Merged(object):

    def __init__(self, settings_list):
        self.settings_list = settings_list

    def __getitem__(self, key):
        for settings in self.settings_list:
            if key in settings:
                return settings[key]
        raise KeyError(key)

    def __contains__(self, key):
        contains = False
        for settings in self.settings_list:
            contains |= key in settings
        return contains

    def merge(self, settings):
        self.settings_list.append(settings)
