from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import TelegramObject
from src.database.models import ChatLang

from src.utils.input_formats import validate_lang_code


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
                       ) -> Any:
        session: AsyncSession = data.get('session')

        # Получаем chat_id отправителя
        chat_id = None

        # Проверяем, есть ли сообщение или callback в обновлении
        if event.message and event.message.from_user:
            chat_id = event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            chat_id = event.callback_query.from_user.id

        # Если chat_id все еще не найден
        if chat_id is None:
            return await handler(event, data)

        # Запрашиваем язык пользователя из БД
        async with session.begin():
            result = await session.execute(
                select(ChatLang).where(ChatLang.chat_id == chat_id)
            )
            user = result.scalars().one_or_none()
            if user:
                if user.blocked:
                    return None
                # Добавляем lang в data, если пользователь найден
                try:
                    data['lang'] = validate_lang_code(user.lang)
                except ValueError:
                    data['lang'] = 'ru'
            else:
                data['lang'] = 'ru'  # Или устанавливаем значение по умолчанию

        return await handler(event, data)
