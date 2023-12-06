# Copyright (c) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import logging
from functools import wraps

from flask import Response, current_app, jsonify, request, abort
import requests
from rfl.web.tokens import check_jwt
from rfl.authentication.errors import LDAPAuthenticationError

from ..version import get_version


logger = logging.getLogger(__name__)


def validate_cluster(view):
    """Decorator for Flask views functions check for valid cluster path parameter."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        cluster = kwargs["cluster"]
        if cluster not in current_app.agents.keys():
            abort(
                404,
                f"Unable to retrieve {view.__name__} from cluster {cluster}, cluster "
                "not found",
            )
        return view(*args, **kwargs)

    return wrapped


def version():
    return Response(f"Slurm-web gateway v{get_version()}", mimetype="text/plain")


def login():
    try:
        idents = json.loads(request.data)
        user = current_app.authentifier.login(
            user=idents["user"], password=idents["password"]
        )
    except LDAPAuthenticationError as err:
        logger.warning(
            "LDAP authentication error for user %s: %s", idents["user"], str(err)
        )
        abort(401, str(err))
    logger.info("User %s authenticated successfully", user)
    # generate token
    token = current_app.jwt.generate(
        user=user, duration=current_app.settings.jwt.duration
    )
    # get permissions on all agents
    clusters = []
    for agent in current_app.agents.values():
        cluster = {"name": agent.cluster}
        response = request_agent(agent.cluster, "permissions", token)
        if response.status_code != 200:
            logger.error(
                "Unable to retrieve permissions from cluster %s: %d",
                agent.cluster,
                response.status_code,
            )
        else:
            cluster.update(response.json())
            clusters.append(cluster)
    return jsonify(
        result="Authentication successful",
        token=token,
        fullname=user.fullname,
        groups=user.groups,
        clusters=clusters,
    )


def request_agent(cluster: str, query: str, token: str = None):
    headers = {}
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}
    return requests.get(
        f"{current_app.agents[cluster].url}/{query}",
        headers=headers,
    )


def proxy_agent(cluster: str, query: str, token: str = None):
    response = request_agent(cluster, query, token)
    return jsonify(response.json()), response.status_code


@check_jwt
@validate_cluster
def stats(cluster: str):
    return proxy_agent(cluster, "stats", request.token)


@check_jwt
@validate_cluster
def jobs(cluster: str):
    return proxy_agent(cluster, "jobs", request.token)


@check_jwt
@validate_cluster
def nodes(cluster: str):
    return proxy_agent(cluster, "nodes", request.token)


@check_jwt
@validate_cluster
def qos(cluster: str):
    return proxy_agent(cluster, "qos", request.token)
