#!/usr/bin/env python

"""
Flask-Sockets
-------------

Elegant WebSockets for your Flask apps.
"""
from setuptools import setup


setup(
    name='Flask-Sockets',
    version='0.11',
    url='git+git://github.comk/klimuk/flask-sockets.git',
    license='See License',
    author='Kenneth Reitz, Kirill Klimuk',
    author_email='_@kennethreitz.com',
    description='Elegant WebSockets for your Flask apps.',
    long_description=__doc__,
    py_modules=['flask_sockets'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'werkzeug',
        'gevent',
        'gevent-websocket'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)