from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Registration, Orders, VehicleInfo


async def outer_reg_add_user(session: AsyncSession, data: dict):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == data.get('licence_series'),
                Registration.licence_number == data.get('licence_number')
            )
        )
        user = result.scalars().one_or_none()

        if user:
            return False
        else:
            obj = Registration(
                chat_id="Внешняя регистрация",
                accept_user_agree=True,
                name=data.get('name'),
                surname=data.get('surname'),
                middle_name=data.get('middle_name'),
                number=data.get('number'),
                licence_series=data.get('licence_series'),
                licence_number=data.get('licence_number')
            )
            session.add(obj)
            await session.commit()
            return True


async def outer_reg_delete_user(session: AsyncSession, data: dict):
    async with session.begin():
        query = delete(Registration).where(
            Registration.licence_series == data.get('licence_series'),
            Registration.licence_number == data.get('licence_number')
        )
        result = await session.execute(query)
        deleted_count = result.rowcount
        await session.commit()
        return deleted_count
