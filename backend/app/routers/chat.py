import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ai_service import agent, Deps

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Handle chat messages and stream responses from the AI agent.
    Includes a 45-second timeout for the entire operation.
    """
    
    async def stream_response() -> AsyncGenerator[str, None]:
        deps = Deps(db=db)
        try:
            # Wrap the agent run in a timeout
            async with asyncio.timeout(45.0):
                async with agent.run_stream(request.message, deps=deps) as result:
                    async for message in result.stream_text(delta=True):
                        yield message
        except asyncio.TimeoutError:
            yield "\n\nI'm sorry, I'm taking too long to think. Please try a simpler question."
        except Exception as e:
            yield f"\n\nAn error occurred: {str(e)}"

    return StreamingResponse(stream_response(), media_type="text/plain")
