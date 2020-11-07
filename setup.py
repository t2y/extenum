import os
import re
import sys

from setuptools import setup


long_description = ''
this_directory = os.path.abspath(os.path.dirname(__file__))
for md in ('README.md', 'CHANGELOG.md'):
    with open(os.path.join(this_directory, md), encoding='utf-8') as f:
        long_description += f.read()

init_py = open('extenum/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))

setup(
    name='extenum',
    version=metadata['version'],
    description='Extended Enum classes for the Python 3 enum module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['enum'],
    author='Tetsuya Morimoto',
    author_email='tetsuya.morimoto@gmail.com ',
    url='https://github.com/t2y/extenum',
    license='Apache License 2.0',
    platforms=['unix', 'linux', 'osx', 'windows'],
    packages=['extenum'],
    include_package_data=True,
    install_requires=[],
    tests_require=['tox', 'pytest', 'pytest-flake8'],
)
