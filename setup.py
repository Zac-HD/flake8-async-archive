#!/usr/bin/env python3

from pathlib import Path

import setuptools


def local_file(name: str) -> Path:
    return Path(__file__).parent / name


with local_file("flake8_async.py").open("r") as o:
    for line in o:
        if line.startswith("__version__"):
            _, __version__, _ = line.split('"')


setuptools.setup(
    name="flake8-async",
    version=__version__,
    author="Cooper Lees and Zac Hatfield-Dodds",
    author_email="me@cooperlees.com",
    py_modules=["flake8_async"],
    url="https://github.com/cooperlees/flake8-async",
    license="MIT",
    description="A flake8 plugin that checks bad async / asyncio practices",
    zip_safe=False,
    install_requires=["flake8"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    long_description=(
        local_file("README.md").open().read()
        + "\n\n"
        + local_file("CHANGELOG.md").open().read()
    ),
    long_description_content_type="text/markdown",
    entry_points={
        "flake8.extension": ["ASY = flake8_async:Plugin"],
    },
)
