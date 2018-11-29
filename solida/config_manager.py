import os

from comoda import a_logger, ensure_dir, path_exists
from comoda.yaml import load as load_config
from functools import total_ordering
from pkg_resources import resource_filename
from shutil import copyfile

from solida import __appname__, config_dir


@total_ordering
class WeightedPath:
    def __init__(self, path, weight):
        self.path = path
        self.weight = weight

    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.path,
                                  self.weight)

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight


class ConfigurationManager(object):
    def __init__(self, args=None,
                 path_from_cli=None,
                 path_from_package='config/config.yaml',
                 config_filename='config.yaml'):
        def copy_config_file_from_package(appname, src, dst):
            _from_package = resource_filename(appname, src)
            copyfile(_from_package, dst)

        self.loglevel = args.loglevel
        self.logfile = args.logfile
        logger = a_logger(self.__class__.__name__, level=self.loglevel,
                          filename=self.logfile)

        cfg_dir = os.path.join(config_dir)
        config_file_path = os.path.join(cfg_dir, config_filename)

        # Create configuration file from default if needed
        if not path_exists(cfg_dir, logger, force=False):
            logger.info('Creating config dir {}'.format(cfg_dir))
            ensure_dir(cfg_dir)
        if not path_exists(config_file_path, logger, force=False):
            logger.info('Copying default config file from {} package '
                        'resource'.format(__appname__))
            copy_config_file_from_package(__appname__, path_from_package,
                                          config_file_path)

        config_file_paths = []
        if path_from_cli and path_exists(path_from_cli, logger, force=False):
            config_file_paths.append(WeightedPath(path_from_cli, 0))
        if path_exists(config_file_path, logger, force=False):
            config_file_paths.append(WeightedPath(config_file_path, 1))

        logger.debug("config file paths: {}".format(config_file_paths))

        config_file_path = sorted(config_file_paths)[0].path
        logger.info('Reading configuration from {}'.format(config_file_path))

        c = load_config(config_file_path)
        self.pipes_conf = c['pipelines'] if 'pipelines' in c else None
        self.default_conf = c['default_vars'] if 'default_vars' in c else None

    @property
    def get_default_config(self):
        return self.default_conf

    @property
    def get_pipelines_config(self):
        return self.pipes_conf

    def get_pipeline_config(self, label):
        return self.pipes_conf[label] if label in self.pipes_conf else None
