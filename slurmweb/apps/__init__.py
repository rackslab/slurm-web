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
import logging

from flask import Flask
from rfl.settings import RuntimeSettings

from ..log import setup_logger, TTYFormatter

logger = logging.getLogger(__name__)


class SlurmwebApp(Flask):
    def __init__(self, debug: bool, show_libs_logs: bool, vendor_conf, site_conf):
        super().__init__(self.NAME)
        # load configuration files
        setup_logger(
            "slurmweb", TTYFormatter, debug=debug, show_libs_logs=show_libs_logs
        )
        self.settings = RuntimeSettings.definition_yaml(Path(self.SETTINGS_DEFINITION))
        self.settings.override_ini(Path(self.SITE_CONFIGURATION))
        # set URL rules
        for route in self.VIEWS:
            kwargs = dict()
            if route.methods is not None:
                kwargs["methods"] = route.methods
            self.add_url_rule(route.endpoint, view_func=route.func, **kwargs)

    def run(self, debug: bool = False):
        logger.info("Running %s application", self.NAME)
        super().run(
            host="localhost",
            port=3332,
            debug=debug,
        )
