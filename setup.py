#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from setuptools import find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'websocket-client',
]

setup(
    name='strategypy',
    version='0.2.1',
    description="A strategy game for Python bots with replaceable front ends",
    long_description=readme,
    author="Davide Ceretti",
    author_email='dav.ceretti@gmail.com',
    url='https://github.com/davide-ceretti/strategypy',
    packages=find_packages(),
    package_dir={'strategypy':
                 'strategypy'},
    include_package_data=True,
    entry_points={
        'console_scripts': ['strategypy=strategypy.cli:run'],
    },
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='strategypy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
