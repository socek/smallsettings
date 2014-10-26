===============
1. Introduction
===============

1.1 What MorfDict is design for?
================================

MorfDict is base class which provide morfing of data. StringDict and PathDict is
design for making multi level settings. For example, you want settings in 3
files:

- app.py
    Not editable application settings like name of the application.
- defaul.py
    Default settings, like url for db or number of server threads.
- local.py
    Settings which always will be overrided. This file is not commited to the
    repository.

This can be achived with the StringDict and PathDict classes. If you have for
example url for db in form like sqlalchemy, you can set it like this:

::

    >> settings['url'] = '%(type)s://%(login)s:%(password)s@%(host)s:%(port)s/%(name)s'
    >> settings['type'] = 'postgresql'
    >> settings['login'] = 'db'
    >> settings['password'] = 'db'
    >> settings['host'] = 'localhost'
    >> settings['port'] = 'port'
    >> settings['name'] = 'name'

Now you can change the name of the db after this lines, so there is no need to
make the whole url now. The Factory class is design to provide loader for such
settings file configuration.

1.2 Install
===========

MorfDict package is in pypi, so you can just type this:

::

    >> (sudo) pip install morfdict

1.3 Source
==========

https://github.com/socek/smallsettings

::

    >> git clone https://github.com/socek/smallsettings.git
