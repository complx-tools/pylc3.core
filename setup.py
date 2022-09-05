#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from skbuild import setup
from setuptools import find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pylc3.core',
    version='0.1.3',
    description="Python bindings for liblc3, the LC-3 simulator framework",
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Brandon Whitehead",
    author_email='brandon.whitehead@gatech.edu',
    url='https://github.com/complx-tools/pylc3.core',
    license="GNU General Public License v3",
    packages=find_packages(exclude=['tests', 'docs', 'scripts', 'cmake']),
)