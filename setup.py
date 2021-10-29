#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "slack_sdk", "yagmail", "gitpython", "paramiko", "pydrive"]

setup_requirements = ["pytest-runner", ]

test_requirements = ["pytest>=3", ]

setup(
    name="codebots",
    version="0.10.0",
    author="Francesco Ranaudo",
    author_email="ranaudo@arch.ethz.ch",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="collection of bots for tasks automation",
    entry_points={
        "console_scripts": [
            "codebots=codebots.cli:main",
            "slackbot=codebots.cli:slackbot",
            "telebot=codebots.cli:telebot",
            "emailbot=codebots.cli:emailbot",
            "sshbot=codebots.cli:sshbot",
            "deploybot=codebots.cli:deploybot",
            "latexbot=codebots.cli:latexbot",
            "drivebot=codebots.cli:drivebot",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="codebots",
    packages=["codebots"],
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/franaudo/codebots",
    zip_safe=False,
)
