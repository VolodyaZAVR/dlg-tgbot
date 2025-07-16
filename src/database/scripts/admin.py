from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from src.database.models import Registration, Orders, ChatLang, VehicleInfo
from src.database.scripts.orders import get_scalar_subquery
from src.bot.translations.registration import get_user_already_reg_text


async def select_users_by_id(session: AsyncSession, driver_id):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.id == driver_id
            )
        )
        return result.fetchall() if result else None


async def select_users_by_surname(session: AsyncSession, surname):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.surname == surname
            )
        )
        return result.fetchall() if result else None


async def select_users_by_licence(session: AsyncSession, series, number):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == series,
                Registration.licence_number == number
            )
        )
        return result.fetchall() if result else None


async def search_fast_reg_user(session: AsyncSession, series, number):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == series,
                Registration.licence_number == number
            )
        )
        return result.first() if result else None


async def search_user_status(session: AsyncSession, user_id):
    async with session.begin():
        query = await session.execute(
            select(ChatLang).where(
                ChatLang.chat_id == int(user_id)
            )
        )
        result = query.scalar()
        return result.blocked if result else None


async def update_user_status(session: AsyncSession, user_id, status):
    async with session.begin():
        await session.execute(
            update(ChatLang).where(
                ChatLang.chat_id == int(user_id)
            ).values(blocked=status)
        )
        await session.commit()


async def update_user_name(session: AsyncSession, series, number, name):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == series,
            Registration.licence_number == number
        ).values(name=name)
        await session.execute(query)
        await session.commit()


async def update_user_surname(session: AsyncSession, series, number, surname):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == series,
            Registration.licence_number == number
        ).values(surname=surname)
        await session.execute(query)
        await session.commit()


async def update_user_middle_name(session: AsyncSession, series, number, middle_name):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == series,
            Registration.licence_number == number
        ).values(middle_name=middle_name)
        await session.execute(query)
        await session.commit()


async def update_user_number(session: AsyncSession, series, number, new_number):
    async with session.begin():
        query = update(Registration).where(
            Registration.licence_series == series,
            Registration.licence_number == number
        ).values(number=new_number)
        await session.execute(query)
        await session.commit()


async def delete_user_from_db(session: AsyncSession, series, number):
    async with session.begin():
        query = delete(Registration).where(
            Registration.licence_series == series,
            Registration.licence_number == number
        )
        result = await session.execute(query)
        deleted_count = result.rowcount
        await session.commit()
        return deleted_count


async def select_orders(session: AsyncSession, order):
    async with session.begin():
        result = await session.execute(
            select(Orders).where(
                Orders.order == order
            )
        )
        return result.fetchall() if result else None


async def select_orders_by_key(session: AsyncSession, key):
    async with session.begin():
        result = await session.execute(
            select(Orders).where(
                Orders.key == key
            )
        )
        return result.fetchall() if result else None


async def select_vehicle_by_key(session: AsyncSession, key):
    async with session.begin():
        result = await session.execute(
            select(VehicleInfo).where(
                VehicleInfo.key == key
            )
        )
        return result.fetchall() if result else None


async def select_orders_by_driver(session: AsyncSession, worker_id):
    async with session.begin():
        result = await session.execute(
            select(Orders).where(
                Orders.worker_id == worker_id
            )
        )
        return result.fetchall() if result else None


async def delete_order_from_db(session: AsyncSession, order_id):
    async with session.begin():
        query = delete(Orders).where(
            Orders.id == order_id
        )
        result = await session.execute(query)
        deleted_count = result.rowcount
        await session.commit()
        return deleted_count


async def order_reset_key(session: AsyncSession, key):
    async with session.begin():
        query = await session.execute(
            select(Orders).where(
                Orders.key == key
            )
        )
        result = query.scalar()
        if result:
            query = update(Orders).where(
                Orders.key == key
            ).values(key="")
            await session.execute(query)
            await session.commit()
            return result
        else:
            return None


async def vehicle_reset_key(session: AsyncSession, key):
    async with session.begin():
        query = await session.execute(
            select(VehicleInfo).where(
                VehicleInfo.key == key
            )
        )
        result = query.scalar()
        if result:
            query = update(VehicleInfo).where(
                VehicleInfo.key == key
            ).values(key="")
            await session.execute(query)
            await session.commit()
            return result
        else:
            return None


async def add_user(session: AsyncSession, msg: Message, data: dict):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == data["licence_series"],
                Registration.licence_number == data["licence_number"]
            )
        )
        user = result.scalars().one_or_none()

        if user:
            await msg.answer(text=get_user_already_reg_text("ru"))
            raise Exception(f"Попытка повторной регистрации. Запрос reg_user с параметрами: "
                            f"{data['licence_series']} и {data['licence_number']}")
        else:
            obj = Registration(
                chat_id=str(msg.from_user.id),
                accept_user_agree=True,
                name=data["name"],
                surname=data["surname"],
                middle_name=data["middle_name"],
                number=data["number"],
                licence_series=data["licence_series"],
                licence_number=data["licence_number"]
            )
            session.add(obj)
            await session.commit()


async def add_fast_reg_user(session: AsyncSession, msg: Message, name, surname, middle_name, number, licence_series,
                            licence_number):
    async with session.begin():
        result = await session.execute(
            select(Registration).where(
                Registration.licence_series == licence_series,
                Registration.licence_number == licence_number
            )
        )
        user = result.scalars().one_or_none()

        if user:
            await msg.answer(text=get_user_already_reg_text("ru"))
            raise Exception(f"Попытка повторной регистрации. Запрос reg_user с параметрами: "
                            f"{licence_series} и {licence_number}")
        else:
            obj = Registration(
                chat_id=str(msg.from_user.id),
                accept_user_agree=True,
                name=name,
                surname=surname,
                middle_name=middle_name,
                number=number,
                licence_series=licence_series,
                licence_number=licence_number
            )
            session.add(obj)
            await session.commit()


async def check_vehicle_existing(session: AsyncSession, data: dict, scalar_subquery):
    query_select = select(VehicleInfo).where(
        VehicleInfo.worker_id == scalar_subquery,
        VehicleInfo.vehicle_number == data["vehicle_number"],
        VehicleInfo.has_trailer == bool(data["trailer"]),
        VehicleInfo.trailer_number == data["trailer_number"],
        VehicleInfo.trailer_weight == bool(data["trailer_weight"]),
        VehicleInfo.key == ""
    )
    return await session.execute(query_select)


async def add_fast_reg_vehicle(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)

        result = await check_vehicle_existing(session, data, scalar_subquery)
        if not result.fetchall():
            query = insert(VehicleInfo).values(
                worker_id=scalar_subquery,
                vehicle_number=data["vehicle_number"],
                has_trailer=bool(data["trailer"]),
                trailer_number=data["trailer_number"],
                trailer_weight=bool(data["trailer_weight"]),
                key=""
            )
            await session.execute(query)
            await session.commit()


async def remove_fast_reg_vehicle(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)
        result = await check_vehicle_existing(session, data, scalar_subquery)
        if result.one_or_none():
            query = delete(VehicleInfo).where(
                VehicleInfo.worker_id == scalar_subquery,
                VehicleInfo.vehicle_number == data["vehicle_number"],
                VehicleInfo.has_trailer == bool(data["trailer"]),
                VehicleInfo.trailer_number == data["trailer_number"],
                VehicleInfo.trailer_weight == bool(data["trailer_weight"]),
                VehicleInfo.key == ""
            )
            await session.execute(query)
            await session.commit()


async def update_orders_key_admin(session: AsyncSession, data: dict, key: str):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)
        for order in data["orders"]:
            query = update(Orders).where(
                Orders.worker_id == scalar_subquery,
                Orders.contact_point == data["contact_point"],
                Orders.job_type == data["job_type"],
                Orders.order == order["Number"],
                Orders.partner == data["partner"],
                Orders.use_orders == data["use_orders"],
                Orders.key == ""
            ).values(key=key)
            await session.execute(query)
        await session.commit()
