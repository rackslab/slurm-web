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

from rfl.web.tokens import RFLTokenizedWebApp
import requests

from . import SlurmwebApp
from ..views import SlurmwebAppRoute
from ..views import gateway as views
from ..auth import AuthenticatorFactory

logger = logging.getLogger(__name__)


class SlurmwebAgent:
    def __init__(self, cluster, url):
        self.cluster = cluster
        self.url = url

    @classmethod
    def from_json(cls, url, data):
        return cls(data["cluster"], url)


class SlurmwebAppGateway(SlurmwebApp, RFLTokenizedWebApp):

    NAME = "slurm-web-gateway"
    SITE_CONFIGURATION = "/etc/slurm-web/gateway.ini"
    SETTINGS_DEFINITION = "/usr/share/slurm-web/gateway.yml"
    VIEWS = {
        SlurmwebAppRoute("/version", views.version),
        SlurmwebAppRoute("/login", views.login, methods=["POST"]),
        SlurmwebAppRoute("/agents/:cluster/jobs", views.jobs),
        SlurmwebAppRoute("/agents/:cluster/nodes", views.nodes),
    }

    def __init__(self, args):
        SlurmwebApp.__init__(self, args)
        self.authenticator = AuthenticatorFactory.get(
            self.settings.authentication.method, self.settings
        )
        RFLTokenizedWebApp.__init__(
            self,
            audience=self.settings.jwt.audience,
            algorithm=self.settings.jwt.algorithm,
            key=self.settings.jwt.key,
        )
        # Get information from all agents
        self.agents = {}
        for url in self.settings.agents.url:
            try:
                logger.info("Retrieving info from agent at url %s", url)
                agent = self._agent_info(url)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.JSONDecodeError,
            ) as err:
                logger.error(
                    "Unable to retrieve agent info from url %s: [%s] %s",
                    url,
                    type(err).__name__,
                    str(err),
                )
            else:
                logger.debug(
                    "Discovered available agent for cluster %s at url %s",
                    agent.cluster,
                    url,
                )
                self.agents[agent.cluster] = agent

    def _agent_info(self, url: str) -> SlurmwebAgent:
        response = requests.get(f"{url}/info")
        return SlurmwebAgent.from_json(url, response.json())
