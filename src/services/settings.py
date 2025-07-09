import os
import json
import logging
from typing import Dict, List


class Settings:
    _instance = None
    _configs = {}  # Словарь для хранения всех конфигураций

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        """
        Загружает все JSON-файлы из папки config.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        config_dir = os.path.join(project_root, "config")

        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Папка конфигурации {config_dir} не найдена.")

        for file_name in os.listdir(config_dir):
            if file_name.endswith(".json"):
                config_name = file_name[:-5]  # Убираем расширение .json
                with open(os.path.join(config_dir, file_name), "r", encoding="utf-8") as f:
                    self._configs[config_name] = json.load(f)
                    logging.info(f"Конфиг {config_name} успешно загружен.")

    def _save_config(self, config_name: str):
        """
        Сохраняет изменения в конфигурационный файл.
        :param config_name: Имя конфига.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        config_dir = os.path.join(project_root, "config")
        config_file = os.path.join(config_dir, f"{config_name}.json")

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self._configs[config_name], f, ensure_ascii=False, indent=4)
            logging.info(f"Конфиг {config_name} успешно сохранен.")

    def _get_config(self, config_name: str) -> Dict:
        """
        Возвращает конфигурацию по имени.
        :param config_name: Имя конфигурации.
        :return: Словарь с настройками.
        """
        if config_name not in self._configs:
            raise KeyError(f"Конфигурация {config_name} не найдена.")
        return self._configs[config_name]

    def _get_value(self, config_name: str, key: str) -> str:
        """
        Возвращает значение параметра из указанной конфигурации.
        :param config_name: Имя конфигурации.
        :param key: Ключ параметра.
        :return: Значение параметра.
        """
        config = self._get_config(config_name)
        return str(config.get(key))

    @property
    def bot(self) -> dict:
        return self._get_config("bot")

    @bot.setter
    def bot(self, value: dict):
        self._configs["bot"] = value
        self._save_config("bot")

    @property
    def admin(self) -> dict:
        return self._get_config("admin")

    @admin.setter
    def admin(self, value: dict):
        self._configs["admin"] = value
        self._save_config("admin")

    @property
    def main_admin(self) -> int:
        return int(self.admin.get("main_admin", 0))

    @property
    def admins(self) -> List[int]:
        return [int(admin) for admin in self.admin.get("admins", []) if admin.isdigit()]

    @property
    def managers(self) -> List[int]:
        return [int(manager) for manager in self.admin.get("managers", []) if manager.isdigit()]

    @property
    def stands(self) -> List[int]:
        return [int(stand) for stand in self.bot.get("stand_chat_ids", []) if stand.isdigit()]

    @property
    def api(self) -> dict:
        return self._get_config("api")

    @property
    def app(self) -> dict:
        return self._get_config("app")

    @property
    def google_sheet(self) -> dict:
        return self._get_config("google_sheet")

    @property
    def pg(self) -> dict:
        return self._get_config("pg")

    @property
    def redis(self) -> dict:
        return self._get_config("redis")

    def get_db_url(self) -> str:
        """
        Возвращает ссылку на БД postgres
        :return: Формат ссылки для создания переменной engine = sqlalchemy.ext.asyncio.create_async_engine
        """
        return (f"{self.pg.get('pg_url')}://{self.pg.get('pg_user')}:{self.pg.get('pg_password')}@"
                f"{self.pg.get('pg_host')}:{self.pg.get('pg_port')}/{self.pg.get('pg_db')}")

    def get_redis_url(self, key: str) -> str:
        """
        Возвращает ссылку на БД redis
        :param key: Номер порта redis хранящийся в конфиге под названием storage_base или throttling_base.
        :return: Формат ссылки для создания переменной RedisStorage.from_url
        """
        return f"redis://{self.redis.get('host')}:{self.redis.get('port')}/{self._get_value('redis', key)}"

    def add_stand(self, user_id: str):
        try:
            if "stand_chat_ids" not in self.bot or not isinstance(self.bot["stand_chat_ids"], list):
                self.bot["stand_chat_ids"] = []
            if user_id not in self.bot["stand_chat_ids"]:
                self.bot["stand_chat_ids"].append(user_id)
                # Явно вызываем setter для сохранения изменений
                self.bot = self.bot
                logging.info(f"Стойка с ID {user_id} успешно добавлена.")
        except Exception as ex:
            logging.error(f"Ошибка при добавлении стойки: {ex}")

    def remove_stand(self, user_id: str):
        try:
            if "stand_chat_ids" in self.bot and isinstance(self.bot["stand_chat_ids"], list):
                if user_id in self.bot["stand_chat_ids"]:
                    self.bot["stand_chat_ids"].remove(user_id)
                    # Явно вызываем setter для сохранения изменений
                    self.bot = self.bot
                    logging.info(f"Стойка с ID {user_id} успешно удалена.")
        except Exception as ex:
            logging.error(f"Ошибка при удалении стойки: {ex}")

    def add_admin(self, user_id: str):
        try:
            if "admins" not in self.admin or not isinstance(self.admin["admins"], list):
                self.admin["admins"] = []

            if user_id not in self.admin["admins"]:
                self.admin["admins"].append(user_id)
                # Явно вызываем setter для сохранения изменений
                self.admin = self.admin
                logging.info(f"Админ с ID {user_id} успешно добавлен.")
        except Exception as ex:
            logging.error(f"Ошибка при добавлении админа: {ex}")

    def remove_admin(self, user_id: str):
        try:
            if "admins" in self.admin and isinstance(self.admin["admins"], list):
                if user_id in self.admin["admins"]:
                    self.admin["admins"].remove(user_id)
                    # Явно вызываем setter для сохранения изменений
                    self.admin = self.admin
                    logging.info(f"Админ с ID {user_id} успешно удален.")
        except Exception as ex:
            logging.error(f"Ошибка при удалении админа: {ex}")

    def add_manager(self, user_id: str):
        try:
            if "managers" not in self.admin or not isinstance(self.admin["managers"], list):
                self.admin["managers"] = []

            if user_id not in self.admin["managers"]:
                self.admin["managers"].append(user_id)
                # Явно вызываем setter для сохранения изменений
                self.admin = self.admin
                logging.info(f"Менеджер с ID {user_id} успешно добавлен.")
        except Exception as ex:
            logging.error(f"Ошибка при добавлении менеджера: {ex}")

    def remove_manager(self, user_id: str):
        try:
            if "managers" in self.admin and isinstance(self.admin["managers"], list):
                if user_id in self.admin["managers"]:
                    self.admin["managers"].remove(user_id)
                    # Явно вызываем setter для сохранения изменений
                    self.admin = self.admin
                    logging.info(f"Менеджер с ID {user_id} успешно удален.")
        except Exception as ex:
            logging.error(f"Ошибка при удалении менеджера: {ex}")


settings = Settings()
