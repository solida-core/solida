import sys

#import pygit2

from .ansible_wrapper import AnsibleWrapper
from .config_manager import ConfigurationManager


class PipelinesManager(object):
    """

    """
    def __init__(self, args=None, logger=None):
        cm = ConfigurationManager(args=args, logger=logger)
        self.conf = cm.get_pipelines_config
        self.logger = logger

    def __exist(self, label):
        return label in self.conf

    def pipeline_exist(self, label):
        return self.__exist(label)

    def show_pipelines(self):
        for p in self.conf.keys():
            self.show_pipeline(p)

    def show_pipeline(self, label):
        pl = Pipeline(self.conf[label])
        print("  label: {} \n  description: {} \n".format(pl.label,
                                                            pl.description))

    def get_pipeline(self, label):
        if self.__exist(label):
            pipeline = Pipeline(self.conf[label], self.logger)
            print("Solida pipelines found:")
            self.show_pipeline(label)
            self.logger.info("Pipeline {} information retrieved".format(label))
            return pipeline
        else:
            msg = "Pipeline {} not found".format(label)
            self.logger.error(msg)



class Pipeline(object):
    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger

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

    @property
    def playbook_vars_template(self):
        return self.config['playbook_vars_template']

    @property
    def conf(self):
        myconf = {'label': self.label,
                  'url': self.url,
                  'playbook': self.playbook}
        return myconf

    def instantiate(self, host, profile):
        msg = "Instantiating {0} into {1}/{2}".format(self.label,
                                                      profile['project_dir'],
                                                      profile['project_name'])
        self.logger.info(msg)
        aw = AnsibleWrapper(host, self.conf, profile)
        aw.run()


