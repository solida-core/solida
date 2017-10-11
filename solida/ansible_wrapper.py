import os.path
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleWrapper(object):
    """

    """
    def __init__(self, host, prj_path, prj_name, prj_email, pl, cconf,
                 playbooks_path='playbooks'):
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

        playbook_list = [os.path.join(playbooks_path, pl.playbook)]

        extra_vars = {'miniconda_dir': '/tmp',
                      'project_dir': prj_path,
                      'pipeline_url': pl.url,
                      'pipeline_label': pl.label}

        if prj_name != '':
            extra_vars['project_name'] = prj_name
        if prj_email != '':
            extra_vars['project_email_address'] = prj_email
        if cconf:
            extra_vars['cluster_setup'] = cconf['setup']
            if cconf['setup']:
                extra_vars['default_host_group'] = cconf['default_host_group']

        variable_manager.extra_vars = extra_vars

        self.pbex = PlaybookExecutor(playbooks=playbook_list,
                                     inventory=inventory,
                                     variable_manager=variable_manager,
                                     loader=loader,
                                     options=options,
                                     passwords=passwords)

    def run(self):
        return self.pbex.run()
