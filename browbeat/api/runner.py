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

import uuid

from browbeat.api import config
from browbeat.api import logger
from browbeat.api import tools

LOG = logger.LOG


class Browbeat(object):
    def __init__(self, args):
        self.args = args
        self.config = config.load_browbeat_config(self.args.config)
        self.tools = tools.Tools(self.args.config)

    def run(self):
        LOG.info('Running browbeat ...')

        browbeat_uuid = uuid.uuid4()
        workspace_dir = self.tools.create_workspace(
            self.config['browbeat']['workdir'], str(browbeat_uuid))
        LOG.debug('Created workspace: %s' % workspace_dir)
