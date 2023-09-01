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

from flask import Response, current_app, jsonify
import requests

from ..version import get_version
from ..errors import SlurmwebAuthenticationError
from . import SlurmrestdUnixAdapter


def version():
    return Response(f"Slurm-web agent v{get_version()}", mimetype="text/plain")


def login():
    try:
        current_app.authenticator.login(json.loads(request.data))
    except SlurmwebAuthenticationError:
        return jsonify(error="Authentication failed"), 403
    return jsonify(result="Authentication successful")


def slurmrest(query):

    session = requests.Session()
    prefix = "http+unix://slurmrestd/"
    session.mount(prefix, SlurmrestdUnixAdapter(current_app.settings.slurmrestd.socket))
    response = session.get(f"{prefix}/{query}")
    return jsonify(response.json()), response.status_code
