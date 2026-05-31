from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.middleware import LoggingMiddleware
from app.routers import health

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI PostgreSQL Chat API",
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
