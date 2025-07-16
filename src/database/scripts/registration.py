from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery
from src.database.models import Registration

from src.bot.translations.registration import get_user_already_reg_text


async def reg_user(session: AsyncSession, call: CallbackQuery, data: dict, lang: str):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == data["licence_series"],
                Registration.licence_number == data["licence_number"]
            )
        )
        user = result.scalars().one_or_none()

        if user:
            await call.message.answer(text=get_user_already_reg_text(lang))
            raise Exception(f"Попытка повторной регистрации. Запрос reg_user с параметрами: "
                            f"{data['licence_series']} и {data['licence_number']}")
        else:
            obj = Registration(
                chat_id=str(call.from_user.id),
                accept_user_agree=bool(data["user_agree"]),
                name=data["name"],
                surname=data["surname"],
                middle_name=data["middle_name"],
                number=data["number"],
                licence_series=data["licence_series"],
                licence_number=data["licence_number"]
            )
            session.add(obj)
            await session.commit()


async def update_name(session: AsyncSession, data: dict):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == data['licence_series'],
            Registration.licence_number == data['licence_number']
        ).values(name=data['edit_name'])
        await session.execute(query)
        await session.commit()


async def update_surname(session: AsyncSession, data: dict):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == data['licence_series'],
            Registration.licence_number == data['licence_number']
        ).values(surname=data['edit_surname'])
        await session.execute(query)
        await session.commit()


async def update_middle_name(session: AsyncSession, data: dict):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == data['licence_series'],
            Registration.licence_number == data['licence_number']
        ).values(middle_name=data['edit_middle_name'])
        await session.execute(query)
        await session.commit()


async def update_number(session: AsyncSession, data: dict):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == data['licence_series'],
            Registration.licence_number == data['licence_number']
        ).values(number=data['edit_number'])
        await session.execute(query)
        await session.commit()