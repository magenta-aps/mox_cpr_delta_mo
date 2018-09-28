# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mox_cpr_delta_mo",
    version = "0.0.1",
    author = "Jørgen Gårdsted Jørgensen, Heini Leander Ovason",
    author_email = "jgj@magenta-aps.dk",
    description = ("mox agent for subscribing for updates from danish cpr registry and updating mo with results"),
    license = "MPL",
    keywords = "cpr mo mora lora",
    url = "",
    packages=['mox_cpr_delta_mo'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MPL License",
    ],
    install_requires=[
        # see requirements.txt
        # https://caremad.io/posts/2013/07/setup-vs-requirement/
    ]
)
