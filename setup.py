#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the specification of the mmworkbench package"""
# pylint: disable=locally-disabled,invalid-name
from setuptools import setup

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'click-log==0.1.8',
    'elasticsearch>=5.1.0',
    'Flask>=0.12',
    'Flask-Cors>=3.0.2',
    'future>=0.16.0',
    'nltk==3.2.2',
    'numpy>=1.10.1',
    'py>=1.4.34',
    'python-dateutil>=2.6.0',
    'requests>=2.13.0',
    'scipy>=0.9',
    'scikit-learn>=0.18.1',
    'tqdm>=4.15.0',
    'urllib3<1.22,>=1.21.1',
    'python-crfsuite>=0.9.2',
    'sklearn-crfsuite>=0.3.6',
    'bleach=1.5.0',
    'tensorflow>=1.2.1'
]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'flake8==3.2.1',
    'pylint==1.6.5',
    'pytest==3.0.5',
    'pytest-cov==2.4.0',
]

setup(
    name='mmworkbench',
    version='3.0.0',
    description="A Python module for building natural language processing models.",
    long_description=history,
    author="MindMeld, Inc.",
    author_email='contact@mindmeld.com',
    url='https://github.com/mindmeld/mindmeld-workbench3',
    packages=[
        'mmworkbench',
    ],
    package_dir={'mmworkbench': 'mmworkbench'},
    entry_points={
        'console_scripts': ['mmworkbench=mmworkbench.cli:cli']
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='mindmeld',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements
)
