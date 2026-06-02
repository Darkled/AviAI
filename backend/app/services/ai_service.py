import re
from dataclasses import dataclass
from typing import Any

from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.schema_service import get_database_schema

@dataclass
class Deps:
    db: AsyncSession

# Initialize OpenRouter model (OpenRouter is OpenAI compatible)
model = OpenAIChatModel(
    settings.openrouter_model,
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    ),
)

# Define the agent
agent = Agent(
    model,
    deps_type=Deps,
    end_strategy="exhaustive",
    system_prompt=(
        "You are an Aviation Data Expert. Your goal is to help users analyze their aircraft fleet data."
        "You have access to a PostgreSQL database with two main tables: 'aircraft_models' and 'fleet'."
        "Use the 'get_db_schema' tool to understand the available tables and columns."
        "Always use the 'execute_sql' tool to query the database."
        "IMPORTANT: You can only execute SELECT queries. Do not attempt to modify the database."
        "After getting results, provide a clear, human-readable explanation of the data."
        "If the user asks for something not related to aviation data or the database, politely decline."
    ),
)

@agent.tool
async def get_db_schema(ctx: RunContext[Deps]) -> str:
    """Get the database schema including tables and columns."""
    schema = await get_database_schema(ctx.deps.db)
    schema_str = "Database Schema:\n"
    for table in schema.tables:
        schema_str += f"- Table: {table.name}\n"
        for col in table.columns:
            schema_str += f"  - {col.name} ({col.type}, nullable={col.nullable})\n"
    return schema_str

@agent.tool
async def execute_sql(ctx: RunContext[Deps], query: str) -> str:
    """Execute a read-only SQL query and return the results as a string."""
    # Strict check for read-only
    clean_query = query.strip().upper()
    if not clean_query.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed for safety reasons."
    
    # Check for forbidden keywords
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE"]
    for word in forbidden:
        if re.search(rf"\b{word}\b", clean_query):
            return f"Error: Forbidden keyword '{word}' detected in query."

    try:
        result = await ctx.deps.db.execute(text(query))
        rows = result.fetchall()
        if not rows:
            return "No results found."
        
        # Format results as a string
        columns = result.keys()
        output = [", ".join(map(str, columns))]
        for row in rows:
            output.append(", ".join(map(str, row)))
        
        return "\n".join(output)
    except Exception as e:
        return f"Database Error: {str(e)}"
