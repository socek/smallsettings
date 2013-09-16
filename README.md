SmallSettings
=============

In many projects (web applicatons in particular) there is a need of making a settings. For application we need a 3 types of settings.
* Application settings (for example: application name)
* Envoritment settings (for example: url to database)
* Dynamic settings (for example: what ads to we show today)

SmallSettings provides solusion for the first 2 types of settings (the third one should be stored in the database).
The second problem with settings is wrapping some settings. Sometimes you have to wrap var from app settings in envoritment settings, and sometime you have to do the oposit. SmallSettings has a solution for this.

Settings classes
========
First we look at the "Settings" class.

    >> from smallsettings import Settings
    >> settings = Settings({'base_settings': 1})
    >> settings['base_settings']
    1

Pretty normal dict. But it have a special features:

    >> settings['something'] = 'new settings %(base_settings)s'
    >> settings['something']
    'new settings 1'

We can now ovveride the 'base_settings':

    >> settings['base_settings'] = 2
    >> settings['something']
    'new settings 2'

Second, the "Paths" class.

    >> from smallsettings import Paths
    >> paths = Paths({'base' : '/tmp'})
    >> paths['base']
    '/tmp'
    >> paths['home'] = '/home'
    >> paths['home']
    '/home'

But using previous var is slite different, because the Paths class use os.path.join:

    >> paths['me'] = ['%(home)s', 'me']
    >> paths['me']
    '/home/me'

If we want to "merge" settings and paths, we co do this:

    >> merged = settings.merged(paths)
    >> merged['something']
    'new settings 2'
    >> merged['me']
    '/home/me'

Factory
=======
    >> from smallsettings import Factory
    >> factory = Factory('modulename')
    >> settings, paths = factory.make_settings()

