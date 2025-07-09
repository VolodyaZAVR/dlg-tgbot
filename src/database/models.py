from typing import Annotated
from sqlalchemy import String, BigInteger, DateTime, func, ForeignKey, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import true


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class ChatLang(Base):
    __tablename__ = 'user_lang'
    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(BigInteger(), unique=True, nullable=False)
    lang: Mapped[str] = mapped_column(String(2), nullable=False)
    blocked: Mapped[bool] = mapped_column(Boolean(), nullable=False)


class Registration(Base):
    __tablename__ = 'registration'
    id: Mapped[intpk]
    chat_id: Mapped[str] = mapped_column(String(50), nullable=False)
    accept_user_agree: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=False)
    number: Mapped[str] = mapped_column(String(15), nullable=False)
    licence_series: Mapped[str] = mapped_column(String(4))
    licence_number: Mapped[str] = mapped_column(String(9), nullable=False)


class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey("registration.id", ondelete="CASCADE"))
    contact_point: Mapped[str] = mapped_column(String(50), nullable=False)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)
    use_orders: Mapped[bool] = mapped_column(Boolean(), nullable=False, server_default=true())
    order: Mapped[str] = mapped_column(String(60), nullable=False)
    partner: Mapped[str] = mapped_column(String(50), nullable=False)
    key: Mapped[str] = mapped_column(String(6), nullable=False)
    row_number: Mapped[int] = mapped_column(Integer(), nullable=True)


class VehicleInfo(Base):
    __tablename__ = 'vehicle_info'
    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey("registration.id", ondelete="CASCADE"))
    vehicle_number: Mapped[str] = mapped_column(String(10), nullable=False)
    has_trailer: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    trailer_number: Mapped[str] = mapped_column(String(10))
    trailer_weight: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    key: Mapped[str] = mapped_column(String(6), nullable=False)
