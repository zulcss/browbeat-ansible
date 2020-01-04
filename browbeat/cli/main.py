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

import argparse
import logging
import os
import sys

from browbeat.api import exceptions
from browbeat.api import logger
from browbeat.api import runner

LOG = logger.LOG


class BrowbeatShell(object):
    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog="browbeat",
            description="Openstack Performance benchmark orchestrator",
            add_help=False)
        parser.add_argument('-?', '-h', '--help',
                            action='help',
                            help='show this help message and exit')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='increase output verbosity')
        parser.add_argument('-C', '--config',
                            help='browbeat configuration file')
        parser.add_argument('-i', '--inventory',
                            help='browbeat inventory for Openstack cloud')

        return parser

    def parsed_args(self, argv):
        parser = self.get_base_parser()
        args = parser.parse_args(argv)

        if args.verbose:
            LOG.setLevel(level=logging.DEBUG)
            LOG.debug("browbeat running in debug mode.")

        if not args.config:
            raise exceptions.CommandError("You must provide workload option "
                                          "via --config.")
        if not args.inventory:
            raise exceptions.CommandError("You must provide workload option "
                                          "via --inventory.")
        if not os.path.exists(args.inventory):
            raise Exception('Unable to find inventory: %s' %
                            self.args.inventory)

        return args

    def main(self, argv):
        parsed_args = self.parsed_args(argv)

        logging.getLogger('pykwalify').setLevel(logging.WARNING)

        LOG.debug("CLI Args: {}".format(parsed_args))

        runner.Browbeat(parsed_args).run()


def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]
        BrowbeatShell().main(args)
    except exceptions.BrowbeatExceptions as ex:
        LOG.error(ex.message)
        sys.exit(1)
    except Exception:
        raise
        sys.exit(1)
