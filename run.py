import asyncio
import logging
from contextlib import suppress
import uvicorn
from src.bot.bot import main as bot_main
from src.api_v1.app import app as fastapi_app
import os
from pytz import timezone
from datetime import datetime


def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Форматтер для всех логгеров
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Устанавливаем московское время через pytz
    moscow_tz = timezone('Europe/Moscow')
    logging.Formatter.converter = lambda *args: datetime.now(moscow_tz).timetuple()

    # Удаляем существующие обработчики в корневом логере
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Настройка корневого логгера (root_log.log)
    root_log_file = os.path.join(log_dir, "root_log.log")
    root_handler = logging.FileHandler(root_log_file, mode="a", encoding="utf-8")
    root_handler.setFormatter(formatter)
    root_logger.addHandler(root_handler)

    # Настройка логирования бота (bot.log)
    bot_log_file = os.path.join(log_dir, "bot.log")
    bot_handler = logging.FileHandler(bot_log_file, mode="a", encoding="utf-8")
    bot_handler.setFormatter(formatter)
    bot_logger = logging.getLogger("bot")
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.addHandler(bot_handler)
    # bot_logger.propagate = False # Отключаем распространение в корневой логгер

    # Настройка логирования бэкенда (fastapi.log)
    fastapi_log_file = os.path.join(log_dir, "fastapi.log")
    fastapi_handler = logging.FileHandler(fastapi_log_file, mode="a", encoding="utf-8")
    fastapi_handler.setFormatter(formatter)
    fastapi_logger = logging.getLogger("backend")
    fastapi_logger.setLevel(logging.DEBUG)
    fastapi_logger.addHandler(fastapi_handler)
    # fastapi_logger.propagate = False # Отключаем распространение в корневой логгер

    # Настройка логирования базы данных (db.log)
    db_log_file = os.path.join(log_dir, "db.log")
    db_handler = logging.FileHandler(db_log_file, mode="a", encoding="utf-8")
    db_handler.setFormatter(formatter)
    db_logger = logging.getLogger("database")
    db_logger.setLevel(logging.DEBUG)
    db_logger.addHandler(db_handler)
    # db_logger.propagate = False # Отключаем распространение в корневой логгер


async def run_fastapi(reload=False):
    config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=reload  # Включаем только для разработки
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_bot():
    try:
        await bot_main()
    except Exception as ex:
        logging.error(f"Bot caught an exception: {ex}", exc_info=True)


async def main():
    setup_logging()
    logging.info("Starting FastAPI and Telegram bot...")

    # Запускаем FastAPI и бота параллельно
    fastapi_task = asyncio.create_task(run_fastapi(True))
    bot_task = asyncio.create_task(run_bot())

    # Ждём завершения любой из задач
    await asyncio.gather(fastapi_task, bot_task)

if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
