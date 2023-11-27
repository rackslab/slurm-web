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

import json
import logging

from flask import Response, current_app, jsonify, request, abort
import requests

from ..version import get_version
from ..errors import SlurmwebAuthenticationError


logger = logging.getLogger(__name__)


def version():
    return Response(f"Slurm-web gateway v{get_version()}", mimetype="text/plain")


def login():
    try:
        idents = json.loads(request.data)
        current_app.authenticator.login(
            user=idents["user"], password=idents["password"]
        )
    except SlurmwebAuthenticationError as err:
        abort(403, f"Authentication failed: {err}")
    # generate token
    token = current_app.jwt.generate(
        user=idents["user"], duration=current_app.settings.jwt.duration
    )
    return jsonify(
        result="Authentication successful",
        token=token,
        clusters=[agent.cluster for agent in current_app.agents.values()],
    )


def jobs(cluster):
    if cluster not in current_app.agent.keys():
        abort(404, f"Unable to retrieve jobs from cluster {cluster}, cluster not found")
    response = requests.get(f"{current_app.agents[cluster].url}/jobs")
    return jsonify(response.json()), response.status_code


def nodes(cluster):
    if cluster not in current_app.agent.keys():
        abort(
            404, f"Unable to retrieve nodes from cluster {cluster}, cluster not found"
        )
    response = requests.get(f"{current_app.agents[cluster].url}/jobs")
    return jsonify(response.json()), response.status_code
