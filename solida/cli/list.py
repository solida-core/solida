from ..pipelines_manager import PipelinesManager


help_doc = """
Show pipelines list
"""


def make_parser(parser):
    pass


def implementation(logger, args):
    pm = PipelinesManager(args, logger)
    pm.show_pipelines()


def do_register(registration_list):
    registration_list.append(('list', help_doc, make_parser, implementation))
