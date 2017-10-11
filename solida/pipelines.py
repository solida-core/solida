from tempfile import mkdtemp

from pipelines_manager import PipelinesManager

help_doc = """
Pipeline
"""


def make_parser(parser):
    parser.add_argument('--install',
                        dest='install_pipeline',
                        type=str,
                        help="Pipeline's label to install",
                        default=None,
                        required=True)
    parser.add_argument('--tmp_dir',
                        dest='tmp_dir',
                        type=str,
                        help="Directory where to clone the pipeline's repository",
                        default=mkdtemp())
    parser.add_argument('--host',
                        dest='host',
                        type=str,
                        help='Hostname to install pipeline into',
                        default='localhost')
    parser.add_argument('--project',
                        dest='project',
                        type=str,
                        help='Project directory',
                        default='noname_project')
    parser.add_argument('--path',
                        dest='path',
                        type=str,
                        help='Local path to install pipeline into',
                        default=mkdtemp())
    parser.add_argument('--email',
                        dest='email',
                        type=str,
                        help='A valid email address where notify execution events',
                        default='example@example')


def implementation(logger, args):
    pm = PipelinesManager(args, logger)
    pl = pm.get_pipeline(args.install_pipeline)
    if pl:
        logger.info("Retrieved pipeline {} information".format(pl.label))

        host = args.host
        project = args.project
        path = args.path
        email = args.email
        cconf = pm.get_cluster_config

        pl.instantiate(host, path, project, email, cconf)


def do_register(registration_list):
    registration_list.append(('pl', help_doc, make_parser, implementation))
