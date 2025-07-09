from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import VehicleInfo
from src.database.scripts.orders import get_scalar_subquery


async def add_vehicle_info(session: AsyncSession, data: dict):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)

        query_select = select(VehicleInfo).where(
            VehicleInfo.worker_id == scalar_subquery,
            VehicleInfo.vehicle_number == data["vehicle_number"],
            VehicleInfo.has_trailer == bool(data["trailer"]),
            VehicleInfo.trailer_number == data["trailer_number"],
            VehicleInfo.trailer_weight == bool(data["trailer_weight"]),
            VehicleInfo.key == ""
        )
        result = await session.execute(query_select)
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


async def update_vehicle_info_key(session: AsyncSession, data: dict, key: str):
    async with session.begin():
        scalar_subquery = await get_scalar_subquery(data)

        query = update(VehicleInfo).where(
            VehicleInfo.worker_id == scalar_subquery,
            VehicleInfo.vehicle_number == data["vehicle_number"],
            VehicleInfo.has_trailer == bool(data["trailer"]),
            VehicleInfo.trailer_number == data["trailer_number"],
            VehicleInfo.trailer_weight == bool(data["trailer_weight"]),
            VehicleInfo.key == ""
        ).values(key=key)
        await session.execute(query)
        await session.commit()


async def delete_vehicle_info_by_key(session: AsyncSession, key: str):
    async with session.begin():
        query = delete(VehicleInfo).where(VehicleInfo.key == key)
        result = await session.execute(query)
        deleted_count = result.rowcount
        await session.commit()

        return deleted_count


async def vehicle_info_check_existing_key(session: AsyncSession, key: str):
    async with session.begin():
        query = await session.execute(select(VehicleInfo.vehicle_number).where(VehicleInfo.key == key))
        result = query.scalars().one_or_none()

        if result:
            return True
        else:
            return False


async def select_vehicle_info_by_worker_id(session: AsyncSession, worker_id):
    async with session.begin():
        result = await session.execute(
            select(VehicleInfo).where(
                VehicleInfo.worker_id == int(worker_id)
            )
        )
        vehicle_info = result.scalar()

        if vehicle_info:
            return vehicle_info
        else:
            raise Exception(f"Пользователя нет в базе данных. "
                            f"Запрос select_vehicle_info_by_worker_id c параметром: {worker_id}")


async def select_vehicle_info_by_key(session: AsyncSession, key):
    async with session.begin():
        result = await session.execute(
            select(VehicleInfo).where(
                VehicleInfo.key == key
            )
        )
        vehicle_info = result.scalar()

        if vehicle_info:
            return vehicle_info
        else:
            raise Exception(f"Нет записи в базе данных. "
                            f"Запрос select_vehicle_info_by_worker_id c параметром: {key}")
