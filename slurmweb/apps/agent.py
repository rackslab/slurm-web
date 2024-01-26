# Copyright (c) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# SPDX-License-Identifier: GPL-3.0-or-later


import logging

from rfl.web.tokens import RFLTokenizedRBACWebApp
from racksdb.web.app import RacksDBWebBlueprint

from . import SlurmwebWebApp
from ..views import SlurmwebAppRoute
from ..views import agent as views
from ..cache import CachingService

logger = logging.getLogger(__name__)


class SlurmwebAppAgent(SlurmwebWebApp, RFLTokenizedRBACWebApp):

    NAME = "slurm-web-agent"
    SITE_CONFIGURATION = "/etc/slurm-web/agent.ini"
    SETTINGS_DEFINITION = "/usr/share/slurm-web/agent.yml"
    VIEWS = {
        SlurmwebAppRoute("/version", views.version),
        SlurmwebAppRoute("/info", views.info),
        SlurmwebAppRoute("/permissions", views.permissions),
        SlurmwebAppRoute("/stats", views.stats),
        SlurmwebAppRoute("/jobs", views.jobs),
        SlurmwebAppRoute("/job/<int:job>", views.job),
        SlurmwebAppRoute("/nodes", views.nodes),
        SlurmwebAppRoute("/qos", views.qos),
        SlurmwebAppRoute("/accounts", views.accounts),
    }

    def __init__(self, args):
        SlurmwebWebApp.__init__(self, args)
        self.register_blueprint(
            RacksDBWebBlueprint(
                db=self.settings.racksdb.db,
                ext=self.settings.racksdb.extensions,
                schema=self.settings.racksdb.schema,
                drawings_schema=self.settings.racksdb.drawings_schema,
            ),
            url_prefix="/racksdb",
        )
        if self.settings.policy.roles.exists():
            logger.debug("Select RBAC site roles policy %s", self.settings.policy.roles)
            selected_roles_policy_path = self.settings.policy.roles
        else:
            logger.debug(
                "Select default RBAC vendor roles policy %s",
                self.settings.policy.vendor_roles,
            )
            selected_roles_policy_path = self.settings.policy.vendor_roles
        RFLTokenizedRBACWebApp.__init__(
            self,
            audience=self.settings.jwt.audience,
            algorithm=self.settings.jwt.algorithm,
            key=self.settings.jwt.key,
            policy=self.settings.policy.definition,
            roles=selected_roles_policy_path,
        )
        self.cache = CachingService(
            host=self.settings.cache.host,
            port=self.settings.cache.port,
            password=self.settings.cache.password,
        )
