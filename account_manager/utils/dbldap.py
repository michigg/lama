from django.db import connections
from ldapdb.backends.ldap.compiler import SQLCompiler, query_as_ldap


def get_filterstr(qs):
    connection = connections['ldap']
    compiler = SQLCompiler(
        query=qs.query,
        connection=connection,
        using=None,
    )
    return query_as_ldap(qs.query, compiler, connection).filterstr