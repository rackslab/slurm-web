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

import ldap

from ._base import Authenticator
from ..errors import SlurmwebAuthenticationError


class AuthenticatorLdap(Authenticator):
    def __init__(self, settings):
        self.settings = settings.ldap

    def connection(self):

        connection = ldap.initialize(self.settings.uri.geturl())

        # LDAP/SSL setup
        if self.settings.uri.geturl().startswith("ldaps"):
            connection.protocol_version = ldap.VERSION3
            # Force cert validation
            connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
            if self.settings.cacert is not None:
                connection.set_option(ldap.OPT_X_TLS_CACERTFILE, self.settings.cacert)
            # Force libldap to create a new SSL context
            connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

        return connection

    def login(self, user, password) -> None:

        connection = self.connection()
        if user is None or password is None:
            raise SlurmwebAuthenticationError("invalid authentication request")

        try:
            # authenticate user on ldap
            user_dn = f"uid={user},{self.settings.user_base}"
            connection.simple_bind_s(user_dn, password)
        except ldap.SERVER_DOWN:
            raise SlurmwebAuthenticationError("LDAP server is unreachable")
        except ldap.INVALID_CREDENTIALS:
            raise SlurmwebAuthenticationError("user or password is incorrect")
        except ldap.NO_SUCH_OBJECT as error:
            raise SlurmwebAuthenticationError(f"no such object: {str(error)}")
        except ldap.UNWILLING_TO_PERFORM as error:
            raise SlurmwebAuthenticationError(
                f"LDAP server is unwilling to perform: {str(error)}"
            )
        finally:
            connection.unbind_s()
