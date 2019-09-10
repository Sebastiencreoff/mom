#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


___version__ = '0.0.2'

setup(name='mom',
      version=___version__,
      description='Mongo Object Manager',
      url='https://github.com/Sebastiencreoff/mom',
      author='Sebastien Creoff',
      author_email='sebastien.creoff@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['setuptools',
                        'jsonschema',
                        'pymongo',
                        ],
      tests_require=[
          'mock',
          'pytest',
      ],
      )
