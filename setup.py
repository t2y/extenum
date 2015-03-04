# -*- coding: utf-8 -*-
import re
import sys

from setuptools import setup


try:
    import pypandoc
    LONG_DESCRIPTION = '\n'.join([
        pypandoc.convert('README.md', 'rst'),
        pypandoc.convert('CHANGELOG.md', 'rst'),
    ])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

init_py = open('extenum/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))

REQUIRES = []
if sys.version_info < (3, 4):
    REQUIRES.append('enum34')


setup(
    name='extenum',
    version=metadata['version'],
    description='Extended Enum classes for the Python 3 enum module',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['enum'],
    author='Tetsuya Morimoto',
    author_email='tetsuya dot morimoto at gmail dot com',
    url='https://github.com/t2y/extenum',
    license='Apache License 2.0',
    platforms=['unix', 'linux', 'osx', 'windows'],
    packages=['extenum'],
    include_package_data=True,
    install_requires=REQUIRES,
    tests_require=['tox', 'pytest', 'pytest-pep8', 'pytest-flakes'],
)
