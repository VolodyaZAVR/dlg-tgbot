from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery

from src.database.models import ChatLang
from src.utils.input_formats import validate_lang_code
from aiogram.types import TelegramObject


async def get_user_lang(session: AsyncSession, event: TelegramObject) -> str:
    chat_id = event.from_user.id

    async with session.begin():
        # Проверяем, существует ли пользователь
        result = await session.execute(
            select(ChatLang).where(ChatLang.chat_id == chat_id)
        )
        user = result.scalars().one_or_none()

        if user is None:
            # Если пользователя нет, создаем его с языком по умолчанию
            user_lang = 'ru'
            new_user = ChatLang(chat_id=chat_id, lang=user_lang, blocked=False)  # Устанавливаем язык 'ru'
            session.add(new_user)
            await session.commit()
            return user_lang
        else:
            # Если пользователь существует, просто сообщаем его язык
            return validate_lang_code(user.lang)


async def set_user_lang(call: CallbackQuery, session: AsyncSession) -> str:
    chat_id = call.from_user.id
    lang_code = call.data.split('_')[1]
    async with session.begin():
        # Обновляем язык пользователя в базе данных
        await session.execute(
            update(ChatLang)
            .where(ChatLang.chat_id == chat_id)
            .values(lang=validate_lang_code(lang_code))
        )
        await session.commit()
        return lang_code
