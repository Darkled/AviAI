import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.services.ai_service import agent, Deps, model
from app.models.chat import Chat, Message
from pydantic_ai import Agent

from pydantic_ai.messages import PartDeltaEvent, TextPartDelta

router = APIRouter()
title_agent = Agent(model)

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[int] = None

class MessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/chats", response_model=List[ChatSchema])
async def get_chats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chat).order_by(desc(Chat.updated_at)))
    return result.scalars().all()

@router.get("/chats/{chat_id}/messages", response_model=List[MessageSchema])
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at)
    )
    messages = result.scalars().all()
    if not messages:
        # Check if chat exists
        chat_result = await db.execute(select(Chat).where(Chat.id == chat_id))
        if not chat_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Chat not found")
    return messages

@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    await db.delete(chat)
    await db.commit()
    return {"status": "success"}

@router.post("/chat")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Handle chat messages, stream responses, and persist to database.
    """
    
    # 1. Get or create chat
    if request.chat_id:
        result = await db.execute(select(Chat).where(Chat.id == request.chat_id))
        chat_obj = result.scalar_one_or_none()
        if not chat_obj:
            raise HTTPException(status_code=404, detail="Chat not found")
    else:
        chat_obj = Chat(title="New Chat")
        db.add(chat_obj)
        await db.flush() # Get ID
    
    # 2. Save user message
    user_msg = Message(chat_id=chat_obj.id, role="user", content=request.message)
    db.add(user_msg)
    await db.commit()

    async def stream_response() -> AsyncGenerator[str, None]:
        deps = Deps(db=db)
        assistant_content = ""
        
        try:
            async with asyncio.timeout(90.0):
                # Use run_stream_events to robustly capture text
                async with agent.run_stream_events(request.message, deps=deps) as stream:
                    async for event in stream:
                        if isinstance(event, PartDeltaEvent):
                            if isinstance(event.delta, TextPartDelta):
                                content = event.delta.content_delta
                                assistant_content += content
                                yield content
            
            # 3. Save assistant message when complete
            if assistant_content:
                assistant_msg = Message(chat_id=chat_obj.id, role="assistant", content=assistant_content)
                db.add(assistant_msg)
                
                # 4. Auto-rename chat if it's the first message
                result = await db.execute(select(Message).where(Message.chat_id == chat_obj.id))
                msg_count = len(result.scalars().all())
                
                if msg_count <= 2 and chat_obj.title == "New Chat":
                    try:
                        # Use title_agent to avoid main agent's system prompt constraints
                        title_run = await title_agent.run(
                            f"Based on this initial query: '{request.message}', generate a short, concise 3-5 word title for this chat. Respond ONLY with the title."
                        )
                        # Access data safely
                        if hasattr(title_run, 'data'):
                            chat_obj.title = str(title_run.data).strip().strip('"').strip("'")
                        elif hasattr(title_run, 'content'):
                            chat_obj.title = str(title_run.content).strip().strip('"').strip("'")
                    except Exception as title_err:
                        print(f"Failed to generate title: {title_err}")
                        # Keep "New Chat" if title generation fails
                
                await db.commit()
                
                # Send the chat_id and title at the end as a special JSON chunk
                yield f"\n\n[METADATA]{{\"chat_id\": {chat_obj.id}, \"title\": \"{chat_obj.title}\"}}"

        except asyncio.TimeoutError:
            yield "\n\nI'm sorry, I'm taking too long to think. Please try a simpler question."
        except Exception as e:
            yield f"\n\nAn error occurred: {str(e)}"

    return StreamingResponse(stream_response(), media_type="text/plain")
