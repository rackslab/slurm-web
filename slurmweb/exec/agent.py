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

import argparse
from pathlib import Path

from ..version import get_version

from ..apps import SlurmwebAppArgs
from ..apps.agent import SlurmwebAppAgent


class SlurmwebExecAgent:
    @staticmethod
    def run():
        parser = argparse.ArgumentParser(description=SlurmwebAppAgent.NAME)
        parser.add_argument(
            "-v",
            "--version",
            dest="version",
            action="version",
            version="%(prog)s " + get_version(),
        )
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            help="Enable debug mode",
        )
        parser.add_argument(
            "--full-debug",
            dest="full_debug",
            action="store_true",
            help="Enable full debug mode",
        )
        parser.add_argument(
            "--conf-defs",
            help="Path to configuration settings definition file (default: %(default)s)",
            default=SlurmwebAppAgent.SETTINGS_DEFINITION,
            type=Path,
        )
        parser.add_argument(
            "--conf",
            help="Path to configuration file (default: %(default)s)",
            default=SlurmwebAppAgent.SITE_CONFIGURATION,
            type=Path,
        )

        application = SlurmwebAppAgent(parser.parse_args(namespace=SlurmwebAppArgs))
        application.run()
