#!/usr/bin/env python

import sys
from setuptools import find_packages, setup

if sys.version_info < (3, 9, 0):
    raise Exception("This project is incompatible with Python < 3.9.")

setup(
    name="pydroptidy",
    version="0.0.1",
    description="Tidy a Dropbox Camera Uploads folder",
    author="Max Manders",
    author_email="max@maxmanders.co.uk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "dropbox",
    ],
    entry_points='''
         [console_scripts]
         pydroptidy=pydroptidy.cli:run
     ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ]
)

