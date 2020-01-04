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

from browbeat.api import logger
from browbeat.api.path import ansible_path
from browbeat.workloads import base

LOG = logger.LOG


class Rally(base.WorkloadBase):
    def __init__(self, config, args, workdir, tools, result_dir_ts):
        self.args = args
        self.config = config
        self.tools = tools
        self.workdir = workdir
        self.result_dir_ts = result_dir_ts

        self.playbook = os.path.join(ansible_path, 'playbooks', 'rally-workload.yml')
    

    def run_workload(self, workload, run_iteration):
        LOG.info("Running Rally workload: {}".format(workload["name"]))
