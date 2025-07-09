import os
import asyncio
import contextlib
import logging
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault, CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from src.services.settings import settings
from src.database.engine import drop_tables, create_tables, session_maker
from src.bot.handlers import common, admin, vehicle_info, orders, qr_code, registration, authorization, menu, manager
from src.bot.middlewares.throttling import ThrottlingMiddleware
from src.bot.middlewares.db import DataBaseSession
from src.bot.middlewares.lang import LanguageMiddleware
from src.alembic.migrations import apply_migrations
from src.bot.keyboards.common import start_kb


bot = Bot(
    token=settings.bot.get('token'),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

logger = logging.getLogger("bot")

storage = RedisStorage.from_url(settings.get_redis_url('storage_base'))
throttling_storage = RedisStorage.from_url(settings.get_redis_url('throttling_base'))

dp = Dispatcher(storage=storage)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='user_agree',
            description='Пользовательское соглашение'
        ),
        BotCommand(
            command='change_lang',
            description='Сменить язык'
        ),
        BotCommand(
            command='menu',
            description='Главное меню'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup(bot, initialize: bool = False):
    if initialize:
        await drop_tables()

    await set_commands(bot)
    await create_tables()
    await apply_migrations()
    await bot.send_message(chat_id=settings.main_admin, text='Бот запущен!')


async def on_shutdown(bot):
    await bot.send_message(chat_id=settings.main_admin, text='Бот остановлен.')


# clear history command handlers
@dp.callback_query(F.data == "clear")
async def handle_clear_messages(call: CallbackQuery):
    chat_id = call.from_user.id
    try:
        for i in range(call.message.message_id, 0, -1):
            await bot.delete_message(chat_id=chat_id, message_id=i)
    except TelegramBadRequest as ex:
        if ex.message == "Telegram server says - Bad Request: message to delete not found!":
            logger.info(f"Попытка удалить сообщения которого нет: {ex}")
        else:
            logger.warning(f"Unexpected error in deleting message algorithm: {ex}")
    finally:
        await call.message.answer(text="Для начала работы нажмите на кнопку ниже 👇", reply_markup=start_kb())


@dp.message(F.text.lower() == "завершить работу")
async def cmd_clear_messages(msg: Message):
    chat_id = msg.from_user.id
    try:
        for i in range(msg.message_id, 0, -1):
            await bot.delete_message(chat_id=chat_id, message_id=i)
    except TelegramBadRequest as ex:
        if ex.message == "Telegram server says - Bad Request: message to delete not found!":
            logger.info(f"Попытка удалить сообщения которого нет: {ex}")
        else:
            logger.warning(f"Unexpected error in deleting message algorithm: {ex}")
    finally:
        await msg.answer(text="Для начала работы нажмите на кнопку ниже 👇", reply_markup=start_kb())


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware.register(ThrottlingMiddleware(storage=throttling_storage))
    dp.update.middleware.register(DataBaseSession(session_pool=session_maker))
    dp.update.middleware.register(LanguageMiddleware())

    dp.include_routers(menu.router, authorization.router, registration.router, orders.router, vehicle_info.router,
                       qr_code.router, admin.admin_router, manager.manager_router, common.router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(f"Catch an exception: {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    # TODO: Разделить вывод между основным логом и логом базы данных
    os.makedirs(settings.bot.get("log_dir"), exist_ok=True)

    main_log_file = os.path.join(str(settings.bot.get("log_dir")), str(settings.bot.get("log_filename")))

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone(timedelta(hours=3))).timetuple()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    file_handler = logging.FileHandler(main_log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
