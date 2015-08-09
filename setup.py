#!/usr/bin/python3

# pylint:disable=C0103
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("Need setuptools to run this script. Please install setuptools.")
    sys.exit(1)

#------------------------------------------------------------------------------
# Metadata
#------------------------------------------------------------------------------
description = (
    "A nose plugin to generate good-looking HTML reports for tests."
)

classifiers = list(filter(lambda x: x.strip(), """
    Intended Audience :: Developers
    Topic :: Software Development :: Testing
""".splitlines()))

#------------------------------------------------------------------------------
# The main setup call
#------------------------------------------------------------------------------
setup(
    # Package data
    name="nose-html-report",
    version="0.1",
    packages=["nose_html_report"],
    install_requires=["Jinja2", "nose", "Pygments"],
    # Register the plugin
    entry_points={
        "nose.plugins.0.10": ["HtmlReport = nose_html_report:HtmlReport"]
    },
    package_data={
        "nose_html_report": ["html/*"]
    },
    # As we need to read Jinja templates
    zip_safe=False,
    # Metadata
    description=description,
    author="Pradyun S. Gedam",
    author_email="pradyunsg@gmail.com",
    url="https://github.com/pradyun/nose-html-report",
    classifiers=classifiers
)
