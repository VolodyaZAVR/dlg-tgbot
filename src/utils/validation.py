import re
import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.utils.texts_utils import InputUtils

logger = logging.getLogger("bot")


class DriverValidator:
    """Класс для проверки форматов персональных данных."""
    _personal_data_formats = {
        "name": r'^[А-ЯЁа-яё]{2,25}$',
        "surname": r'^[А-ЯЁа-яё]{2,25}(?:-[А-ЯЁа-яё]{2,24})?$',
        "middle_name": r'^([А-ЯЁа-яё]{2,25})?$',
        "phone": r'^[+][7]\d{10}$',
    }

    _passport_formats = {
        "ru": {"series": r"^\d{4}$", "number": r"^\d{6}$"},  # Российский паспорт
        "by": {"series": r"^[ABEIKMHOPCTX]{2}$", "number": r"^\d{7}$"},  # Белорусский паспорт
        "en": {"series": r"^[A-Z]{2}$", "number": r"^\d{7}$"},  # Европейский паспорт
        "kz": {"series": r"^[A-Z]$", "number": r"^\d{8}$"},  # Казахстанский паспорт
        "az": {"series": r"^[A-Z]$", "number": r"^\d{8}$"},  # Азербайджанский паспорт
        "tj": {"series": None, "number": r"^\d{9}$"},  # Таджикский паспорт (только номер)
        "uz": {"series": None, "number": r"^\d{7}$"},  # Узбекский паспорт (только номер)
        "kg": {"series": r"^[A-Z]{2,3}$", "number": r"^\d{6,9}$"},  # Киргизский паспорт
        "ua": {"series": r"^[A-Z]{2}$", "number": r"^\d{6,9}$"},  # Украинский паспорт
    }

    @staticmethod
    def validate_name(value: str) -> bool:
        """Имя имеет длину от 2 до 25 символов кириллицы"""
        pattern = DriverValidator._personal_data_formats.get("name")
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_surname(value: str) -> bool:
        """Фамилия имеет длину от 2 до 25 символов кириллицы и поддерживает двойную фамилию:
        дополнительное тире и от 2 до 24 символов кириллицы"""
        pattern = DriverValidator._personal_data_formats.get("surname")
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_middle_name(value: str) -> bool:
        """Отчество имеет длину от 2 до 25 символов кириллицы либо пустая строка в случае отсутствия отчества"""
        if value == "":
            return True
        pattern = DriverValidator._personal_data_formats.get("middle_name")
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_phone_number(value: str) -> bool:
        """
        Проверяет, что номер телефона соответствует российскому формату.
        Поддерживает форматы: +79111234567, 89111234567, +7 911 123-45-67, 8 (911) 123-45-67, 9111234567.
        """
        digits_only = re.sub(r"\D", "", value)

        if len(digits_only) == 10:
            digits_only = "7" + digits_only

        if len(digits_only) != 11:
            return False

        if digits_only[0] not in ("7", "8"):
            return False

        return True

    @staticmethod
    def format_phone_number(value: str) -> str:
        """
        Получает проверенный номер телефона и приводит его к нужному формату
        :param value: Пример 89111234567, +7 911 123-45-67, 8 (911) 123-45-67, 9111234567
        :return: formated_value: +79111234567
        """
        digits_only = re.sub(r"\D", "", value)

        if len(digits_only) == 10:
            digits_only = "7" + digits_only

        if len(digits_only) != 11:
            raise ValueError("Номер телефона должен содержать 11 цифр.")

        if digits_only[0] not in ("7", "8"):
            raise ValueError("Номер телефона должен начинаться с 7 или 8.")

        return "+7" + digits_only[1:]

    @staticmethod
    def validate_passport_series(passport_series: str | None) -> bool:
        """Проверяет корректность серии паспорта для любого формата."""
        # TODO: апи шлет именно None, но пользователь - пустую строку. Надо унифицировать
        if passport_series == "":
            passport_series = None

        if passport_series is None:
            return True
        try:
            for format_data in DriverValidator._passport_formats.values():
                series_pattern = format_data["series"]
                if series_pattern is None:
                    continue

                if re.match(series_pattern, passport_series):
                    return True
            return False
        except Exception as e:
            logger.error(f"Ошибка валидации серии паспорта: {e}")
            return False

    @staticmethod
    def validate_passport_number(passport_number: str) -> bool:
        """Проверяет корректность номера паспорта для любого формата."""
        try:
            for format_data in DriverValidator._passport_formats.values():
                number_pattern = format_data["number"]
                if re.match(number_pattern, passport_number):
                    return True
            return False
        except Exception as e:
            logger.error(f"Ошибка валидации номера паспорта: {e}")
            return False

    @staticmethod
    def validate_full_passport(passport_series: str | None, passport_number: str) -> bool:
        """Проверяет корректность серии и номера паспорта для любого формата."""
        try:
            # TODO: апи шлет именно None, но пользователь - пустую строку. Надо унифицировать
            if passport_series == "":
                passport_series = None

            for format_data in DriverValidator._passport_formats.values():
                series_pattern = format_data["series"]
                number_pattern = format_data["number"]

                # Если формат не требует серии, пропускаем проверку серии
                if series_pattern is None:
                    if re.match(number_pattern, passport_number):
                        return True
                else:
                    if passport_series is not None and re.match(series_pattern, passport_series) and re.match(
                            number_pattern, passport_number):
                        return True
            return False
        except Exception as e:
            logger.error(f"Ошибка валидации серии и номера паспорта любого формата: {e}")
            return False

    @staticmethod
    async def get_passport_form_msg(msg: Message, state: FSMContext):
        try:
            passport_series, passport_number = await InputUtils.split_licence_input(msg.text)
        except Exception as ex:
            logger.error(f"Не удалось получить паспорт из сообщения: {ex}")
            raise ValueError(f"Не удалось получить паспорт из сообщения: {ex}")
        # Проверяем формат паспорта для любого формата
        if DriverValidator.validate_full_passport(passport_series, passport_number):
            await state.update_data(licence_series=passport_series, licence_number=passport_number)
            return passport_series, passport_number
        else:
            raise ValueError("Паспорт не прошел валидацию")


class VehicleValidator:
    """Класс для проверки форматов номеров транспортных средств."""
    _formats = {
        "ru": {"vehicle": r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$',
               "trailer": r'^[АВЕКМНОРСТУХ]{2}\d{4}\d{2,3}$'},
        "by": {"vehicle": r'^[ABEIKMHOPCTX]{2}\d{4}-\d{1,2}$',
               "trailer": r'^[ABEIKMHOPCTX]\d{4}[ABEIKMHOPCTX]-\d$'},
        "en": {"vehicle": r'^\d{3}[A-Z]{3}$',
               "trailer": r'^[A-Z]{1,3}[\d]{1,4}[A-Z]{1,3}$'},
        "kz": {"vehicle": r'^\d{3}[A-Z]{3}\d{2}$',
               "trailer": r'^[A-Z]{3}\d{4}$'}
    }

    # Временное решение для прицепов - принимаем любую строку 3-10 символов
    TEMP_TRAILER_PATTERN = r'^[A-ZА-ЯЁ0-9-]{3,10}$'

    @staticmethod
    def __normalize_belarus_vehicle_number(vehicle_number: str) -> str:
        """
        Нормализует белорусский номер ТС:
        - Извлекает буквы из любой позиции и перемещает их в начало.
        - Убирает лишние пробелы.
        """
        alphabet = "ABEIKMHOPCTX"
        # Убираем лишние пробелы
        no_space_number = vehicle_number.replace(" ", "")

        # Извлекаем все буквы из строки
        letters = "".join([char for char in no_space_number if char.upper() in alphabet])
        # Извлекаем цифры и дефисы
        digits_and_hyphen = "".join([char for char in no_space_number if char.isdigit() or char == "-"])
        # Формируем новый номер: буквы + цифры и дефисы
        normalized_number = letters + digits_and_hyphen
        return normalized_number

    @staticmethod
    def __normalize_kazakhstan_trailer_number(trailer_numer: str) -> str:
        """
        Нормализует казахский номер прицепа:
        - Извлекает буквы из любой позиции и перемещает их в начало.
        - Убирает лишние пробелы.
        """
        alphabet = "ABEIKMHOPCTX"
        # Убираем лишние пробелы
        no_space_number = trailer_numer.replace(" ", "")

        # Извлекаем все буквы из строки
        letters = "".join([char for char in no_space_number if char.isalpha()])
        # Извлекаем цифры
        digits = "".join([char for char in no_space_number if char.isdigit()])
        # Формируем новый номер: буквы + цифры
        normalized_number = letters + digits
        return normalized_number

    @staticmethod
    def validate_vehicle_number(vehicle_number: str) -> bool:
        """Проверяет корректность номера транспортного средства для любого формата."""
        original_number = vehicle_number
        try:
            for fmt_key, pattern_info in VehicleValidator._formats.items():
                # Нормализуем номер если выбран белорусский формат
                if fmt_key == "by":
                    normalized_number = VehicleValidator.__normalize_belarus_vehicle_number(vehicle_number)
                else:
                    normalized_number = original_number

                if re.match(pattern_info["vehicle"], normalized_number):
                    return True

            return False
        except re.error as e:
            logger.error(f"Regex error in any vehicle validation: {e}")
            return False
        
    @staticmethod
    def validate_trailer_number(trailer_number: str) -> bool:
        """Проверяет корректность номера прицепа для любого формата."""
        original_number = trailer_number
        try:
            # Временное решение - используем общий шаблон вместо специфичного для формата
            if re.match(VehicleValidator.TEMP_TRAILER_PATTERN, original_number, re.IGNORECASE):
                return True

            for fmt_key, pattern_info in VehicleValidator._formats.items():
                # Нормализуем номер прицепа если выбран казахстанский формат
                if fmt_key == "kz":
                    normalized_number = VehicleValidator.__normalize_kazakhstan_trailer_number(original_number)
                else:
                    normalized_number = original_number

                if re.match(pattern_info["trailer"], normalized_number):
                    return True

            return False
        except re.error as e:
            logger.error(f"Regex error in any trailer validation: {e}")
            return False


class OrdersInfoValidator:
    _request_type = "Внешняя регистрация"
    _order_format = r'^[A-Za-zА-Яа-я0-9_№#-\\/\s]{1,60}$'
    _partner_format = r'^[A-Za-zА-Яа-я0-9-\s]{1,50}$'
    _key_format = r'^\d\d\d\d\d\d$'
    _allowed_contact_points = {"М19", "М70", "УЗ", "ОП", "K8"}
    _allowed_job_type = {"Прием", "Отгрузка"}

    @staticmethod
    def request_type():
        return OrdersInfoValidator._request_type

    @staticmethod
    def allowed_contact_points():
        return OrdersInfoValidator._allowed_contact_points

    @staticmethod
    def allowed_job_type():
        return OrdersInfoValidator._allowed_job_type

    @staticmethod
    def validate_order(value: str) -> bool:
        pattern = OrdersInfoValidator._order_format
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_partner(value: str) -> bool:
        pattern = OrdersInfoValidator._partner_format
        return bool(re.match(pattern, value))


class KeyValidator:
    _request_type = "Запрос на аннулирование"
    _key_format = r'\d{6}'

    @staticmethod
    def request_type():
        return KeyValidator._request_type

    @staticmethod
    def validate_key(value: str) -> bool:
        pattern = KeyValidator._key_format
        return bool(re.match(pattern, value))
