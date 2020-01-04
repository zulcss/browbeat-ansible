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

import copy
import datetime
import uuid

from stevedore import driver

from browbeat.api import config
from browbeat.api import logger
from browbeat.api import tools

LOG = logger.LOG


class Browbeat(object):
    def __init__(self, args):
        self.args = args
        self.result_dir_ts = datetime.datetime.utcnow().strftime(
            "%Y%m%d-%H%M%S")
        self.config = config.load_browbeat_config(self.args.config)
        self.tools = tools.Tools(self.args.config)

        self.workspace_dir = None

    def run(self):
        LOG.info('Running browbeat ...')

        browbeat_uuid = uuid.uuid4()
        self.workspace_dir = self.tools.create_workspace(
            self.config['browbeat']['workdir'], str(browbeat_uuid))
        LOG.info("Workbench test suite kicked off")
        LOG.info("Browbeat UUID: {}".format(browbeat_uuid))

        if self.config["browbeat"]["rerun_type"] == "iteration":
            self._run_iteration()
        elif self.config["browbeat"]["rerun_type"] == "complete":
            self._run_complete()

    def _run_iteration(self):
        for workload in self.config["workloads"]:
            if not workload["enabled"]:
                LOG.info("{} workload {} disabled in browbeat config".format(
                    workload["type"], workload["name"]))
                continue
            LOG.info("{} workload {} is enabled".format(
                workload["type"], workload["name"]))
            self._run_workload(workload, 0)

    def _run_complete(self):
        for iteration in range(0, self.config["browbeat"]["rerun"]):
            for workload in self.config["workloads"]:
                if not workload["enabled"]:
                    LOG.info("{} workload {} disabled in browbeat config"
                             .format(workload["type"], workload["name"]))
                    continue
                LOG.info("{} workload {} is enabled".format(
                    workload["type"], workload["name"]))
                self._run_iteration(workload, iteration)

    def _run_workload(self, workload, run_iteration):
        mgr = driver.DriverManager(
            namespace='browbeat.workloads',
            name=workload["type"],
            invoke_on_load=True,
            invoke_args=(self.config, self.args, self.workspac_dir,
                         self.tools, self.result_dir_ts, ))
        mgr.driver.run_workload(copy.deepcopy(workload), self.result_dir_ts)
