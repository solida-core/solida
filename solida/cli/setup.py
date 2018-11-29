import os

from comoda import path_exists, ensure_dir
from comoda.yaml import dump, load
from solida import profile_dir
from solida.config_manager import ConfigurationManager
from solida.pipelines_manager import PipelinesManager

help_doc = """
Setup pipeline
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
                        help='Network name of the host where the '
                             'pipeline has to be installed',
                        default='localhost')
    parser.add_argument('--remote-user',
                        dest='remote_user',
                        type=str,
                        help='remote user')
    parser.add_argument('--connection',
                        dest='connection',
                        type=str,
                        help='connection', default='local')


def implementation(logger, args):
    def get_profile(profile_label, profile_path, logger_):
        file_path = os.path.join(profile_path, '{}.yaml'.format(profile_label))

        if path_exists(file_path, logger_, force=False):
            msg = "Profile found at {}".format(file_path)
            print(msg)
            logger.info(msg)
            profile = load(file_path)
            return profile
        logger.info("Profile not found at {}".format(file_path))
        return None

    def write_profile(default_config, pl_, profile_label, profile_path,
                      logger_):
        def merge_two_dicts(x, y):
            z = x.copy()  # start with x's keys and values
            z.update(y)  # modifies z with y's keys and values & returns None
            return z

        file_path = os.path.join(profile_path, '{}.yaml'.format(profile_label))
        if path_exists(file_path, logger_, force=False) and not args.force:
            msg = "{} profile already exists".format(file_path)
            print(msg)
            logger.error(msg)
            # sys.exit()
        else:
            to_dump = merge_two_dicts(default_config,
                                      pl_.playbook_vars_template(project_name=profile_label))
            dump(to_dump, file_path)
            logger.info("Created {} profile".format(file_path))
            print("Edit variables value into the {} file".format(file_path))
        return

    profile_label, ext = os.path.splitext(args.profile)
    profile_path = os.path.join(profile_dir, args.label)
    ensure_dir(profile_path)

    plm = PipelinesManager(args)
    pl = plm.get_pipeline(args.label)
    profile = get_profile(profile_label, profile_path, logger)

    path_from_cli = args.config_file if 'config_file' in vars(args) else None
    cm = ConfigurationManager(args=args, path_from_cli=path_from_cli)
    default_config = cm.get_default_config

    if args.create_profile and not args.deployment:
        write_profile(default_config, pl, profile_label, profile_path, logger)
        return

    if args.deployment and not args.create_profile:
        if profile:
            host = args.host
            remote_user = args.remote_user
            connection = args.connection
            pl.instantiate(host, remote_user, connection, profile)
            return
    if not profile:
        msg = 'Profile "{}" not found. Have you created it? \n' \
              'Digit "solida setup --help" for more details'.format(profile_label)
        print(msg)
        logger.error(msg)


def do_register(registration_list):
    registration_list.append(('setup', help_doc, make_parser,
                              implementation))
