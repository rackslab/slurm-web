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

import socket
import logging

from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


class SlurmwebAppRoute:
    def __init__(self, endpoint: str, func, methods=None):
        self.endpoint = endpoint
        self.func = func
        self.methods = methods


class SlurmrestdUnixConnection(HTTPConnection):
    def __init__(self, path):
        super().__init__("localhost")
        self.path = path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        logger.debug("Connecting to unix socket %s", self.path)
        self.sock.connect(str(self.path))


class SlurmrestdUnixConnectionPool(HTTPConnectionPool):
    def __init__(self, path):
        super().__init__("localhost")
        self.path = path

    def _new_conn(self):
        return SlurmrestdUnixConnection(self.path)


class SlurmrestdUnixAdapter(HTTPAdapter):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def get_connection(self, url, proxies=None):
        return SlurmrestdUnixConnectionPool(self.path)
