#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

NAME = 'pydoku'
VERSION = '0.0.1'
AUTHOR = 'Sid Chaubal'
AUTHOR_EMAIL = 's.p.chaubal@student.vu.nl'
DESCRIPTION = 'A Boolean Satisfiability Solver, that will make you smile'
KEYWORDS = 'sat solver boolean satisfiability propositional logic ai artificial intelligence'
PYTHON_VERSION = '>=3.7.0'
REQUIRED = ['docopt', 'termcolor']
EXCLUDE = ['tests', '*.tests', '*.tests.*', 'tests.*']
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
  with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
except FileNotFoundError:
  long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
  project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
  with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)
else:
  about['__version__'] = VERSION

# Where the magic happens:
setup(
  name = NAME,
  version = about['__version__'],
  description = DESCRIPTION,
  long_description = DESCRIPTION,
  long_description_content_type = 'text/markdown',
  author = AUTHOR,
  author_email = AUTHOR_EMAIL,
  python_requires = PYTHON_VERSION,
  packages = find_packages(exclude = EXCLUDE),
  py_modules = ['pydoku'],
  entry_points = {
    'console_scripts': ['SAT = pydoku.cli:interpret']
  },
  install_requires = REQUIRED,
  extras_require = EXTRAS,
  include_package_data = True,
  license = 'MIT',
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Artificial Intelligence'
  ]
)
