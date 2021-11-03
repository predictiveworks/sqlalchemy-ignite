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


class Error(Exception):

    def __init__(self, msg=None, error_trace=None):
        # for compatibility reasons we want to keep the exception message
        # attribute because clients may depend on it
        if msg:
            self.message = msg
        super(Error, self).__init__(msg)
        self.error_trace = error_trace


class IgniteWarning(Exception):
    pass


class InterfaceError(Error):
    pass


class IgniteError(Error):
    pass


class InternalError(IgniteError):
    pass


class OperationalError(IgniteError):
    pass


class ProgrammingError(IgniteError):
    pass


class IntegrityError(IgniteError):
    pass


class DataError(IgniteError):
    pass


class NotSupportedError(IgniteError):
    pass


# exceptions not in db api

class IgniteConnectionError(OperationalError):
    pass


class TimezoneUnawareException(Error):
    pass
