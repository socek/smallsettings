# -*- encoding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__ == '__main__':
    setup(name='MorfDict',
          version='0.3',
          author='Dominik "Socek" Długajczy',
          author_email='msocek@gmail.com',
          test_suite='morfdict.tests.get_all_test_suite',
          packages=find_packages(),
          package_data={'morfdict': ['README.md']},
          long_description=read('morfdict/README.md'),
          description="Simple settings functions for projects.",
          )
