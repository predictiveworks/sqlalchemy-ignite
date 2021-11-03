# -*- coding: utf-8; -*-
#
# Copyright (c) 2020 - 2021 Dr. Krusche & Partner PartG. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# @author Stefan Krusche, Dr. Krusche & Partner PartG
#

from .exceptions import ProgrammingError
from .cursor import Cursor
from .ignite import IgniteContext


class Connection(object):

    def __init__(self,
                 servers=None,
                 # (optional) sets timeout (in seconds) for each socket operation including
                 # `connect`. 0 means non-blocking mode, which is virtually guaranteed to fail.
                 # Can accept integer or float value. Default is None (blocking mode).
                 timeout=None,
                 # (optional) sets timeout (in seconds) for performing handshake (connection)
                 # with node. Default is 10.0 seconds.
                 handshake_timeout=10.0,
                 # (optional) set to True if Ignite server uses SSL on its binary connector.
                 # Defaults to use SSL when username and password has been supplied, not to use
                 # SSL otherwise.
                 use_ssl=None,
                 # (optional) SSL version constant from standard `ssl` module. Defaults to TLS v1.2.
                 ssl_version=None,
                 # (optional) ciphers to use. If not provided, `ssl` default ciphers are used.
                 ssl_ciphers=None,
                 # (optional) determines how the remote side certificate is treated:
                 #
                 # * `ssl.CERT_NONE`        − remote certificate is ignored (default),
                 # * `ssl.CERT_OPTIONAL`    − remote certificate will be validated,
                 #
                 # if provided,
                 # * `ssl.CERT_REQUIRED`    − valid remote certificate is required
                 #
                 ssl_cert_reqs=None,
                 # (optional) a path to SSL key file to identify local (client) party
                 ssl_keyfile=None,
                 # (optional) password for SSL key file, can be provided when key file is
                 # encrypted to prevent OpenSSL password prompt
                 ssl_keyfile_password=None,
                 # (optional) a path to ssl certificate file to identify local (client) party.
                 ssl_certfile=None,
                 # (optional) a path to a trusted certificate or a certificate chain.
                 # Required to check the validity of the remote (server-side) certificate
                 ssl_ca_certfile=None,
                 # (optional) user name to authenticate to Ignite cluster
                 username=None,
                 # password to authenticate to Ignite cluster.
                 password=None,
                 ):

        if servers:

            tokens = servers.split(":", 1)

            host = tokens[0]
            port = int(tokens[1])

            self.context = IgniteContext(
                host=host,
                port=port,
                timeout=timeout,
                handshake_timeout=handshake_timeout,
                use_ssl=use_ssl,
                ssl_ciphers=ssl_ciphers,
                ssl_cert_reqs=ssl_cert_reqs,
                ssl_keyfile=ssl_keyfile,
                ssl_keyfile_password=ssl_keyfile_password,
                ssl_certfile=ssl_certfile,
                ssl_ca_certfile=ssl_ca_certfile,
                username=username,
                password=password,
            )

            self._closed = False

        else:
            raise ProgrammingError("No connection url provided.")

    def cursor(self):
        """
        Return a new Cursor Object using the connection.
        """
        if not self._closed:
            return Cursor(self)
        else:
            raise ProgrammingError("Connection closed")

    def close(self):
        """
        Close the connection now
        """
        self._closed = True
        self.context.close()

    def commit(self):
        """
        Transactions are not supported, so ``commit`` is not implemented.
        """
        if self._closed:
            raise ProgrammingError("Connection closed")

    def is_closed(self):
        return self._closed

    def __repr__(self):
        return '<Connection {0}>'.format(repr(self.context))

    def __enter__(self):
        return self

    def __exit__(self, *excs):
        self.close()


# For backwards compatibility and not to break existing imports
connect = Connection
