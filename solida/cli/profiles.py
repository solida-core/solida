import os
import sys
import yaml

from ..pipelines_manager import PipelinesManager
from ..utils import path_exists, ensure_dir

PROFILES_PATH = os.path.expanduser('~/solida_profiles')

help_doc = """
Manage playbook vars profiles
"""


def make_parser(parser):
    parser.add_argument('-l', '--label',
                        dest='label',
                        type=str,
                        help="Pipeline's label",
                        default=None)
    parser.add_argument('-p', '--profile',
                        dest='profile',
                        type=str,
                        help='Profile name',
                        default=None)
    parser.add_argument('-f', '--force',
                        dest='force',
                        action='store_true',
                        help="Force profile writing")


def implementation(logger, args):
    profiles_path = PROFILES_PATH
    ensure_dir(profiles_path)

    if args.label:
        pm = PipelinesManager(args, logger)
        pl = pm.get_pipeline(args.label)
        filename = '{}_default.yaml'.format(pl.label)
        if args.profile:
            filename = '{}.yaml'.format(args.profile)
        output = os.path.join(profiles_path, filename)
        if path_exists(output, logger, force=False) and not args.force:
            logger.error("{} profile already exists".format(filename))
            sys.exit()
        stream = open(output, 'w')
        yaml.dump(pl.playbook_vars_template, stream, default_flow_style=False)
        logger.info("Created {} profile".format(output))
        print("Edit variables value into the {} file".format(output))
        return

    list_profiles(profiles_path)


def list_profiles(profiles_path):
    print("In {} found:".format(profiles_path))
    for filename in os.listdir(profiles_path):
        print("  - {}".format(filename))


def do_register(registration_list):
    registration_list.append(('profiles', help_doc, make_parser,
                              implementation))
