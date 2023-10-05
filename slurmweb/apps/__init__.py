#!/usr/bin/env python3
#
# Copyright (C) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# Slurm-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Slurm-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Slurm-web.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
import sys
import logging

from flask import Flask
from rfl.settings import RuntimeSettings
from rfl.settings.errors import SettingsDefinitionError

from ..log import setup_logger, TTYFormatter

logger = logging.getLogger(__name__)


class SlurmwebAppArgs:
    pass


class SlurmwebApp(Flask):

    NAME = None
    SITE_CONFIGURATION = None
    SETTINGS_DEFINITION = None
    VIEWS = set()

    def __init__(self, args: SlurmwebAppArgs):
        super().__init__(self.NAME)
        # load configuration files
        setup_logger(
            "slurmweb",
            TTYFormatter,
            debug=args.debug,
            show_libs_logs=args.full_debug,
        )
        try:
            self.settings = RuntimeSettings.yaml_definition(args.conf_defs)
        except SettingsDefinitionError as err:
            logger.critical(err)
            sys.exit(1)
        self.settings.override_ini(args.conf)
        # set URL rules
        for route in self.VIEWS:
            kwargs = dict()
            if route.methods is not None:
                kwargs["methods"] = route.methods
            self.add_url_rule(route.endpoint, view_func=route.func, **kwargs)
        self.debug = args.full_debug

    def run(self):
        logger.info("Running %s application", self.NAME)
        if self.settings.service.cors:
            logger.debug("CORS is enabled")
            from flask_cors import CORS

            CORS(self)
        super().run(
            host=self.settings.service.interface,
            port=self.settings.service.port,
            debug=self.debug,
        )
