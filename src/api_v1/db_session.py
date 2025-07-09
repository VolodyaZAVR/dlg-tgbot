from sqlalchemy.ext.asyncio import AsyncSession
from src.database.engine import session_maker


async def get_db_session() -> AsyncSession:
    async with session_maker() as session:
        yield session
