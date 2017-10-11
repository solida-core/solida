import argparse
import sys

from importlib import import_module

from utils import a_logger, LOG_LEVELS

CONFIG_FILE = "config/config.yaml"
SUBMOD_NAMES = [
    "pipelines_manager",
    "pipelines"
]
SUBMODULES = [import_module(n) for n in SUBMOD_NAMES]


class App(object):
    def __init__(self):
        self.supported_submodules = []
        for m in SUBMODULES:
            m.do_register(self.supported_submodules)

    def make_parser(self):
        parser = argparse.ArgumentParser(prog='solida',
                                         description='NGS pipelines bootstrapper')
        parser.add_argument('--config_file', type=str, metavar='PATH',
                            help='configuration file', default=CONFIG_FILE)
        parser.add_argument('--logfile', type=str, metavar='PATH',
                            help='log file (default=stderr).')
        parser.add_argument('--loglevel', type=str, help='logger level.',
                            choices=LOG_LEVELS, default='INFO')

        subparsers = parser.add_subparsers(dest='subparser_name',
                                           title='subcommands',
                                           description='valid subcommands',
                                           help='sub-command description')

        for k, h, addarg, impl in self.supported_submodules:
            subparser = subparsers.add_parser(k, help=h)
            addarg(subparser)
            subparser.set_defaults(func=impl)

        return parser


def main(argv):
    app = App()
    parser = app.make_parser()
    args = parser.parse_args(argv)
    logger = a_logger('Solida', level=args.loglevel, filename=args.logfile)

    args.func(logger, args)


if __name__ == '__main__':
    main(sys.argv[1:])
