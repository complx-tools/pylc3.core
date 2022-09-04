#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from skbuild import setup
from setuptools import find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pylc3.core',
    version='0.1.0',
    description="Python bindings for liblc3, the LC-3 simulator framework",
    long_description=readme,
    author="Brandon Whitehead",
    author_email='brandon.whitehead@gatech.edu',
    url='https://github.com/complx-tools/pylc3.core',
    license=license,
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
)
