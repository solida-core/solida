import os.path
from collections import namedtuple

from ansible import context
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager as Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from solida import cache_dir


class AnsibleWrapper(object):
    """

    """
    def __init__(self, host, remote_user, connection, pipeline, profile,
                 playbooks_path='playbooks'):
        def set_extra_vars(pipeline=None, profile=None):
            extra_vars = dict()
            if pipeline:
                extra_vars['pipeline_label'] = pipeline['label']
                extra_vars['pipeline_url'] = pipeline['url']
                extra_vars['pipeline_cache_path'] = os.path.join(cache_dir,
                                                                 pipeline['label'])
            if profile:
                for k, v in profile.items():
                    extra_vars[k] = v

            return extra_vars

        loader = DataLoader()

        options = ImmutableDict(connection=connection, forks=1000, remote_user=remote_user,
                                become=None, become_method=None, become_user=None,
                                diff=False, check=False, listhosts=False,
                                listtasks=False, listtags=False, syntax=False,
                                module_path="", start_at_task=None,  verbosity=100)

        passwords = dict()

        context.CLIARGS = options

        inventory = Inventory(loader=loader, sources="{},".format(host))
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        here = os.path.abspath(os.path.dirname(__file__))
        playbook_list = [os.path.join(here, playbooks_path,
                                      pipeline['playbook'])]

        extra_vars = set_extra_vars(pipeline=pipeline, profile=profile)
        variable_manager._extra_vars = extra_vars

        self.pbex = PlaybookExecutor(playbooks=playbook_list,
                                     inventory=inventory,
                                     variable_manager=variable_manager,
                                     loader=loader,
                                     passwords=passwords)

    def run(self):
        return self.pbex.run()
