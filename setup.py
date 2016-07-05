#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError, err:
    from distutils.core import setup, find_packages
    
from talkback import VERSION

setup(
    name='Talkback',
    version='.'.join(map(str,VERSION)),
    description='A declarative framework for conversational interface applications.',
    packages=find_packages(),
    license='BSD',
    author='Loren Davie',
    author_email='code@axilent.com',
    url='http://github.com/Axilent/talkback',
    install_requires=[
        'Flask>=0.11.1',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'PyYAML>=3.11',
        'Werkzeug>=0.11.10',
        'click>=6.6',
        'itsdangerous>=0.24',
        'nltk>=3.2.1',
        'requests>=2.10.0',
        'textblob>=0.11.1',
        'wsgiref==0.1.2',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)