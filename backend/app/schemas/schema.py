from pydantic import BaseModel


class ColumnSchema(BaseModel):
    name: str
    type: str
    nullable: bool
    default: str | None = None


class TableSchema(BaseModel):
    name: str
    columns: list[ColumnSchema]


class DatabaseSchema(BaseModel):
    tables: list[TableSchema]
