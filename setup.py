#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-kerberos-auth',
    version = ":versiontools:taiga_contrib_kerberos_auth:",
    description = "The Taiga plugin for kerberos authentication",
    long_description = "",
    keywords = 'taiga, kerberos, auth, plugin',
    author = 'dpasqualin',
    author_email = 'dpasqualin@gmail.com',
    url = 'https://github.com/dpasqualin/taiga-contrib-kerberos-auth',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'django >= 1.7',
        'kerberos >= 1.2.5'
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
