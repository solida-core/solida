from appdirs import *

from solida.pipelines_manager import PipelinesManager
from comoda import path_exists, ensure_dir, is_tool_available
from comoda.yaml import dump, load

from solida.__details__ import __appname__

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
    def get_profile(profile_label, profile_path, logger_):
        file_path = os.path.join(profile_path, '{}.yaml'.format(profile_label))

        if path_exists(file_path, logger_, force=False):
            logger.info("{} profile found".format(file_path))
            profile = load(file_path)
            return profile
        logger.info("{} not found".format(file_path))
        return None

    def write_profile(pl_, profile_label, profile_path, logger_):
        file_path = os.path.join(profile_path, '{}.yaml'.format(profile_label))
        if path_exists(file_path, logger_, force=False) and not args.force:
            logger.error("{} profile already exists".format(file_path))
            # sys.exit()
        else:
            dump(pl_.playbook_vars_template(project_name=profile_label),
                 file_path)
            logger.info("Created {} profile".format(file_path))
            print("Edit variables value into the {} file".format(file_path))
        return

    profile_label, ext = os.path.splitext(args.profile)
    profile_path = os.path.join(user_data_dir(__appname__), args.label)
    ensure_dir(profile_path)

    plm = PipelinesManager(args)
    pl = plm.get_pipeline(args.label)
    profile = get_profile(profile_label, profile_path, logger)

    if args.create_profile and not args.deployment:
        write_profile(pl, profile_label, profile_path, logger)
        return

    if args.deployment and not args.create_profile:
        if not is_tool_available('conda'):
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
