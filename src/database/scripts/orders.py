import logging
from typing import Optional

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Registration, Orders

logger = logging.getLogger("database")


async def get_scalar_subquery(data: dict):
    return select(Registration.id).where(
        Registration.licence_series == data["licence_series"],
        Registration.licence_number == data["licence_number"]
    ).scalar_subquery()


async def get_row_number(data: dict, order: dict) -> Optional[str]:
    try:
        row_number = order["row_number"]
        return row_number
    except Exception as ex:
        logger.error(f"Не удалось получить номер строки в гугл таблице: {ex}")
        return None


async def check_order_existing(session: AsyncSession, data: dict, order: dict, scalar_subquery):
    query_select = select(Orders.order).where(
        Orders.worker_id == scalar_subquery,
        Orders.contact_point == data["contact_point"],
        Orders.job_type == data["job_type"],
        Orders.use_orders == bool(data["use_orders"]),
        Orders.order == order["Number"],
        Orders.partner == data["partner"],
        Orders.key == "",
        Orders.row_number == await get_row_number(data, order)
    )
    return await session.execute(query_select)


async def add_fast_reg_orders(session: AsyncSession, data: dict) -> None:
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)
        for order in data["orders"]:
            selected_order = await check_order_existing(session, data, order, scalar_subquery)
            if not selected_order.fetchall():
                query = insert(Orders).values(
                    worker_id=scalar_subquery,
                    contact_point=data["contact_point"],
                    job_type=data["job_type"],
                    use_orders=bool(data["use_orders"]),
                    order=order["Number"],
                    partner=data["partner"],
                    key="",
                    row_number=await get_row_number(data, order)
                )
                await session.execute(query)
        await session.commit()


async def remove_fast_reg_orders(session: AsyncSession, data: dict) -> None:
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)
        for order in data["orders"]:
            selected_order = await check_order_existing(session, data, order, scalar_subquery)
            if selected_order.one_or_none():
                query = delete(Orders).where(
                    Orders.worker_id == scalar_subquery,
                    Orders.contact_point == data["contact_point"],
                    Orders.job_type == data["job_type"],
                    Orders.order == order["Number"],
                    Orders.partner == data["partner"],
                    Orders.key == "",
                    Orders.row_number == await get_row_number(data, order)
                )
                await session.execute(query)
        await session.commit()


async def orders_check_key_existing(session: AsyncSession, key: str):
    async with session.begin():
        query = await session.execute(select(Orders.order).where(Orders.key == key))
        result = query.scalars().one_or_none()
        return True if result else False


async def select_worker_by_key(session: AsyncSession, key: str):
    async with session.begin():
        query = await session.execute(select(Orders.worker_id).where(Orders.key == key))
        result = query.first()
        return result[0] if result else None


async def update_orders_key(session: AsyncSession, data: dict, key: str):
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


async def delete_orders_by_key(session: AsyncSession, key: str):
    async with session.begin():
        query = delete(Orders).where(Orders.key == key)
        result = await session.execute(query)
        deleted_count = result.rowcount
        await session.commit()

        return deleted_count


async def get_any_order(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)
        result = await session.execute(
            select(Orders).where(
                Orders.worker_id == scalar_subquery,
                Orders.contact_point == data["contact_point"],
                Orders.job_type == data["job_type"],
                Orders.key == ""
            )
        )
        order = result.scalar()

        if order:
            return order
        else:
            raise Exception(f"Пользователя нет в базе данных. Запрос get_any_order с параметрами: "
                            f"{data['licence_series']} и {data['licence_number']}")


async def find_order_by_key(session: AsyncSession, key: str):
    async with session.begin():
        query = await session.execute(select(Orders).where(Orders.key == key))
        result = query.scalar()

        if result:
            return result
        else:
            return None


async def get_orders_with_key(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)

        query = select(Orders.order).where(
            Orders.worker_id == scalar_subquery,
            Orders.contact_point == data["contact_point"],
            Orders.job_type == data["job_type"],
            Orders.key == data["key"]
        )
        result = await session.execute(query)

        if result:
            return result.fetchall()
        else:
            raise Exception(f"Нет записей в базе данных. Запрос get_orders с параметрами: "
                            f"worker_id: {data['licence_series']} и {data['licence_number']},"
                            f"contact_point: {data['contact_point']}, job_type: {data['job_type']}")


async def select_orders_row_numbers_with_key(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)

        query = select(Orders.row_number).where(
            Orders.worker_id == scalar_subquery,
            Orders.contact_point == data["contact_point"],
            Orders.job_type == data["job_type"],
            Orders.key == data["key"]
        )
        result = await session.execute(query)

        if result:
            return result.fetchall()
        else:
            raise Exception(f"Нет записей в базе данных. Запрос get_orders с параметрами: "
                            f"worker_id: {data['licence_series']} и {data['licence_number']},"
                            f"contact_point: {data['contact_point']}, job_type: {data['job_type']}")
