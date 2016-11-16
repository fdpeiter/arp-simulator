# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='net-simulator',
    version='0.0.1',
    description='Simple simulator for Echo and ARP requests',
    long_description=readme,
    author='Felipe Peiter',
    author_email='Felipe Peiter',
    url='https://github.com/fdpeiter/simple-net-simulator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

