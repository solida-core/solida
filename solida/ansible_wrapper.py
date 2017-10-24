import os.path
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleWrapper(object):
    """

    """
    def __init__(self, host, pipeline, profile,
                 playbooks_path='playbooks'):
        def set_extra_vars(pipeline=None, profile=None):
            extra_vars = dict()
            if pipeline:
                extra_vars['pipeline_label'] = pipeline['label']
                extra_vars['pipeline_url'] = pipeline['url']
            if profile:
                for k, v in profile.items():
                    extra_vars[k] = v

            return extra_vars

        variable_manager = VariableManager()
        loader = DataLoader()

        Options = namedtuple('Options',
                             ['connection', 'forks', 'become', 'become_method',
                              'become_user', 'check', 'listhosts', 'listtasks',
                              'listtags', 'syntax', 'module_path'])
        options = Options(connection='local', forks=100, become=None,
                          become_method=None, become_user=None,
                          check=False, listhosts=False, listtasks=False,
                          listtags=False, syntax=False, module_path="")

        passwords = dict()

        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=[host])
        variable_manager.set_inventory(inventory)

        here = os.path.abspath(os.path.dirname(__file__))
        playbook_list = [os.path.join(here, playbooks_path,
                                      pipeline['playbook'])]

        variable_manager.extra_vars = set_extra_vars(pipeline=pipeline,
                                                     profile=profile)

        self.pbex = PlaybookExecutor(playbooks=playbook_list,
                                     inventory=inventory,
                                     variable_manager=variable_manager,
                                     loader=loader,
                                     options=options,
                                     passwords=passwords)

    def run(self):
        return self.pbex.run()
