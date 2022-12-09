# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup


version = '1.0.0'


setup(
    name='xlsext',
    version=version,
    keywords='Excel Extensions',
    description='Excel Extensions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    url='https://github.com/Brightcells/xlsext',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['xlsext'],
    py_modules=[],
    install_requires=['xlwt'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
