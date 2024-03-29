#!/usr/bin/env python

# Borrowed from InfraRed project

# Copyright 2016 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import sys
import traceback

import colorlog

log_format = (
    '%(log_color)s'
    '%(asctime)s - '
    '%(message)s'
)

logger_formatter = colorlog.ColoredFormatter(
    log_format,
    log_colors=dict(
        DEBUG='blue',
        INFO='green',
        WARNING='yellow',
        ERROR='red',
        CRITICAL='bold_red,bg_white',
    )
)

LOGGER_NAME = "BrowbeatLogger"
DEFAULT_LOG_LEVEL = logging.INFO

LOG = logging.getLogger(LOGGER_NAME)
LOG.setLevel(DEFAULT_LOG_LEVEL)

# Create stream handler with debug level
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

# Add the logger_formatter to sh
sh.setFormatter(logger_formatter)

# Create logger and add handler to it
LOG.addHandler(sh)


def browbeat_excepthook(exc_type, exc_value, exc_traceback):
    """exception hook that sends OctarioException to log and other

    exceptions to stderr (default excepthook)
    """
    from browbeat.api.exceptions import BrowbeatExceptions

    # sends full exception with trace to log
    if not isinstance(exc_value, BrowbeatExceptions):
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)

    if LOG.getEffectiveLevel() <= logging.DEBUG:
        formated_exception = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback))
        LOG.error(formated_exception + exc_value.message)
    else:
        LOG.error(exc_value.message)


sys.excepthook = browbeat_excepthook
