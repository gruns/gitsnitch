#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# GitSnitch - A simple tool that finds a GitHub user's email address(es)
#
# Ansgar Grunseid, with credit to Eric Migicovsky for his insight to use
#   the GitHub API over git itself
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

import os
import sys
from os.path import dirname, join as pjoin
from setuptools import setup, find_packages, Command

from gitsnitch.__version__ import __version__ as VERSION


class Publish(Command):
    """Publish to PyPI with twine."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('python3 setup.py sdist bdist_wheel')

        sdist = 'dist/gitsnitch-%s.tar.gz' % VERSION
        wheel = 'dist/gitsnitch-%s-py2.py3-none-any.whl' % VERSION
        rc = os.system('twine upload "%s" "%s"' % (sdist, wheel))

        sys.exit(rc)


setup(
    name='gitsnitch',
    license='MIT',
    version=VERSION,
    author='Ansgar Grunseid',
    author_email='grunseid@gmail.com',
    url='https://github.com/gruns/gitsnitch',
    description=(
        "A simple tool that finds a GitHub user's email address(es)"),
    long_description=(
        'Information and documentation can be found at '
        'https://github.com/gruns/gitsnitch.'),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': ['gitsnitch=gitsnitch.cli:cliEntry'],
    },
    install_requires=[
        'furl>=2.1.3',
        'docopt>=0.6.2',
        'requests>=2.7.0',
        'icecream>=2.1.3',
    ],
    cmdclass={
        'publish': Publish,
    },
)
