# -*- coding: utf-8; -*-
#
# Copyright (c) 2020 - 2021 Dr. Krusche & Partner PartG. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# @author Stefan Krusche, Dr. Krusche & Partner PartG
#

from setuptools import setup, find_packages

setup(
    name="sqlalchemy-ignite",
    version="0.5.0",
    license="Apache License Version 2.0",
    url="https://github.com/predictiveworks/sqlalchemy-ignite/",
    author="Dr. Stefan Krusche",
    author_email="krusche@dr-kruscheundpartner.de",
    description="SQLAlchemy dialect for Apache Ignite",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        "pyignite>=0.5.2",
        "sqlalchemy>=1.2.0"
    ],
    extras_require={
        "test": [
            "pytest>=2.5.2",
            "mock>=1.0.1"
        ]
    },
    classifiers=[  # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: SQL",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "sqlalchemy.dialects": [
            "igniteworks = igniteworks.sqlalchemy.dialect:IgniteDialect"
        ]
    },
)
