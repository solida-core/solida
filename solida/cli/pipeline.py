import os
import yaml

from ..cli.profiles import PROFILES_PATH
from ..pipelines_manager import PipelinesManager
from ..utils import path_exists, ensure_dir

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
    parser.add_argument('-i', '--install',
                        dest='install',
                        action='store_true',
                        help="Trigger the pipeline's deployment")
    parser.add_argument('--host',
                        dest='host',
                        type=str,
                        help='Hostname to install pipeline into',
                        default='localhost')
    parser.add_argument('--profile',
                        dest='profile',
                        type=str,
                        help='Profile file',
                        default=None)
    parser.add_argument('--path',
                        dest='path',
                        type=str,
                        help='Local path to install pipeline into')


def implementation(logger, args):
    plm = PipelinesManager(args, logger)
    pl = plm.get_pipeline(args.label)

    profiles_path = PROFILES_PATH
    ensure_dir(profiles_path)

    if args.install:
        if args.profile:
            profile_path = os.path.join(profiles_path, args.profile)
            with open(profile_path, 'r') as yaml_file:
                profile = yaml.load(yaml_file)
            host = args.host
            if args.path and path_exists(args.path, logger, force=False):
                profile['project_dir'] = args.path

            pl.instantiate(host, profile)
        else:
            logger.error('Need to indicate a profile.')


def do_register(registration_list):
    registration_list.append(('pipeline', help_doc, make_parser,
                              implementation))
