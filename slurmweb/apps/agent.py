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

import logging


from . import SlurmwebApp
from ..views import SlurmwebAppRoute
from ..views import agent as views
from ..auth import AuthenticatorFactory

logger = logging.getLogger(__name__)


class SlurmwebAppAgent(SlurmwebApp):

    NAME = "slurm-web-agent"
    SITE_CONFIGURATION = "/etc/slurm-web/agent.ini"
    SETTINGS_DEFINITION = "/usr/share/slurm-web/agent.yml"
    VIEWS = {
        SlurmwebAppRoute("/version", views.version),
        SlurmwebAppRoute("/login", views.login, methods=["POST"]),
        SlurmwebAppRoute("/<path:query>", views.slurmrest),
    }

    def __init__(self, *args):
        super().__init__(*args)
        self.authenticator = AuthenticatorFactory.get(
            self.settings.authentication.method, self.settings
        )
