#! /usr/bin/python

import sys

sys.path.insert(0, '/var/www/smart-home')
# sys.path.append("/var/www/smart-home")


# The app directory contains __init__.py so it is a package
from app import app as application

