"""Read details from files."""

import os


here = os.path.abspath(os.path.dirname(__file__))
__all__ = ['__appname__', '__version__']

with open(os.path.join(os.path.dirname(here), 'APPNAME')) as version_file:
    __appname__ = version_file.read().strip()

with open(os.path.join(os.path.dirname(here), 'VERSION')) as version_file:
    __version__ = version_file.read().strip()
