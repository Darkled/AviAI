import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base
from app.core.middleware import LoggingMiddleware
from app.routers import health, schema, chat

app = FastAPI(
    title="AI PostgreSQL Chat API",
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(LoggingMiddleware)

# Initialize Logfire
if settings.logfire_token:
    logfire.configure(token=settings.logfire_token)
    # Instrument Pydantic AI for agent tracing
    logfire.instrument_pydantic_ai()
    # Instrument HTTPX for deep visibility into API calls
    logfire.instrument_httpx(capture_all=True)
    # Instrument FastAPI
    logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(schema.router, prefix="/api", tags=["schema"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
