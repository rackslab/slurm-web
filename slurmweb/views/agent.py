# Copyright (c) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from flask import Response, current_app, jsonify, abort, request
import requests
from rfl.web.tokens import rbac_action, check_jwt

from ..version import get_version
from . import SlurmrestdUnixAdapter


logger = logging.getLogger(__name__)


def version():
    return Response(f"Slurm-web agent v{get_version()}", mimetype="text/plain")


def info():
    data = {"cluster": current_app.settings.service.cluster}
    return jsonify(data)


@check_jwt
def permissions():
    roles, actions = current_app.policy.roles_actions(request.user)
    return jsonify(
        {
            "roles": list(roles),
            "actions": list(actions),
        }
    )


def slurmrest(query):

    session = requests.Session()
    prefix = "http+unix://slurmrestd/"
    session.mount(prefix, SlurmrestdUnixAdapter(current_app.settings.slurmrestd.socket))
    try:
        response = session.get(f"{prefix}/{query}")
        return response.json()
    except requests.exceptions.ConnectionError as err:
        abort(500, f"Unable to connect to slurmrestd: {err}")


@rbac_action("view-stats")
def stats():
    data = slurmrest("/slurm/v0.0.39/jobs")
    total = 0
    running = 0
    for job in data["jobs"]:
        total += 1
        if "RUNNING" in job["job_state"]:
            running += 1
    data = slurmrest("/slurm/v0.0.39/nodes")
    nodes = 0
    cores = 0
    for node in data["nodes"]:
        nodes += 1
        cores += node["cpus"]
    return jsonify(
        {
            "resources": {"nodes": nodes, "cores": cores},
            "jobs": {"running": running, "total": total},
        }
    )


@rbac_action("view-jobs")
def jobs():
    return jsonify(slurmrest("/slurm/v0.0.39/jobs")["jobs"])


@rbac_action("view-nodes")
def nodes():
    return jsonify(slurmrest("/slurm/v0.0.39/nodes")["nodes"])


@rbac_action("view-qos")
def qos():
    return jsonify(slurmrest("/slurmdb/v0.0.39/qos")["qos"])
