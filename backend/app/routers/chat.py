import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ai_service import agent, Deps

from pydantic_ai.messages import PartDeltaEvent, TextPartDelta

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Handle chat messages and stream responses from the AI agent.
    Includes a 90-second timeout for the entire operation.
    """
    
    async def stream_response() -> AsyncGenerator[str, None]:
        deps = Deps(db=db)
        try:
            # Increased timeout to 90 seconds for slower models and complex queries
            async with asyncio.timeout(90.0):
                # Use run_stream_events to robustly capture text from all turns (tool calls)
                async with agent.run_stream_events(request.message, deps=deps) as stream:
                    async for event in stream:
                        if isinstance(event, PartDeltaEvent):
                            if isinstance(event.delta, TextPartDelta):
                                yield event.delta.content_delta
        except asyncio.TimeoutError:
            yield "\n\nI'm sorry, I'm taking too long to think. Please try a simpler question."
        except Exception as e:
            yield f"\n\nAn error occurred: {str(e)}"

    return StreamingResponse(stream_response(), media_type="text/plain")
