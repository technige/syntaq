#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011-2012 Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
sys.path.insert(0, "src")
from syntaq import __author__ as syntaq_author
from syntaq import __license__ as syntaq_license
from syntaq import __package__ as syntaq_package
from syntaq import __version__ as syntaq_version
sys.path.pop(0)

from distutils.core import setup

setup(
    name=syntaq_package,
    version=syntaq_version,
    description="Lightweight markup language parser/compiler based on Creole",
    long_description="Syntaq is a lightweight markup language based on (and " \
                     "backward compatible with) Creole. The package comes " \
                     "with a Python/Jython module which allows compilation " \
                     "of markup to HTML.",
    author=syntaq_author,
    author_email="nigel@nigelsmall.com",
    url="http://nigelsmall.com/syntaq",
    scripts=[],
    package_dir={"": "src"},
    packages=["syntaq"],
    license=syntaq_license,
    classifiers=[]
)
