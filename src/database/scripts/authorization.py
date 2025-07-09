from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Registration


async def get_user(session: AsyncSession, data: dict):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == data['licence_series'],
                Registration.licence_number == data['licence_number']
            )
        )
        user = result.scalars().one_or_none()
        return user if user else None


async def get_user_by_id(session: AsyncSession, worker_id):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.id == worker_id
            )
        )
        user = result.scalars().one_or_none()
        return user if user else None
