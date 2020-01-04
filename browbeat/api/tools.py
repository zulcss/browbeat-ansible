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
import sys

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
