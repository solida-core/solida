from ..cache_manager import CacheManager

help_doc = """
Do a local cache refresh of the pipelines
"""


def make_parser(parser):
    parser.add_argument('--ask',
                        dest='ask',
                        action='store_true',
                        help="Ask before to trigger the pipeline's refresh")
    pass


def implementation(logger, args):

    # Copy git repos into cache
    chm = CacheManager(args=args)
    chm.updates()


def do_register(registration_list):
    registration_list.append(('refresh', help_doc, make_parser, implementation))
