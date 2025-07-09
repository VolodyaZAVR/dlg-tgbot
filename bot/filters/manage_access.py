import logging
from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from src.services.settings import settings

logger = logging.getLogger("bot")


class IsAdmin(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user_id = None

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        if user_id is None:
            logger.warning("Not found user ID.")
            return False

        return int(user_id) in settings.admins


class IsManager(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user_id = None

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        if user_id is None:
            logger.warning("Not found user ID.")
            return False

        return int(user_id) in settings.managers


class IsStandUser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IsStandUser, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_stand_chat_ids() -> list:
        """
        Возвращает список ID чатов для стендов из конфига.
        Если список пустой или не задан, выбрасывает исключение.
        """
        stand_chat_ids = settings.stands

        if stand_chat_ids is None or len(stand_chat_ids) == 0:
            raise ValueError("Ошибка развертки стендов. В конфиге не указаны номера id чатов для стендов.")

        # Преобразуем все ID к целочисленному типу
        try:
            stand_chat_ids = [int(chat_id) for chat_id in stand_chat_ids]
        except (ValueError, TypeError) as e:
            logger.error(f"Ошибка преобразования ID чатов в целые числа: {e}")
            raise ValueError("Некорректные ID чатов в конфиге.") from e

        return stand_chat_ids

    def __call__(self, user_id: int) -> bool:
        """
        Проверяет, является ли пользователь участником стендов.
        Возвращает True, если user_id находится в списке ID чатов для стендов.
        """
        try:
            stand_chat_ids = self.get_stand_chat_ids()
        except ValueError as e:
            logger.error(f"Ошибка при получении списка ID чатов: {e}")
            return False

        return user_id in stand_chat_ids


is_stand_user = IsStandUser()


def get_stand_chat_ids() -> list:
    stand_chat_ids = settings.stands
    # Проверяем список на пустоту
    if stand_chat_ids is None:
        raise Exception("Ошибка развертки стендов. В конфиге не указаны номера id чатов для стендов.")
    else:
        # Возвращаем список id чатов
        return stand_chat_ids
