# -*- coding: utf-8 -*-
"""
bugle
~~~~

yet another static site-generator

"""

from setuptools import setup

with open('requirements.txt') as f:
    libs = f.readlines()

packages = [
        'bugle'
]

setup(
    name='bugle-sites',
    version='0.0.4',
    url='https://github.com/yosemitebandit/bugle',
    license='MIT',
    author='Matt Ball',
    author_email='matt.ball.2@gmail.com',
    description='static sites from markdown and yaml',
    long_description=__doc__,
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    install_requires=libs,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
