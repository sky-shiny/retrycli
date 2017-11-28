#!/usr/bin/env python

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

PACKAGES = [
    'retrycli',
]

REQUIRES = [
    'argh == 0.26.1',
    'retrying == 1.3.3'
]

with open('README.md', 'r') as f:
    README = f.read()

with open('HISTORY', 'r') as f:
    HISTORY = f.read()

setup(
    name='retrycli',
    version='0.1.1',
    description='Retrying wrapper for the shell.',
    long_description=README + '\n\n' + HISTORY,
    author='Max Cameron',
    author_email='maxwell.cameron@johngaltsystems.com',
    url='http://github.com/sky-chiny/retrycli',
    packages=PACKAGES,
    package_data={
        '': ['LICENSE'],
    },
    scripts=['retry'],
    include_package_data=True,
    install_requires=REQUIRES,
    license='BSD License',
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ),
)
