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
import yaml

from pykwalify import core as pykwalify_core
from pykwalify import errors as pykwalify_errors

from browbeat.api import logger
from browbeat.api.path import conf_schema_path

LOG = logger.LOG


def load_browbeat_config(path):
    """Loads and validates an entire Browbeat config per the expected schema.

    :param path: The path to the Browbeat Config file
    """
    try:
        path = os.path.expanduser(path)

        if not os.path.exists(path):
            LOG.error('Config does not exists: %s' % path)
            sys.exit(1)

        with open(path, 'r') as config:
            browbeat_config = yaml.safe_load(config)

        # Validate base config for Browbeat format
        _validate_yaml("browbeat", browbeat_config)
        LOG.info("Config {} validated".format(path))

        for workload in browbeat_config["workloads"]:
            _validate_yaml(workload["type"], workload)
            LOG.debug("Workload {} validated as {}".format(
                workload["name"], workload["type"]))

        return browbeat_config
    except yaml.YAMLError as e:
        LOG.error("Unable to parse configuration file: %s" %
                  config)
        error_msg = ("The request body must be properly formatted YAML. "
                     "Details: %s." % e)
        LOG.error(error_msg)
        sys.exit(1)


def _validate_yaml(schema, config):
    """Raises exception if config is invalid.

    :param schema: The schema to validate with (browbeat, rally...)
    :param config: Loaded yaml to validate
    """
    check = pykwalify_core.Core(
        source_data=config, schema_files=["{}/{}.yml".format(
            conf_schema_path, schema)])
    try:
        check.validate(raise_exception=True)
    except pykwalify_errors.SchemaError as e:
        LOG.error("Schema validation failed")
        raise Exception(
            "File does not conform to {} schema: {}".format(schema, e))
