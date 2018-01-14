#!/usr/bin/env python
'''
Class using Ansible2 API for running different playbooks/tasks on remote servers
'''
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class AnsibleRunner(object):
  def __init__(self, host, user, key, module_path):
    self.host = host
    self.user = user
    self.key = key
    self.module_path = module_path

  def run(self, _tasks):
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'remote_user', 'remote_pass', 'private_key_file', 'no_log', 'ssh_common_args', 'sftp_extra_args', 'scp_extra_args', 'ssh_extra_args', 'become', 'become_method', 'become_user', 'check', 'verbosity'])
    # initialize needed objects
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(connection='smart', module_path=self.module_path, forks=10, remote_user=self.user, remote_pass=None, private_key_file=self.key, no_log=None, ssh_common_args=None, sftp_extra_args=None, scp_extra_args=None, ssh_extra_args=None, become=None, become_method=None, become_user=None, check=None, verbosity=None)

    # Instantiate our ResultsCollector for handling results as they come in
    results_callback = ResultsCollector()

    # create inventory and pass to var manager
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.host)
    variable_manager.set_inventory(inventory)

    # create play with tasks
    play_source =  dict(name = "play", hosts = self.host, gather_facts = 'no', tasks = _tasks)
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
      # actually run it
      tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=None,
              stdout_callback=results_callback,
            )
      tqm.run(play)
    finally:
      if tqm is not None:
        tqm.cleanup()

    return results_callback.get()


class ResultsCollector(CallbackBase):
  def __init__(self, *args, **kwargs):
    super(ResultsCollector, self).__init__(*args, **kwargs)
    self.hosts = []

  def v2_runner_on_unreachable(self, result, ignore_errors=False):
    self.hosts.append({'host':result._host.get_name(), 'result':None, 'success':False, 'msg':'unreachable'})

  def v2_runner_on_ok(self, result):
    self.hosts.append({'host':result._host.get_name(), 'result':result._result, 'success':True, 'msg':''})

  def v2_runner_on_failed(self, result, ignore_errors=False):
    self.hosts.append({'host':result._host.get_name(), 'result':result._result, 'success':False, 'msg':'failed'})

  def get(self):
    return self.hosts