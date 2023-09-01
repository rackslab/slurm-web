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

from ._base import Authenticator
from .ldap import AuthenticatorLdap
from ..errors import SlurmwebRuntimeError


class AuthenticatorFactory:

    MAP = {"ldap": AuthenticatorLdap}

    @staticmethod
    def get(method: str, settings) -> Authenticator:
        try:
            return AuthenticatorFactory.MAP[method](settings)
        except KeyError:
            raise SlurmwebRuntimeError(f"Unsupported authentication method {method}")
