class Settings(object):
    def __init__(self, main_modulepath, settings_modulepath='settings'):
        self.main_modulepath = main_modulepath
        self.settings_modulepath = settings_modulepath

    def import_module(self, modulename):
        modulepath = '.'.join([self.main_modulepath, self.settings_modulepath, modulename])
        return __import__(
            modulepath, globals(), locals(), ['']
        )

    def import_default(self, settings):
        module = self.import_module('default')
        return module.make_settings(settings)

    def import_local_without_errors(self, settings):
        try:
            module = self.import_module('local')
            return module.make_settings(settings)
        except ImportError:
            pass
        return settings

    def import_test(self, settings):
        module = self.import_module('tests')
        return module.make_settings(settings)

    def init_settings(self, settings):
        from os.path import dirname, abspath
        mainmodule = __import__(
            self.main_modulepath, globals(), locals(), ['']
        )
        settings['PROJECT_PATH'] = dirname(abspath(mainmodule.__file__))
        return settings

    def make_settings(self, settings={}, testrun=False):
        settings = self.init_settings(settings)
        settings = self.import_default(settings)
        if testrun:
            settings = self.import_test(settings)
        else:
            settings = self.import_local_without_errors(settings)
        return settings
