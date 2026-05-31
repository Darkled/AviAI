from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_data_db
from app.services import schema_service
from app.schemas.schema import DatabaseSchema

router = APIRouter()


@router.get("/schema", response_model=DatabaseSchema)
async def get_schema(db: AsyncSession = Depends(get_data_db)):
    return await schema_service.get_database_schema(db)
