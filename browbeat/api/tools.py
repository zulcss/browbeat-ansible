#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import shutil
import sys
import tempfile

import ansible_runner
import six

from browbeat.api import logger

import pathlib

LOG = logger.LOG

WORKSPACE_DIR = ['results', 'logs']


class Tools(object):
    def __init__(self, args):
        self.args = args

    def create_workspace(self, workdir, uuid):
        try:
            workdir = os.path.expanduser(workdir)
            for path in WORKSPACE_DIR:
                work_dir = os.path.join(workdir, uuid, path)
                p = pathlib.Path(work_dir)
                if not p.exists():
                    LOG.debug('Creating workspace: %s' % work_dir)
                    p.mkdir(parents=True)
            return workdir
        except Exception as ex:
            LOG.exception('Unable to create workspace: {}'.format(
                ex.message))
            sys.exit(1)
    
    def _encode_envvars(self, env):
        for key, value in env.items():
            env[key] = six.text_type(value)
        else:
            return env
        
    def run_ansible_playbook(self, playbook, inventory, extra_vars=None,
        ssh_user='stack', output_callback='yaml', quiet=True):
        private_data_dir = tempfile.mkdtemp()
        try:
            extravars = {
                'ansible_ssh_extra_args': (
                '-o UserKnownHostsFile={} '
                '-o StrictHostKeyChecking=no '
                '-o ControlMaster=auto '
                '-o ControlPersist=30m '
                '-o ServerAliveInterval=64 '
                '-o ServerAliveCountMax=1024 '
                '-o Compression=no '
                '-o TCPKeepAlive=yes '
                '-o VerifyHostKeyDNS=no ' 
                '-o ForwardX11=no '
                '-o ForwardAgent=yes '
                '-o PreferredAuthentications=publickey '
                '-T').format(os.devnull)
            }
            if extra_vars:
                if isinstance(extra_vars, dict):
                    extravars.update(extra_vars)

            env = os.environ.copy()
            env['ANSIBLE_DISPLAY_FAILED_STDERR'] = True
            env['ANSIBLE_FORKS'] = 36
            env['ANSIBLE_TIMEOUT'] = 30
            env['ANSIBLE_GATHER_TIMEOUT'] = 45
            env['ANSIBLE_SSH_RETRIES'] = 3
            env['ANSIBLE_PIPELINING'] = True
            env['ANSIBLE_REMOTE_USER'] = ssh_user
            env['ANSIBLE_STDOUT_CALLBACK'] = output_callback
            env['ANSIBLE_CALLBACK_WHITELIST'] = 'profile_tasks,validation_output'
            env['ANSIBLE_RETRY_FILES_ENABLED'] = False
            env['ANSIBLE_HOST_KEY_CHECKING'] = False

            env['ANSIBLE_ROLES_PATH'] = os.path.expanduser(
                '~/.ansible/roles:'
                '/usr/share/browbeat/ansible:'
                '/usr/share/ansible/roles:'
                '/etc/ansible/roles:'
                '{}/roles'.format(
                    ansible_path)
            )

            if self.args.verbose:
                quiet = False
     
            params = {
                'private_data_dir': private_data_dir,
                'inventory': inventory,
                'playbook': playbook,
                'envvars': self._encode_envvars(env=env),
                'extravars': extravars,
                'quiet': quiet
            } 
            result = ansible_runner.run(**params)
            if result.status == 'failed' or \
                    (result.stats and result.stats.get('failures', [])):
                LOG.error('Failed to run: %s' % playbook)
            else:
                LOG.info(
                    'Ansible execution success. playbook: {}'.format(
                playbook))

        finally:
            shutil.rmtree(private_data_dir)

