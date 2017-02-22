from os.path import abspath
from os.path import dirname

from morfdict.models import Paths
from morfdict.models import StringDict


class Factory(object):
    """Loader for settings files."""

    def __init__(self, main_modulepath, settings_modulepath='settings'):
        """
        :param main_modulepath: import path to a main module
        :param settings_modulepath: import path to a settings module within
            main module
        """
        self.main_modulepath = main_modulepath
        self.settings_modulepath = settings_modulepath

    def _import_wrapper(self, modulepath):
        return __import__(
            modulepath, globals(), locals(), ['']
        )

    def import_module(self, modulename):
        """Import module from settings module."""
        modulepath = '.'.join(
            [self.main_modulepath, self.settings_modulepath, modulename])
        return self._import_wrapper(modulepath)

    def run_module(self, name):
        """Import settings from a module. Raise ImportError on missing module.
        """
        module = self.import_module(name)
        module.make_settings(self.settings, self.paths)

    def run_module_without_errors(self, name):
        """Import settings from a module. Do not raise ImportError on missing
        module."""
        try:
            module = self.import_module(name)
            module.make_settings(self.settings, self.paths)
        except ImportError:
            pass

    def init_data(self, settings):
        """Initialize settings with data. Add 'module_root' to paths
        depending on main module.
        """
        self.settings = StringDict(settings)
        self.paths = Paths()

        mainmodule = self._import_wrapper(self.main_modulepath)

        self.paths.set('module_root', dirname(abspath(mainmodule.__file__)))

    def make_settings(self, settings={}, paths={}, additional_modules=None):
        """Make StringDict and PathDict from modules.

        :param settings: default settings
        :param paths: default paths
        :param additional_modules: list of tuples of additional modules. First
        :param element: in tuple is a module name, second is bool. If setted to
            true,
        :param method: will raise ImportError on missing module.
        """
        additional_modules = additional_modules or (('local', False),)
        self.init_data(settings, paths)

        self.run_module('default')

        for module_name, show_error in additional_modules:
            if show_error:
                self.run_module(module_name)
            else:
                self.run_module_without_errors(module_name)

        return self.settings, self.paths
