#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is at http://slack-admin.rtfd.org."""

setup(
    name='slack-admin',
    version='0.1.0',
    description='Slack Admin CLI',
    long_description=readme + '\n\n' + doclink,
    author='Evgeny Demchenko',
    author_email='little_pea@list.ru',
    url='https://github.com/littlepea/slack-admin',
    packages=[
        'slack_admin',
    ],
    package_dir={'slack_admin': 'slack_admin'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='slack-admin',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points='''
        [console_scripts]
        slack-admin=slack_admin.main:cli
    ''',
)
