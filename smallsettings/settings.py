import os


class Settings(dict):

    def __init__(self, data={}):
        super(Settings, self).__init__(data)

    def __getitem__(self, key):
        value = super(Settings, self).__getitem__(key)
        if type(value) in (str, unicode):
            return value % self
        else:
            return value

    def merged(self, settings):
        """Gets Merged object of this object and another one."""
        return Merged([self, settings])


class Paths(Settings):

    def __init__(self, data={}):
        super(Paths, self).__init__()
        for name, value in data.items():
            self[name] = value

    def __getitem__(self, key):
        parsed_values = []
        for value in super(Paths, self).__getitem__(key):
            parsed_values.append(
                value % self
            )
        return os.path.join(*parsed_values)

    def __setitem__(self, key, value):
        if type(value) not in (list, tuple):
            value = [value, ]
        return super(Paths, self).__setitem__(key, value)

    def merged(self, settings):
        """Gets Merged object of this object and another one."""
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
        """Add another Settings or Paths object to the list."""
        self.settings_list.append(settings)
