import argparse
import os

from importlib import import_module

from .utils import a_logger, LOG_LEVELS
import solida.__version__

here = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(here, "config/config.yaml")
SUBMOD_NAMES = [
    "solida.cli.list",
    "solida.cli.pipeline"
]
SUBMODULES = [import_module(n) for n in SUBMOD_NAMES]


class App(object):
    def __init__(self):
        self.supported_submodules = []
        for m in SUBMODULES:
            m.do_register(self.supported_submodules)

    def make_parser(self):
        example_text = '''example:

         solida list'''
        parser = argparse.ArgumentParser(prog='solida',
                                         description='NGS pipelines bootstrapper',
                                         epilog=example_text,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--config_file', type=str, metavar='PATH',
                            help='configuration file', default=CONFIG_FILE)
        parser.add_argument('--logfile', type=str, metavar='PATH',
                            help='log file (default=stderr).')
        parser.add_argument('--loglevel', type=str, help='logger level.',
                            choices=LOG_LEVELS, default='INFO')
        parser.add_argument('-v', '--version', action='version',
                            version='%(prog)s {}'.format(solida.__version__))

        subparsers = parser.add_subparsers(dest='subparser_name',
                                           title='subcommands',
                                           description='valid subcommands',
                                           help='sub-command description')

        for k, h, addarg, impl in self.supported_submodules:
            subparser = subparsers.add_parser(k, help=h)
            addarg(subparser)
            subparser.set_defaults(func=impl)

        return parser


def main():
    app = App()
    parser = app.make_parser()
    args = parser.parse_args()
    logger = a_logger('Solida', level=args.loglevel, filename=args.logfile)

    args.func(logger, args) if hasattr(args, 'func') else parser.print_help()


if __name__ == '__main__':
    main()
