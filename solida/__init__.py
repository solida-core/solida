"""Command-line solution to facilitate the usage of Snakemake"""

import os

from appdirs import *

__all__ = ['__appname__', '__version__', 'cache_dir', 'config_dir',
           'profile_dir', 'log_file']

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(os.path.dirname(here),
                       'solida', 'APPNAME')) as version_file:
    __appname__ = version_file.read().strip()

with open(os.path.join(os.path.dirname(here),
                       'solida', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()


cache_dir = user_cache_dir(__appname__)
config_dir = user_config_dir(__appname__)
profile_dir = user_data_dir(__appname__)
log_file = user_log_dir(__appname__)