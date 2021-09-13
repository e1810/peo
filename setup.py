#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="peo",
    version="0.0",
    description="Python Extensions for objdump",
    url="https://github.com/d4wnin9/peo/",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "peo=peo.core:main",
        ],
    },
)