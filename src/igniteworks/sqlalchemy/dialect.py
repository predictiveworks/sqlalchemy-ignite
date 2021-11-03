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

from abc import ABC

from sqlalchemy import types as sqltypes
from sqlalchemy.engine import reflection
from sqlalchemy.engine.default import DefaultDialect

from igniteworks.sqlalchemy import types as ignite_types

"""
The system data types are specified in form of Java data types;
the current implementation version does not support spatial geometry 
types from com.vividsolutions.jts library
"""
TYPES_MAP = {
    # BINARY
    "byte[]": sqltypes.BINARY,
    # BOOLEAN
    "java.lang.Boolean": sqltypes.Boolean,
    # BYTE
    "java.lang.Byte": ignite_types.TINYINT,
    # DATE: The format is yyyy-MM-dd.
    "java.sql.Date": sqltypes.DATE,
    # DOUBLE
    "java.lang.Double": sqltypes.DECIMAL,
    # DECIMAL
    "java.math.BigDecimal": sqltypes.DECIMAL,
    # FLOAT
    "java.lang.Float": sqltypes.Float,
    # INTEGER
    "java.lang.Integer": sqltypes.Integer,
    # LONG
    "java.lang.Long": sqltypes.BIGINT,
    # SHORT
    "java.lang.Short": sqltypes.SmallInteger,
    # STRING
    "java.lang.String": sqltypes.String,
    # TIME: The format is hh:mm:ss.
    "java.sql.Time": sqltypes.TIME,
    # TIMESTAMP: The format is yyyy-MM-dd hh:mm:ss[.nnnnnnnnn].
    "java.sql.Timestamp": sqltypes.TIMESTAMP,
}


def _resolve_type(col_type):
    return TYPES_MAP.get(col_type, sqltypes.UserDefinedType)


"""
column = [
    0 - "name":         col_name,
    1 - "alias":        col_alias,
    2 - "type":         col_type,
    3 - "is_key":       is_key,
    4 - "is_nullable":  is_nullable,
    5 - "precision":    precision,
    6 - "scale":        scale,
]
"""


def _create_column_info(row):
    nullable = True if row[4] == "true" else False
    return {
        'name': row[0],
        'type': _resolve_type(row[2]),
        'nullable': nullable
    }


class IgniteDialect(DefaultDialect, ABC):
    name = 'igniteworks'

    def __init__(self, *args, **kwargs):
        super(IgniteDialect, self).__init__(*args, **kwargs)

    @classmethod
    def dbapi(cls):
        import igniteworks.client as connection
        return connection

    def connect(self, host=None, port=None, *args, **kwargs):

        server = None
        if host:
            server = '{0}:{1}'.format(host, port or '10800')
        if 'servers' in kwargs:
            server = kwargs.pop('servers')
        if server:
            return self.dbapi.connect(servers=server, **kwargs)

        return self.dbapi.connect(**kwargs)

    def do_rollback(self, connection):
        # if any exception is raised by the dbapi, sqlalchemy by default
        # attempts to do a rollback. Apache Ignite supports transactions,
        # but the current version of this dialect does not implement them
        # yet. Implementing this as noop seems to cause sqlalchemy to
        # propagate the original exception to the user
        pass

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        """
        Retrieve column names and types that refer to a certain
        Apache Ignite cache or table
        """
        sql = "GET COLUMNS FROM " + table_name
        if schema:
            sql += " WITH " + schema

        cursor = connection.execute(sql)
        return [_create_column_info(row) for row in cursor.fetchall()]

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        """
        This method retrieves all schemas registered in an
        Apache Ignite cluster

        The connection object refers to the Cursor object
        """
        sql = "GET CACHES"

        cursor = connection.execute(sql)
        schemas = cursor.fetchall()

        if len(schemas) == 0:
            return []

        return [row[0] for row in schemas]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        """
        This method retrieves all tables (caches) that are
        currently available. The result is exposed as a list
        of tables names (Strings).

        The connection object refers to the Cursor object
        """
        sql = "GET TABLES"
        if schema:
            sql += " FROM " + schema

        cursor = connection.execute(sql)
        tables = cursor.fetchall()

        if len(tables) == 0:
            return []

        return [row[0] for row in tables]

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        """
        Retrieve column names that build the (primary) key
        """
        sql = "GET KEYS FROM " + table_name
        if schema:
            sql += " WITH " + schema

        cursor = connection.execute(sql)
        rows = cursor.fetchall()
        keys = [row[0] for row in rows]

        return {
            "name": "PRIMARY KEY",
            "constrained_columns": keys
        }

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None,
                         postgresql_ignore_search_path=False, **kw):
        # Apache Ignite doesn't support foreign keys,
        # so this remains empty
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        """
        Retrieving index is not supported by the current implementation
        """
        return []


dialect = IgniteDialect
