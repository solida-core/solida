import os
import yaml

from ..cli.profiles import PROFILES_PATH
from ..pipelines_manager import PipelinesManager
from ..utils import path_exists, ensure_dir, is_tool

help_doc = """
Manage pipeline
"""


def make_parser(parser):
    parser.add_argument('-l', '--label',
                        dest='label',
                        type=str,
                        help="Pipeline's label",
                        default=None,
                        required=True)
    parser.add_argument('-p', '--profile',
                        dest='profile',
                        type=str,
                        help='Profile file label',
                        default='',
                        required=True)
    parser.add_argument('--deploy',
                        dest='deployment',
                        action='store_true',
                        help="Trigger the pipeline's deployment")
    parser.add_argument('--create-profile',
                        dest='create_profile',
                        action='store_true',
                        help="Trigger the profile's writing")
    parser.add_argument('-f', '--force',
                        dest='force',
                        action='store_true',
                        help="Force profile writing")
    parser.add_argument('--host',
                        dest='host',
                        type=str,
                        help='Hostname to install pipeline into',
                        default='localhost')
    parser.add_argument('--path',
                        dest='path',
                        type=str,
                        help='Local path to install pipeline into')


def implementation(logger, args):
    def get_profile(profile_label, logger_):
        ensure_dir(PROFILES_PATH)
        filename, file_extension = os.path.splitext(profile_label)
        profile_path = os.path.join(PROFILES_PATH, '{}.yaml'.format(filename))

        if path_exists(profile_path, logger_, force=False):
            logger.info("{} profile found".format(profile_path))
            with open(profile_path, 'r') as yaml_file:
                profile = yaml.load(yaml_file)
            return profile
        logger.info("{} not found".format(profile_path))
        return None

    def write_profile(pl_, profile_label, logger_):
        ensure_dir(PROFILES_PATH)
        filename, file_extension = os.path.splitext(profile_label)
        profile_path = os.path.join(PROFILES_PATH, '{}.yaml'.format(filename))
        if path_exists(profile_path, logger_, force=False) and not args.force:
            logger.error("{} profile already exists".format(profile_path))
            # sys.exit()
        else:
            stream = open(profile_path, 'w')
            yaml.dump(pl_.playbook_vars_template, stream,
                      default_flow_style=False)
            logger.info("Created {} profile".format(profile_path))
            print("Edit variables value into the {} file".format(profile_path))
        return

    plm = PipelinesManager(args, logger)
    pl = plm.get_pipeline(args.label)
    profile = get_profile(args.profile, logger)

    if args.create_profile and not args.deployment:
        write_profile(pl, args.profile, logger)
        return

    if args.deployment and not args.create_profile:
        if not is_tool('conda'):
            logger.error('Conda not found. Install it from '
                         'https://conda.io/miniconda.html')
            return
        if profile:
            host = args.host
            pl.instantiate(host, profile)
            return
        else:
            logger.error('Profile not found. Have you created it?.')


def do_register(registration_list):
    registration_list.append(('pipeline', help_doc, make_parser,
                              implementation))
