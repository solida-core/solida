from solida import *
from ..pipelines_manager import PipelinesManager


help_doc = """
Show Solida details
"""


def make_parser(parser):
    pass


def implementation(logger, args):
    print("{} {}\n".format(__appname__.capitalize(), __version__))

    solida_path = {'cache dir': cache_dir,
                   'config dir': config_dir,
                   'profile dir': profile_dir,
                   'log file': log_file
                   }
    print("Paths: ")
    for k, v in solida_path.items():
        print("  {}: {}".format(k, v))
    print("\n")

    pm = PipelinesManager(args)
    pm.show_pipelines()


def do_register(registration_list):
    registration_list.append(('info', help_doc, make_parser, implementation))
