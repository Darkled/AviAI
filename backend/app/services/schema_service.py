from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema import ColumnSchema, TableSchema, DatabaseSchema


async def get_database_schema(db: AsyncSession) -> DatabaseSchema:
    dialect = db.bind.dialect.name
    
    if dialect == "postgresql":
        return await _get_postgres_schema(db)
    elif dialect == "sqlite":
        return await _get_sqlite_schema(db)
    else:
        raise ValueError(f"Unsupported dialect: {dialect}")


async def _get_postgres_schema(db: AsyncSession) -> DatabaseSchema:
    # Get all tables in the public schema
    tables_query = text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
    )
    result = await db.execute(tables_query)
    table_names = [row[0] for row in result.all()]

    tables = []
    for table_name in table_names:
        # Get columns for each table
        columns_query = text(
            "SELECT column_name, data_type, is_nullable, column_default "
            "FROM information_schema.columns "
            "WHERE table_schema = 'public' AND table_name = :table_name "
            "ORDER BY ordinal_position;"
        )
        col_result = await db.execute(columns_query, {"table_name": table_name})
        columns = [
            ColumnSchema(
                name=row[0],
                type=row[1],
                nullable=row[2] == "YES",
                default=str(row[3]) if row[3] is not None else None,
            )
            for row in col_result.all()
        ]
        tables.append(TableSchema(name=table_name, columns=columns))

    return DatabaseSchema(tables=tables)


async def _get_sqlite_schema(db: AsyncSession) -> DatabaseSchema:
    # Get all tables
    tables_query = text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    result = await db.execute(tables_query)
    table_names = [row[0] for row in result.all()]

    tables = []
    for table_name in table_names:
        # Get columns for each table using PRAGMA
        columns_query = text(f"PRAGMA table_info('{table_name}');")
        col_result = await db.execute(columns_query)
        columns = [
            ColumnSchema(
                # PRAGMA table_info returns (id, name, type, notnull, default_value, pk)
                name=row[1],
                type=row[2],
                nullable=not bool(row[3]),
                default=str(row[4]) if row[4] is not None else None,
            )
            for row in col_result.all()
        ]
        tables.append(TableSchema(name=table_name, columns=columns))

    return DatabaseSchema(tables=tables)
