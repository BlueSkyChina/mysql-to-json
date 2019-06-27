#!/usr/bin/env python3

from setuptools import setup
from distutils.command.install import install as _install

setup(
    name = 'mysql-to-jsonline',
    version = '1.0.0',
    description = 'Connects to a MySQL database and exports selected data to JSON.one row of table to one line with json style',
    author = 'Seth Black',
    author_email = 'sblack@sethserver.com',
    url = 'https://github.com/BlueSkyChina/mysql-to-jsonline',
    packages = ['mysqljsonline'],
    keywords = ['mysql','json','database','db','export','export tool','export utility'],
    install_requires = [
        'mysqlclient'
    ],
    entry_points = {
        'console_scripts' : [
            'mysql-to-jsonline = mysqljson.__main__:main'
        ]
    },
    classifiers = [
        "Topic :: Database",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    long_description = """\
Connects to a MySQL database and exports selected data to JSON.

## Usage

mysql-to-jsonline [-h] [-d DATABASE] [-H HOSTNAME] [-P PORT] [-u USER] [-p]
                     [-e QUERY]

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        MySQL database name.
  -H HOSTNAME, --hostname HOSTNAME
                        MySQL host name.
  -P PORT, --port PORT  MySQL port number.
  -u USER, --user USER  MySQL username.
  -p, --password        Shh! It's a secret.
  -e QUERY, --query QUERY
                        Query to run.

## Examples

All examples simple select all table information from `information_schema` and save it to `tables.json`

### Simple

This assumes we have full access to the mysql database from localhost.

$> mysql-to-jsonline -e 'SELECT * FROM information_schema.tables' > tables.json

### Medium Complexity

This explicitly sets a user and asks for a password, while still connecting to localhost.

$> mysql-to-jsonline -d mysql -u seth -p -e 'SELECT * FROM information_schema.tables' > tables.json

### All The Things!

This explicitly sets every command line option available.

$> mysql-to-jsonline -h mydbserver.myhost.com -P 3306 -d mysql -u seth -p -e 'SELECT * FROM information_schema.tables' > tables.json
"""
)
