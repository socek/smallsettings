===========
2. Tutorial
===========

2.1 Using MorfDict
==================

MorfDict is a dict which converts data late on the fly.
Late changeing of values is called "morfing".

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




2.2 Using StringDict
====================

StringDict is MorfDict whith default interpolation for itself.

::

    >> from morfdict import StringDict
    >> data = StringDict()
    >> data['first'] = 'one'
    >> data['second'] = '%(first)s two'
    >> data['second']
    'one two'

2.3 Using Paths
===============

Paths is designed for storing paths.

::

    >> from morfdict import Paths
    >> paths = PathDict()
    >> paths.set('base', 'tmp', is_root=True)
    >> paths.set('myname', 'home', 'base')
    >> paths.get('home')
    '/tmp/home/myname'

Main purpose is to name all the paths that you use.

::

    >> paths.set(name='base', value='tmp')

Second feature is to make parenting. So if you change the parent path, the child
paths will change also.

::

    >> paths.set('base', 'tmp')
    >> paths.set('child', 'one', parent='base')
    >> assert paths.get('chilld') == 'tmp/one'
    >>
    >> paths.set('base', 'usr')
    >> assert paths.get('child') == 'usr/one'


2.4 Using Factory
=================
Factory can provide loader for settings. It helps in situation where you have
multi level settings, for example: default/application, then added local
settings. If we want to use ‘modulename.settings’ where ‘modulename’ is our
main module and ‘settings’ is our settins module.

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

2.5 Parrenting
==============

There is a possibility to make multi level morf dict interacting with each
other. Parrenting is hidden, so you can just make something like this:

::

    >> data = StringDict()
    >> data['parentvar'] = 'myvar'
    >> data['child'] = {'childvar': '%(parentvar)s child'}
    >> print(data['child:childvar'])
    myvar child

As you can see, you can use vars from parents whithin the childs. Using the
child from the parrent is achived by using ":", so you can not use this symbol
in key name, because it will brake. This is implemented so you can use
interpolation of the childs:

::

    >> data = StringDict()
    >> data['parentvar'] = 'myvar'
    >> data['child'] = {'childvar': '%(parentvar)s child'}
    >> data['second'] = '%(child:childvar)s parent'
    >> print(data['second'])
    myvar child parent

2.6 Casting to dict
===================

MorfDict stores data like normal dict. So this will probebly will not make
expected results:

::

    >> data = StringDict()
    >> data['one'] = 'one'
    >> data['two'] = '%(one)s two'
    >> print(dict(data))
    {'one': 'one', 'two': '%(one)s two'}

But there is a method called .to_dict wich will make proper result.

::

    >> data = StringDict()
    >> data['one'] = 'one'
    >> data['two'] = '%(one)s two'
    >> print(data.to_dict())
    {'one': 'one', 'two': 'one two'}

The second method is made bacouse sometimes you can need a raw dict data.

2.7 Merging aka updateing
=========================

From the same reason as above .update will not work as exptected, so you should
use .merge method.

::

    >> one = StringDict()
    >> one['first'] = 'one'
    >> one['third'] = 'third from one'
    >> two = StringDict()
    >> two['second'] = '%(first)s second'
    >> two['third'] = 'third from two'
    >> two.merge(one)
    >> print(two['second'])
    one second
    >> print(two['third'])
    third from one
