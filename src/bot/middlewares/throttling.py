import logging
from datetime import datetime, timedelta
import pytz
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from src.services.settings import settings
from src.bot.filters.manage_access import get_stand_chat_ids


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        super().__init__()
        self._storage = storage
        self._timezone = pytz.timezone('Europe/Moscow')

    async def __call__(self, handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
                       update: Update,
                       data: Dict[str, Any]) -> Any:
        user_id = None

        if hasattr(update, 'message') and update.message and hasattr(update.message, 'from_user'):
            user_id = str(update.message.from_user.id)
        elif hasattr(update, 'callback_query') and update.callback_query and hasattr(update.callback_query,
                                                                                     'from_user'):
            user_id = str(update.callback_query.from_user.id)

        if user_id is None:
            logging.warning("Не удалось получить user_id из входных данных.")
            try:
                # Отправляем сообщение пользователю, если возможно
                if hasattr(update, 'message') and update.message:
                    await update.message.answer("Произошла ошибка с идентификацией вашего ID. "
                                                "Пожалуйста, попробуйте снова.")
                elif hasattr(update, 'callback_query') and update.callback_query:
                    await update.callback_query.answer("Произошла ошибка с идентификацией вашего ID. "
                                                       "Пожалуйста, попробуйте снова.")
            except Exception as ex:
                logging.error(f"Не удалось отправить пользователю сообщение: {ex}")
            finally:
                return None

        # Не применяем спам машину если это стойка
        if int(user_id) in get_stand_chat_ids():
            return await handler(update, data)

        now = datetime.now(self._timezone)

        # Проверяем, находится ли пользователь в состоянии блокировки
        blocked_until_timestamp = await self._storage.redis.get(f"blocked:{user_id}")
        if blocked_until_timestamp:
            blocked_until = datetime.fromtimestamp(float(blocked_until_timestamp), tz=self._timezone)
            if now < blocked_until:
                # Пользователь все еще заблокирован
                if hasattr(update, 'message') and update.message:
                    await update.message.answer(
                        f"Мы обнаружили подозрительную активность. Попробуйте снова после "
                        f"{blocked_until.strftime('%H:%M:%S')}."
                    )
                elif hasattr(update, 'callback_query') and update.callback_query:
                    await update.callback_query.answer(
                        f"Мы обнаружили подозрительную активность. Попробуйте снова после "
                        f"{blocked_until.strftime('%H:%M:%S')}."
                    )
                return None

        # Проверяем количество запросов пользователя
        user_requests_count = await self._storage.redis.get(f"requests:{user_id}")

        if user_requests_count is not None:
            if int(user_requests_count) >= int(settings.redis.get('max_requests')):
                # Устанавливаем время блокировки
                block_duration = timedelta(seconds=int(settings.redis.get('ignore_time')))
                blocked_until = now + block_duration

                # Сохраняем время блокировки в Redis
                await self._storage.redis.set(
                    f"blocked:{user_id}",
                    blocked_until.timestamp(),
                    ex=int(block_duration.total_seconds())
                )

                # Отправляем сообщение пользователю
                if hasattr(update, 'message') and update.message:
                    await update.message.answer(
                        f"Мы обнаружили подозрительную активность. Попробуйте снова после "
                        f"{blocked_until.strftime('%H:%M:%S')}."
                    )
                elif hasattr(update, 'callback_query') and update.callback_query:
                    await update.callback_query.answer(
                        f"Мы обнаружили подозрительную активность. Попробуйте снова после "
                        f"{blocked_until.strftime('%H:%M:%S')}."
                    )
                return None
            else:
                # Увеличиваем счетчик запросов
                await self._storage.redis.incr(f"requests:{user_id}")
        else:
            # Инициализируем счетчик запросов
            await self._storage.redis.set(f"requests:{user_id}", 1, ex=10)

        return await handler(update, data)
