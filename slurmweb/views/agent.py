# Copyright (c) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union
import logging

from flask import Response, current_app, jsonify, abort, request
import requests
from rfl.web.tokens import rbac_action, check_jwt

from ..version import get_version
from ..errors import SlurmwebCacheError
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
    except requests.exceptions.ConnectionError as err:
        logger.error("Unable to connect to slurmrestd: %s", err)
        abort(500, f"Unable to connect to slurmrestd: {err}")
    result = response.json()
    if len(result["errors"]):
        logger.error("slurmrestd query %s errors: %s", query, result["errors"])
        abort(500, f"slurmrestd errors: {str(result['errors'])}")
    if len(result["warnings"]):
        logger.warning("slurmrestd query %s warnings: %s", query, result["warnings"])
        # abort(500, f"slurmrestd warnings: {str(result['warnings'])}")
    return result


def filter_fields(items, selection: Union[list[str], None]):
    if selection is not None:
        for item in items:
            for key in list(item.keys()):
                if key not in selection:
                    del item[key]
    return items


def _cached_data(
    cache_key: str, query: str, result_key: str, filters: Union[list[str], None]
):
    if not current_app.settings.cache.enabled:
        return filter_fields(slurmrest(query)[result_key], filters)
    try:
        data = current_app.cache.get(cache_key)
        if data is None:
            data = filter_fields(slurmrest(query)[result_key], filters)
            current_app.cache.put(cache_key, data)
        return data
    except SlurmwebCacheError as err:
        logger.error("Cache error: %s", str(err))
        abort(500, f"Cache error: {str(err)}")


def _cached_jobs():
    return _cached_data(
        "jobs",
        f"/slurm/v{current_app.settings.slurmrestd.version}/jobs",
        "jobs",
        current_app.settings.filters.jobs,
    )


def _cached_job(job):
    return _cached_data(
        f"job-{job}",
        f"/slurm/v{current_app.settings.slurmrestd.version}/job/{job}",
        "jobs",
        None,
    )[0]


def _cached_nodes():
    return _cached_data(
        "nodes",
        f"/slurm/v{current_app.settings.slurmrestd.version}/nodes",
        "nodes",
        current_app.settings.filters.nodes,
    )


def _cached_qos():
    return _cached_data(
        "qos",
        f"/slurmdb/v{current_app.settings.slurmrestd.version}/qos",
        "qos",
        current_app.settings.filters.qos,
    )


def _cached_accounts():
    return _cached_data(
        "accounts",
        f"/slurmdb/v{current_app.settings.slurmrestd.version}/accounts",
        "accounts",
        current_app.settings.filters.accounts,
    )


@rbac_action("view-stats")
def stats():
    total = 0
    running = 0
    for job in _cached_jobs():
        total += 1
        if "RUNNING" in job["job_state"]:
            running += 1

    nodes = 0
    cores = 0
    for node in _cached_nodes():
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
    return jsonify(_cached_jobs())


@rbac_action("view-jobs")
def job(job: int):
    return jsonify(_cached_job(job))


@rbac_action("view-nodes")
def nodes():
    return jsonify(_cached_nodes())


@rbac_action("view-qos")
def qos():
    return jsonify(_cached_qos())


@rbac_action("view-accounts")
def accounts():
    return jsonify(_cached_accounts())
