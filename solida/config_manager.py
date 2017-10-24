import os
import yaml

from .utils import path_exists


class ConfigurationManager(object):
    def __init__(self, args=None, logger=None):
        def __load_config(cf):
            conf = dict()
            if os.path.isfile(cf):
                with open(cf) as cfg:
                    conf = yaml.load(cfg)
            return conf

        if args and path_exists(args.config_file, logger):
            c = __load_config(args.config_file)
            self.pipes_conf = c['pipelines'] if 'pipelines' in c else None

    @property
    def get_pipelines_config(self):
        return self.pipes_conf

    def get_pipeline_config(self, label):
        return self.pipes_conf[label] if label in self.pipes_conf else None
