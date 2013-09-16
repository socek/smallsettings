from os.path import dirname, abspath

from settings import Settings, Paths


class Factory(object):

    def __init__(self, main_modulepath, settings_modulepath='settings'):
        self.main_modulepath = main_modulepath
        self.settings_modulepath = settings_modulepath

    def _import_wrapper(self, modulepath):
        return __import__(
            modulepath, globals(), locals(), ['']
        )

    def import_module(self, modulename):
        modulepath = '.'.join(
            [self.main_modulepath, self.settings_modulepath, modulename])
        return self._import_wrapper(modulepath)

    def run_module(self, name):
        module = self.import_module(name)
        module.make_settings(self.settings, self.paths)

    def run_module_without_errors(self, name):
        try:
            module = self.import_module(name)
            module.make_settings(self.settings, self.paths)
        except ImportError:
            pass

    def init_data(self, settings, paths):
        self.settings = Settings(settings)
        self.paths = Paths(paths)

        mainmodule = self._import_wrapper(self.main_modulepath)

        self.paths['project_path'] = dirname(abspath(mainmodule.__file__))

    def make_settings(self, settings={}, paths={}, additional_modules=(('local', False),)):
        self.init_data(settings, paths)

        self.run_module('default')

        for module_name, show_error in additional_modules:
            if show_error:
                self.run_module(module_name)
            else:
                self.run_module_without_errors(module_name)

        return self.settings, self.paths
