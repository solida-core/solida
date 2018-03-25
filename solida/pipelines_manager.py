from copy import deepcopy
from comoda import a_logger

from .ansible_wrapper import AnsibleWrapper
from .config_manager import ConfigurationManager


class PipelinesManager(object):
    """

    """
    def __init__(self, args=None):
        path_from_cli = args.config_file if args.config_file else None
        cm = ConfigurationManager(loglevel=args.loglevel,
                                  path_from_cli=path_from_cli)
        self.conf = cm.get_pipelines_config
        self.loglevel = args.loglevel
        self.logger = a_logger(self.__class__.__name__, level=self.loglevel)

    def __exist(self, label):
        return label in self.conf

    def pipeline_exist(self, label):
        return self.__exist(label)

    def show_pipelines(self):
        for p in self.conf.keys():
            self.show_pipeline(p)

    def show_pipeline(self, label):
        pl = Pipeline(self.conf[label], self.loglevel)
        print("  label: {} \n  description: {} \n".format(pl.label,
                                                          pl.description))

    def get_pipeline(self, label):
        if self.__exist(label):
            pipeline = Pipeline(self.conf[label], self.loglevel)
            print("Solida pipelines found:")
            self.show_pipeline(label)
            self.logger.info("Pipeline {} information retrieved".format(label))
            return pipeline
        else:
            msg = "Pipeline {} not found".format(label)
            self.logger.error(msg)


class Pipeline(object):
    def __init__(self, config, loglevel='INFO'):
        self.config = config
        self.logger = a_logger(self.__class__.__name__, level=loglevel)

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

    def instantiate(self, host, profile):
        msg = "Instantiating {0} into {1}/{2}".format(self.label,
                                                      profile['project_dir'],
                                                      profile['project_name'])
        self.logger.info(msg)
        aw = AnsibleWrapper(host, self.conf, profile)
        aw.run()
