from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import Insert

# copy and modified from https://github.com/sqlalchemy/sqlalchemy/issues/5374#issuecomment-752693165

"""
When imported, automatically make all insert not fail on duplicate keys
"""


# modified
@compiles(Insert, "sqlite")
def sqlite_insert_ignore(insert, compiler, **kw):
    statement = compiler.visit_insert(insert, **kw)
    # len("INSERT") == 6
    return f'{statement[:6]}{ " OR IGNORE "}{statement[6:]}'


@compiles(Insert, "mysql")
def mysql_insert_ignore(insert, compiler, **kw):
    return compiler.visit_insert(insert.prefix_with("IGNORE"), **kw)


@compiles(Insert, "postgresql")
def postgresql_on_conflict_do_nothing(insert, compiler, **kw):
    statement = compiler.visit_insert(insert, **kw)
    # IF we have a "RETURNING" clause, we must insert before it
    returning_position = statement.find("RETURNING")
    if returning_position >= 0:
        return (
            statement[:returning_position]
            + "ON CONFLICT DO NOTHING "
            + statement[returning_position:]
        )
    else:
        return statement + " ON CONFLICT DO NOTHING"
