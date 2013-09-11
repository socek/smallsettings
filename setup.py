# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='SmallSettings',
          version='0.2',
          author=['Dominik "Socek" Długajczy'],
          author_email=['msocek@gmail.com', ],
          test_suite='smallsettings.tests.get_all_test_suite',
          packages=find_packages(),
          )
