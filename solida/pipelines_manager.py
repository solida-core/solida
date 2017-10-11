import os
import sys
import yaml
from collections import namedtuple

import pygit2

from ansible_wrapper import AnsibleWrapper
from utils import path_exists


class PipelinesManager(object):
    """

    """
    def __init__(self, args=None, logger=None):
        def __load_config(cf):
            conf = dict()
            if os.path.isfile(cf):
                with open(cf) as cfg:
                    conf = yaml.load(cfg)
            return conf

        self.logger = logger
        if args and path_exists(args.config_file, logger):
            c = __load_config(args.config_file)
            self.conf = c['pipelines'] if 'pipelines' in c else None
            self.cluster_conf = c['cluster'] if 'cluster' in c else None

    def __exist(self, label):
        return label in self.conf

    def pipeline_exist(self, label):
        return self.__exist(label)

    def show_pipelines(self):
        for p in list(self.conf.keys()):
            self.show_pipeline(self.conf[p])

    @staticmethod
    def show_pipeline(label):
        pl = Pipeline(label)
        print("{} - {}".format(pl.label, pl.description))

    def get_pipeline(self, label):
        pipeline = None
        if self.__exist(label):
            pipeline = Pipeline(self.conf[label], self.logger)
        else:
            self.logger.error("Pipeline {} not found".format(label))
        return pipeline

    @property
    def get_cluster_config(self):
        return self.cluster_conf


class Pipeline(object):
    def __init__(self, conf, logger=None):
        self._label = conf['label']
        self._description = conf['description']
        self._url = conf['url']
        self._type = conf['type']
        self._playbook = conf['playbook']
        self.logger = logger

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def type(self):
        return self._type

    @property
    def playbook(self):
        return self._playbook

    @property
    def conf(self):
        MyConf = namedtuple('Configuration',
                            'label, description, url, type, playbook')
        return MyConf(label=self.label, description=self.description,
                      url=self.url, type=self.type, playbook=self.playbook)

    def get_source(self, path):
        """
        Retrieve pipeline's source code
        :param path: destination path
        :return: True if succeed, otherwise False
        """
        if self.type == 'git':
            try:
                pygit2.clone_repository(self.url, path)
            except pygit2.GitError as e:
                sys.exit(e)
            return True
        return False

    def instantiate(self,  host, path, project, email, cconf):
        self.logger.info("Instantiating {0} into {1}/{2}".format(self.label,
                                                                 path, project))
        aw = AnsibleWrapper(host, path, project, email, self.conf, cconf)
        aw.run()


help_doc = """
Pipelines manager
"""


def make_parser(parser):
    parser.add_argument('--list',
                        dest='list_pipelines',
                        action='store_true',
                        help='Show pipelines list')


def implementation(logger, args):
    pm = PipelinesManager(args, logger)
    if args.list_pipelines:
        pm.show_pipelines()


def do_register(registration_list):
    registration_list.append(('pm', help_doc, make_parser, implementation))
