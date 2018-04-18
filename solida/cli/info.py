from ..__details__ import *
from ..pipelines_manager import PipelinesManager

from appdirs import *

help_doc = """
Show Solida details
"""


def make_parser(parser):
    pass


def implementation(logger, args):
    print("{} {}\n".format(__appname__.capitalize(), __version__))

    solida_path = {'cache dir': user_cache_dir(__appname__),
                   'config dir': user_config_dir(__appname__),
                   'profile dir': user_data_dir(__appname__),
                   'log file': user_log_dir(__appname__)
                   }
    print("Paths: ")
    for k, v in solida_path.items():
        print("  {}: {}".format(k, v))
    print("\n")

    pm = PipelinesManager(args)
    pm.show_pipelines()


def do_register(registration_list):
    registration_list.append(('info', help_doc, make_parser, implementation))
