import os
import subprocess
from pathlib import Path
from src.services.settings import settings


async def apply_migrations():
    alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"

    try:
        # Генерация миграции
        subprocess.run(
            ["alembic", "-c", str(alembic_ini_path), "revision", "--autogenerate", "-m", "Auto migration"],
            check=True,
            env={**os.environ, "env_db_url": settings.get_db_url()},  # Передача URL базы данных
        )

        # Применение миграции
        subprocess.run(
            ["alembic", "-c", str(alembic_ini_path), "upgrade", "head"],
            check=True,
            env={**os.environ, "env_db_url": settings.get_db_url()},  # Передача URL базы данных
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении миграций: {e}")
