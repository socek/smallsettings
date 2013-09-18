# -*- encoding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__ == '__main__':
    setup(name='SmallSettings',
          version='0.2',
          author='Dominik "Socek" Długajczy',
          author_email='msocek@gmail.com',
          test_suite='smallsettings.tests.get_all_test_suite',
          packages=find_packages(),
          long_description=read('README.md'),
          description = "Simple settings functions for projects.",
          )
