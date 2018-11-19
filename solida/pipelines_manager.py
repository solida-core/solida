import os
import sys

from copy import deepcopy
from comoda import a_logger, is_tool_available
from git import Repo

from solida import cache_dir
from .ansible_wrapper import AnsibleWrapper
from .config_manager import ConfigurationManager


class PipelinesManager(object):
    """

    """
    def __init__(self, args=None):
        self.loglevel = args.loglevel
        self.logfile = args.logfile
        self.logger = a_logger(self.__class__.__name__, level=self.loglevel,
                               filename=self.logfile)
        path_from_cli = args.config_file if 'config_file' in vars(args) else None
        cm = ConfigurationManager(args=args, path_from_cli=path_from_cli)
        self.conf = cm.get_pipelines_config
        self.cache_dir = cache_dir

    def __exist(self, label):
        return label in self.conf

    def pipeline_exist(self, label):
        return self.__exist(label)

    def show_pipelines(self):
        print("Workflows available: ")
        for p in self.conf.keys():
            self.show_pipeline(p)

    def show_pipeline(self, label):
        pl = Pipeline(self.conf[label], loglevel=self.loglevel,
                      logfile=self.logfile)
        print("  label: {}".format(pl.label))
        print("  description: {}".format(pl.description))
        repo_dir = os.path.join(self.cache_dir, label)
        repo = Repo(repo_dir)
        heads = repo.heads
        master = heads.master
        print("  url: {}".format(pl.url))
        print("  commit id: {}".format(master.commit))
        print("  ")

    def get_pipeline(self, label):
        if self.__exist(label):
            pipeline = Pipeline(self.conf[label], loglevel=self.loglevel,
                                logfile=self.logfile)
            print("Pipeline found:")
            self.show_pipeline(label)
            self.logger.info("Pipeline {} information retrieved".format(label))
            return pipeline
        else:
            msg = "Pipeline {} not found".format(label)
            print(msg)
            self.logger.error(msg)


class Pipeline(object):
    def __init__(self, config, loglevel='INFO', logfile=sys.stdout):
        self.config = config
        self.logger = a_logger(self.__class__.__name__, level=loglevel,
                               filename=logfile)

    @property
    def conf(self):
        myconf = {'label': self.label,
                  'url': self.url,
                  'playbook': self.playbook}
        return myconf

    @property
    def label(self):
        return self.config['label']

    @property
    def description(self):
        return self.config['description']

    @property
    def url(self):
        return self.config['url']

    @property
    def type(self):
        return self.config['type']

    @property
    def playbook(self):
        return self.config['playbook']

    def playbook_vars_template(self, **kwargs):
        pvt = deepcopy(self.config['playbook_vars_template'])
        for kw in kwargs:
            if kw in pvt:
                pvt[kw] = kwargs[kw]
        return pvt

    def instantiate(self, host, remote_user, connection, profile):
        # TODO: tool availability check should run on remote host also
        # tool_label = 'conda'
        # if not is_tool_available(tool_label):
        #     msg = '{} not found at host {}. Install it from ' \
        #           'https://conda.io/miniconda.html'.format(tool_label.capitalize(), host)
        #     print(msg)
        #     self.logger.error(msg)
        #     return
        msg = "Instantiating {0} into {1}/{2}".format(self.label,
                                                      profile['project_dir'],
                                                      profile['project_name'])
        print(msg)
        self.logger.info(msg)
        aw = AnsibleWrapper(host, remote_user, connection, self.conf, profile)
        aw.run()
