MorfDict
========

MorfDict is a dict like object, which convers data late on the fly.

::

    >> from morfdict import MorfDict
    >> data = MorfDict()
    >> data['first'] = 'my data'
    >> data['first']
    'my data'
    >> data.set_morf('first', lambda obj, value: '*' + value + '*')
    >> data['first']
    '*my data*'

If you want to make your own default morf method, just ovveride
\_default\_morf method.

::

    >> class MyMorf(MorfDict):
    >>    def _default_morf(self, obj, value):
    >>        return '*' + value + '*'

StringDict class
================

StringDict is MorfDict whith default interpolation for itself.

::

    >> from morfdict import StringDict
    >> data = StringDict()
    >> data['first'] = 'one'
    >> data['second'] = '%(first)s two'
    >> data['second']
    'one two'

PathDict class
==============

PathDict is designed for storing paths.

::

    >> from morfdict import PathDict
    >> paths = PathDict({'base' : '/tmp'})
    >> paths['home'] = ['%(base)s', 'home', 'myname']
    >> paths['home']
    '/tmp/home/myname'

Or you can make this:

::

    >> from morfdict import PathDict
    >> paths = PathDict({'base' : '/tmp'})
    >> paths.set_path('main', 'base', 'home')
    >> paths.set_path('home', 'main', 'myname')
    >> paths['home']
    '/tmp/home/myname'

Factory class
=============

If we want to use ‘modulename.settings’ where ‘modulename’ is our main
module and ‘settings’ is our settins module.

::

    >> from morfdict import Factory
    >> factory = Factory('modulename', 'settings')
    >> settings, paths = factory.make_settings()

It will read the settings from modulename/settings/default.py. This file
should looks like this:

::

    >> def make_settings(settings, paths):
    >>     settings['name'] = 'value'

If we want to add some additional files for settings, like “local.py”,
we can do this:

::

    >> settings, paths = factory.make_settings(additional_modules=[('local', False)])

This is the default behavior. The bool means “raise error on missing
module”.
