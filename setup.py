#
# Setup file for the project
#
#
"""Bclockchain app as a portable app"""

import sys
import os
import setuptools

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

You're actually using Python {}.{} but in order to run this project you need
 to have at least Python {}.{}.
Please upgrade your Python's version.
""".format(*(CURRENT_PYTHON + REQUIRED_PYTHON)))
    sys.exit(1)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

PACKAGES_REQUIRED = [
    'Django>=2.1.5',
    'web3==4.8.1',
    'eth_account==0.2.3',
    'requests>=2.20.0',
    'djangorestframework==3.9.1'
]

setuptools.setup(
    name='Nexus Blockchain',
    version='0.0.2',
    author='Chiheb Nexus',
    author_email='chihebnexus@gmail.com',
    description=(
        'A tiny implementation of the blockchain technology'
        ' meant for educational purposes and built'
        ' using Python, Django, VueJS and a RDBMS database'
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/Chiheb-Nexus/nexus_blockchain',
    packages=setuptools.find_packages(),
    install_requires=PACKAGES_REQUIRED,
    classifiers=(
        'Programming Language :: Python :: 3',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Licence :: GPLv3',
        'Operating System :: OS Independent'
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    )
)
