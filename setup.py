#! /usr/bin/env python
#coding=utf-8

from os.path import dirname, join
from setuptools import setup

with open(join(dirname(__file__), 'dig/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='dig',
    version=version,
    author='Gogary',
    author_email='gugugujiawei@gmail.com',

    url='https://pypi.python.org/pypi/dig',
    license='MIT',
    description='command-line front end of google translation serve.',
    long_description=open('README.rst').read(),

    # install_requires=['docopt==0.6.1', 'google_translate_api>=0.3'],
    packages=['dig'],

    entry_points={
        'console_scripts': [
            'dig = dig.cmdline:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
