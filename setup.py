#!/usr/bin/env python
# Fro Python
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='pyoffer',
      version='0.0.2',
      description='pyoffer tracks special offers on Internet',
      url='http://github.com/bijanebrahimi/pyoffer',
      author='Bijan Ebrahimi',
      author_email='bijanebrahimi@riseup.net',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['yapsy', 'pyquery', 'pyqt5'],
      test_suite='tests',
      entry_points="""
      [console_scripts]
      pyoffer-gui = pyoffer.run:main
      """,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      extras_require={
          'testing': ['pytest', 'setuptools']
      })
