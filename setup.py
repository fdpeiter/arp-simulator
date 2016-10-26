# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='arp-simulator',
    version='0.0.1',
    description='Simple simulator for arp requests',
    long_description=readme,
    author='Felipe Peiter',
    author_email='Felipe Peiter',
    url='https://github.com/fdpeiter/arp-simulator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

