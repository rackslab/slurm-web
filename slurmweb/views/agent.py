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

from flask import Response, current_app, jsonify, stream_with_context
import requests
from rfl.web.tokens import rbac_action

from ..version import get_version
from . import SlurmrestdUnixAdapter


logger = logging.getLogger(__name__)


def version():
    return Response(f"Slurm-web agent v{get_version()}", mimetype="text/plain")


def info():
    data = {"cluster": current_app.settings.service.cluster}
    return jsonify(data)


@rbac_action("view-jobs")
def slurmrest(query):

    session = requests.Session()
    prefix = "http+unix://slurmrestd/"
    session.mount(prefix, SlurmrestdUnixAdapter(current_app.settings.slurmrestd.socket))
    response = session.get(f"{prefix}/{query}")
    return jsonify(response.json()), response.status_code


@rbac_action("view-jobs")
def stream_jobs():
    def stream():
        ping_message = 'event: ping\ndata: {"time": "now"}\n\n'
        yield ping_message.encode()
        for message in current_app.events.pubsub.listen():
            logger.debug("Received event message %s from pubsub", str(message))
            data = {"job_id": message["data"]}
            yield f"event: job\ndata: {json.dumps(data)}\n\n".encode()

    return Response(
        stream_with_context(stream()),
        mimetype="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
