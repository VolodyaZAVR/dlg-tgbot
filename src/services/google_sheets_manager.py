import os
import logging
import pytz
from datetime import datetime
from typing import Dict, Any, List

from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.api_core.retry import Retry
from googleapiclient.errors import HttpError

from src.database.scripts.authorization import get_user
from src.database.scripts.orders import select_orders_row_numbers_with_key
from src.services.settings import settings
from src.utils.texts_utils import sheets_weight_class_format, sheets_job_type_format, \
    sheets_contact_point_format


class GoogleSheetsClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._credentials_path = settings.google_sheet["credentials_path"]
        self._spreadsheet_id = settings.google_sheet["spreadsheet_id"]
        self._service = self._build_service()
        self._document_column = settings.google_sheet["document_column"]
        self._reg_time_column = settings.google_sheet["registration_time_column"]
        self._offset_row = settings.google_sheet["offset_row"]
        self._start_write = settings.google_sheet["writing_start_column"]
        self._start_write_idx = settings.google_sheet["writing_start_index"]
        self._end_write = settings.google_sheet["writing_end_column"]
        self._end_write_idx = settings.google_sheet["writing_end_index"]

    def _build_service(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        config_dir = os.path.join(project_root, "config")
        credentials_path = os.path.join(config_dir, self._credentials_path)
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        return build('sheets', 'v4', credentials=creds)

    @staticmethod
    def _get_moscow_time():
        return datetime.now(pytz.timezone("Europe/Moscow"))

    def _get_current_sheet_name(self) -> str:
        """
        Генерирует имя листа, соответствующее текущему дню в формате DD.MM.
        :return: Имя листа.
        """
        return self._get_moscow_time().strftime("%d.%m")

    def _get_sheet_id(self, sheet_name: str) -> int:
        """
        Получает ID листа по его имени.
        :param sheet_name: Имя листа.
        :return: ID листа.
        :raises ValueError: Если лист с указанным именем не найден.
        """
        try:
            # Получаем метаданные таблицы
            spreadsheet = self._service.spreadsheets().get(
                spreadsheetId=self._spreadsheet_id
            ).execute()
            sheets = spreadsheet.get('sheets', [])

            # Ищем лист по имени
            for sheet in sheets:
                properties = sheet.get('properties', {})
                title = properties.get('title')
                sheet_id = properties.get('sheetId')

                if title == sheet_name and isinstance(sheet_id, int):
                    return sheet_id

            # Если лист не найден
            raise ValueError(f"Лист с именем '{sheet_name}' не найден.")

        except HttpError as ex:
            logging.error(f"HTTP ошибка при получении метаданных таблицы: {ex}")
            raise ValueError(f"Не удалось получить ID листа из-за HTTP ошибки: {ex}")
        except Exception as ex:
            logging.error(f"Неожиданная ошибка при получении ID листа: {ex}")
            raise ValueError(f"Произошла ошибка при получении ID листа: {ex}")

    @property
    def is_online(self) -> bool:
        try:
            sheet_id = self._get_sheet_id(self._get_current_sheet_name())
            if sheet_id is not None:
                return True

        except ValueError:
            return False
        except Exception:
            return False

    @Retry(initial=1.0, maximum=90.0, multiplier=2.0)
    def _execute_values_get(self, range_name: str) -> dict | None:
        try:
            return self._service.spreadsheets().values().get(
                spreadsheetId=self._spreadsheet_id,
                range=range_name
            ).execute()
        except HttpError as ex:
            if ex.resp.status == 429:
                logging.warning("Превышено количество запросов. Повторная попытка...")
                raise ex
            else:
                logging.error(f"Ошибка HTTP при выполнении get: {ex}")
                return None
        except Exception as ex:
            logging.error(f"Неожиданная ошибка при выполнении get: {ex}")
            return None

    @Retry(initial=1.0, maximum=90.0, multiplier=2.0)
    def _execute_values_batch_get(self, ranges: list) -> dict | None:
        try:
            result = self._service.spreadsheets().values().batchGet(
                spreadsheetId=self._spreadsheet_id,
                ranges=ranges
            ).execute()
            return result
        except HttpError as ex:
            if ex.resp.status == 429:
                logging.warning("Превышено количество запросов. Повторная попытка...")
                raise ex
            else:
                logging.error(f"Ошибка HTTP при выполнении batchGet: {ex}")
                return None
        except Exception as ex:
            logging.error(f"Неожиданная ошибка при выполнении batchGet: {ex}")
            return None

    @Retry(initial=1.0, maximum=90.0, multiplier=2.0)
    def _execute_batch_update(self, requests: list):
        """
        Выполняет запрос batchUpdate к Google Sheets API с механизмом повторных попыток.
        :param requests: Список запросов для batchUpdate.
        """
        try:
            body = {"requests": requests}
            self._service.spreadsheets().batchUpdate(
                spreadsheetId=self._spreadsheet_id,
                body=body
            ).execute()
        except HttpError as ex:
            if ex.resp.status == 429:
                logging.warning("Превышено количество запросов. Повторная попытка...")
                raise ex
            else:
                logging.error(f"Ошибка HTTP при выполнении batchUpdate: {ex}")
                raise ex
        except Exception as ex:
            logging.error(f"Неожиданная ошибка при выполнении batchUpdate: {ex}")
            raise ex

    async def _collect_body_values(self, session: AsyncSession, data: dict) -> list | None:
        try:
            user = await get_user(session, data)
            if not user:
                raise Exception("Не удалось получить данные о водителе")

            full_name = " ".join(filter(None, [user.surname, user.name, user.middle_name]))
            licence = f"{data.get('licence_series', '')} {data.get('licence_number', '')}"
            curr_time = self._get_moscow_time().strftime("%H:%M:%S")

            values = [
                full_name,
                curr_time,
                "",
                "",
                user.number,
                "",
                sheets_contact_point_format(data.get('contact_point', '')),
                sheets_job_type_format(data.get('job_type', '')),
                licence,
                data.get('vehicle_number', ''),
                data.get('trailer_number', ''),
                sheets_weight_class_format(data.get('trailer_weight'))
            ]
            return values
        except Exception as ex:
            logging.error(f"Не удалось собрать список данных для записи: {ex}. "
                          f"Набор данных на котором произошла ошибка: {data}")
            return None

    async def check_orders_existing(self, state: FSMContext) -> Dict[str, Any] | None:
        orders = (await state.get_data()).get("orders", [])
        enriched_orders = []

        sheet_name = self._get_current_sheet_name()
        document_range = f"{sheet_name}!{self._document_column}{self._offset_row}:{self._document_column}"
        reg_time_range = f"{sheet_name}!{self._reg_time_column}{self._offset_row}:{self._reg_time_column}"

        try:
            result = self._execute_values_batch_get(ranges=[document_range, reg_time_range])

            if not result:
                raise Exception("Не пришел ответ от Google API")

            value_ranges = result.get('valueRanges', [])
            if len(value_ranges) < 2:
                raise Exception(f"В результате запроса недостаточно данных. result: {value_ranges}")

            document_values = value_ranges[0].get('values', [])
            registration_time_values = value_ranges[1].get('values', [])

            document_dict = {
                row[0]: idx + self._offset_row
                for idx, row in enumerate(document_values)
                if row and row[0]
            }

            for order in orders:
                order_number = order["Number"]
                print(order_number)
                row_number = document_dict.get(order_number)

                print(row_number)
                if row_number:
                    reg_time_index = row_number - self._offset_row
                    registration_time_row = (
                        registration_time_values[reg_time_index][0]
                        if len(registration_time_values) > reg_time_index and registration_time_values[
                            reg_time_index]
                        else None
                    )
                    status = True if not registration_time_row else None
                else:
                    status = None

                print(status)
                enriched_order = {
                    **order,
                    "Status": status,
                    "row_number": row_number
                }
                enriched_orders.append(enriched_order)

            print("enriched", enriched_orders)
            await state.update_data(orders=enriched_orders)
            return await state.get_data()

        except Exception as ex:
            logging.error(f"Ошибка при проверке заявок в гугл таблице: {ex}, "
                          f"набор данных на котором произошла ошибка: {orders}")
            return None

    async def write_data_to_row(self, session: AsyncSession, data: dict) -> bool:
        """
        Записывает данные в определенные строки в заданных столбцах и выравнивает текст по центру.
        :param session: Асинхронная сессия базы данных
        :param data: Словарь с данными для записи.
        :return: True, если запись прошла успешно, иначе False.
        """
        try:
            sheet_name = self._get_current_sheet_name()
            sheet_id = self._get_sheet_id(sheet_name)

            # Получаем заявки для записи и данные о водителе
            orders = await select_orders_row_numbers_with_key(session, data)
            values = await self._collect_body_values(session, data)

            if not values:
                raise Exception("Данные для записи не получены")

            # Создаем список запросов для batchUpdate
            requests = []

            for order in orders:
                row_number = order[0]
                range_name = f"{sheet_name}!{self._start_write}{row_number}:{self._end_write}{row_number}"

                # Добавляем запрос на запись данных
                requests.append({
                    "updateCells": {
                        "rows": [{"values": [{"userEnteredValue": {"stringValue": value}} for value in values]}],
                        "fields": "userEnteredValue",
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row_number - 1,
                            "endRowIndex": row_number,
                            "startColumnIndex": self._start_write_idx,
                            "endColumnIndex": self._end_write_idx
                        }
                    }
                })

                # Добавляем запрос на выравнивание по центру
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row_number - 1,
                            "endRowIndex": row_number,
                            "startColumnIndex": self._start_write_idx,
                            "endColumnIndex": self._end_write_idx
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": "CENTER"
                            }
                        },
                        "fields": "userEnteredFormat.horizontalAlignment"
                    }
                })

            # Выполняем все запросы через batchUpdate
            self._execute_batch_update(requests)

            logging.info(f"Данные успешно записаны для {len(orders)} заявок.")
            return True

        except ValueError as ve:
            logging.error(f"Не найдено id листа при записи данных в Google Таблицу: {ve}")
            return False
        except Exception as ex:
            logging.error(f"Ошибка при записи данных в Google Таблицу: {ex}.")
            return False

    @staticmethod
    async def is_any_order_exists(orders: List[Dict[str, Any]]) -> bool:
        for order in orders:
            if order["row_number"]:
                return True
        return False


sheets_manager = GoogleSheetsClient()
