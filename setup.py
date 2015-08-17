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
 
    url='https://github.com/enjoyhot/dig',
    license='BSD',
    description='Command-line tool of [ google, youdao ] translation service.',
    long_description=open('README.rst').read(),

    
    install_requires=['docopt==0.6.2','futures>=3.0.3','requests==2.7.0'],
    packages=['dig'],


    data_files=[('dig', ['dig/VERSION', 'dig/mpg123.exe'])],


    entry_points={
        'console_scripts': [
            'dig = dig.cmdline:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop ',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

print("======================")
print("######################")
print("# dig version: " + version + " #")
print("######################")