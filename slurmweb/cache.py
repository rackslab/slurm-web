# Copyright (c) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union

import redis
import pickle

from .errors import SlurmwebCacheError


class CachingService:
    def __init__(self, host: str, port: int, password: Union[str, None]):
        self.host = host
        self.port = port
        self.connection = redis.Redis(host=host, port=port, password=password)

    def put(self, key, value):
        try:
            self.connection.set(key, pickle.dumps(value), ex=60)
        except redis.exceptions.ConnectionError as err:
            raise SlurmwebCacheError(str(err)) from err

    def get(self, key):
        try:
            value = self.connection.get(key)
            if value is not None:
                value = pickle.loads(value)
            return value
        except redis.exceptions.ConnectionError as err:
            raise SlurmwebCacheError(str(err)) from err
