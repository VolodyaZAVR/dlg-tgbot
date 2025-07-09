import json
import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession, BasicAuth

from src.database.scripts.authorization import get_user
from src.database.scripts.orders import get_orders_with_key
from src.services.settings import settings


class APIService:
    _instance = None

    def __new__(cls):
        """
        Singleton pattern.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dump_start_number: int = 10000000):
        """
        Инициализатор сервиса API.
        :param dump_start_number: Начальный номер дампа.
        """
        self._dump_start_number = dump_start_number
        self._url = f"http://{settings.api.get('api_ip')}:{settings.api.get('api_port')}/{settings.api.get('api_path')}"
        self._auth = BasicAuth(login=settings.api.get('api_user'), password=settings.api.get('api_password'))
        self._headers = {"Content-Type": "application/json"}

    def _get_next_dump_number(self) -> str:
        """
        Генерирует следующий номер дампа.
        :return: Строковое представление номера дампа.
        """
        self._dump_start_number += 1
        return f"{self._dump_start_number:08d}"

    async def send_orders_to_api(self, data: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        Отправляет данные о заявках на API.
        :param data: Данные для отправки.
        :return: JSON-ответ от API или None в случае ошибки.
        """
        data_dict = await self._make_orders_dict(data)
        try:
            logging.info(f"Отправляемые данные:{data_dict}\n{json.dumps(data_dict, indent=4)}.")
            async with ClientSession() as client:
                async with client.post(url=self._url, auth=self._auth, json=data_dict,
                                       headers=self._headers) as response:
                    if response.status == 200:
                        logging.info("Обмен заявок. Данные успешно получены.")
                        response_json = await response.json(content_type='text/html')
                        logging.info(f"Полученные данные:\n{response_json}.")
                        if "partners" in response_json and "payload" in response_json:
                            return response_json
                        else:
                            raise Exception("Некорректный ответ от API. Отсутствуют поля partners и payload.")
                    else:
                        raise Exception(f"\nСтатус код: {response.status}.\n"
                                        f"Ответ API: {await response.text()}")
        except Exception as ex:
            logging.error(f"Обмен заявок. Ошибка обмена с API: {ex}")
            return None

    async def _make_orders_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создаёт словарь данных о заявках для обмена.
        :param data: Данные для отправки.
        :return: Словарь нужных данных для обмена.
        """
        orders = data["orders"]
        partner = data["partner"]
        payloads = self._create_payloads(orders)
        return self._orders_dump_impl(
            dump_number=self._get_next_dump_number(),
            contact_point=data['contact_point'],
            job_type=data['job_type'],
            use_orders=data['use_orders'],
            payload=payloads,
            partners=partner
        )

    @staticmethod
    def _create_payloads(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Создаёт словарь номеров для обмена.
        :param orders: Список заявок.
        :return: Список номеров для проверки.
        """
        payloads = []
        for order in orders:
            payload = {
                "Number": order["Number"],
                "Status": None
            }
            payloads.append(payload)
        return payloads

    @staticmethod
    def _orders_dump_impl(
            dump_number: str,
            contact_point: str,
            job_type: str,
            use_orders: bool | None,
            payload: List[Dict[str, Any]],
            partners: str
    ) -> Dict[str, Any]:
        """
        Создаёт словарь данных о заявках для отправки на API.
        :param dump_number: Номер дампа.
        :param contact_point: Точка обращения.
        :param job_type: Тип обращения.
        :param use_orders: Тип отправляемых номеров. True - номера заявок, False - номера контейнеров.
        :param payload: Список заявок.
        :param partners: Информация о контрагентах.
        :return: Словарь данных.
        """
        return {
            "id": dump_number,
            "type": "Проверка",  # Устанавливается по договору обмена
            "contact_point": contact_point,
            "job_type": job_type,
            "use_orders": use_orders,
            "payload": payload,
            "partners": partners,
            "status": ""  # Не используется в текущей реализации
        }

    async def send_full_data_to_api(
            self,
            session: AsyncSession,
            data: Dict[str, Any]
    ) -> Dict[str, Any] | None:
        """
        Отправляет полные данные на API.
        :param session: Асинхронная сессия базы данных.
        :param data: Данные для отправки.
        :return: JSON-ответ от API или None в случае ошибки.
        """
        data_dict = await self._make_full_data_dict(session, data)
        try:
            logging.info(f"Отправляемые данные:{data_dict}\n{json.dumps(data_dict, indent=4)}.")
            async with ClientSession() as client:
                async with client.post(url=self._url, auth=self._auth, json=data_dict,
                                       headers=self._headers) as response:
                    if response.status == 200:
                        logging.info("Обмен полный пакет. Данные успешно получены.")
                        response_json = await response.json(content_type='text/html')
                        logging.info(f"Полученные данные:\n{response_json}.")
                        return response_json
                    else:
                        raise Exception(f"\nСтатус код: {response.status}.\n"
                                        f"Ответ API: {await response.text()}")
        except Exception as ex:
            logging.error(f"Обмен полный пакет. Ошибка в обмене с API: {ex}")
            return None

    async def _make_full_data_dict(
            self,
            session: AsyncSession,
            data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Создаёт словарь полных данных для отправки на API.
        :param session: Асинхронная сессия базы данных.
        :param data: Данные для отправки.
        :return: Словарь данных.
        """
        orders = await get_orders_with_key(session, data)
        payloads = []

        for order in orders:
            payload = {
                "Number": str(order[0]),
                "Status": None
            }
            payloads.append(payload)

        user = await get_user(session, data)

        return self._full_data_dump_impl(
            dump_number=self._get_next_dump_number(),
            user=user,
            data=data,
            payload=payloads
        )

    @staticmethod
    def _full_data_dump_impl(
            dump_number: str,
            user,
            data: Dict[str, Any],
            payload: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Создаёт словарь полных данных для отправки на API.
        :param dump_number: Номер дампа.
        :param user: Информация о водителе.
        :param data: Данные о заявках.
        :param payload: Список заявок.
        :return: Словарь данных.
        """
        return {
            "id": dump_number,
            "type": "Полные данные",  # Устанавливается по договору обмена
            "driver": {
                "user_agree": bool(user.accept_user_agree),
                "name": user.name,
                "surname": user.surname,
                "middle_name": user.middle_name,
                "number": user.number,
                "passport_series": user.licence_series,
                "passport_number": user.licence_number
            },
            "contact_point": data.get("contact_point"),
            "job_type": data.get("job_type"),
            "use_orders": bool(data.get("use_orders")),
            "payload": payload,
            "partners": data.get("partner"),
            "vehicle_info": {
                "vehicle_number": data.get("vehicle_number"),
                "has_trailer": bool(data.get("has_trailer")),
                "trailer_number": data.get("trailer_number"),
                "vehicle_weight": bool(data.get("trailer_weight")),
            },
            "status": ""  # Не используется в текущей реализации
        }


api_service = APIService()
