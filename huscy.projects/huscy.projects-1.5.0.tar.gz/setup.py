from os import path

from setuptools import find_namespace_packages, setup

from huscy.projects import __version__


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='huscy.projects',
    version=__version__,
    license='AGPLv3+',

    author='Mathias Goldau, Stefan Bunde',
    author_email='goldau@cbs.mpg.de, stefanbunde+git@posteo.de',

    description='Managing projects in a research context.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://bitbucket.org/huscy/projects/',

    packages=find_namespace_packages(include=['huscy.*']),

    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.11',
        'django-guardian>=2.0',
        'django-reversion>=3',
        'drf-nested-routers>=0.90',
    ],
    extras_require={
        'development': ['psycopg2-binary'],
        'testing': [
            'tox',
            'watchdog==0.9',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
    ],
)
