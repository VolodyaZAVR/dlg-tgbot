import re
import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from typing import List, Dict, Any

from src.utils.texts_utils import InputUtils, format_partner, format_name

logger = logging.getLogger("bot")


class LanguageValidator:
    """Класс для проверки языковых кодов."""
    VALID_LANGUAGES = {'ru', 'en', 'kz', 'by', 'az', 'uz', 'tg', 'kg'}

    @staticmethod
    def validate_lang_code(lang_code: str) -> str:
        """Проверяет корректность языкового кода."""
        if lang_code not in LanguageValidator.VALID_LANGUAGES:
            raise ValueError("Invalid language code.")
        return lang_code


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
    def validate_license(selected_format: str, license_series: str, license_number: str) -> bool:
        """Проверяет корректность серии и номера паспорта для выбранного формата."""
        format_data = DriverValidator._passport_formats.get(selected_format)
        if not format_data:
            return False

        series_pattern = format_data["series"]
        number_pattern = format_data["number"]

        try:
            if not re.match(number_pattern, license_number):
                return False

            if series_pattern:
                if not license_series or not re.match(series_pattern, license_series):
                    return False

            return True
        except re.error as e:
            logger.error(f"Validation licence regex error: {e}")
            return False

    @staticmethod
    def validate_any_license(license_series: str, license_number: str) -> bool:
        """Проверяет корректность серии и номера паспорта для любого формата."""
        try:
            for format_data in DriverValidator._passport_formats.values():
                series_pattern = format_data["series"]
                number_pattern = format_data["number"]

                # Если формат не требует серии, пропускаем проверку серии
                if series_pattern is None:
                    if re.match(number_pattern, license_number):
                        return True
                else:
                    if re.match(series_pattern, license_series) and re.match(number_pattern, license_number):
                        return True

        except Exception as e:
            logger.error(f"Validation any format licence regex error: {e}")
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
        "kz": {"vehicle": r'^[A-Z]\d{3}[A-Z]{2}$|^\d{3}[A-Z]{2}\d{2}$|^\d{3}[A-Z]{3}\d{2}$',
               "trailer": r'^[A-Z]{3}\d{4}$'},
        "kg": {"vehicle": r'^\d{2,3}[A-Z]{2}$',
               "trailer": r'^[A-Z]{2}\d{4}$'}
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
    def validate_vehicle(selected_format: str, vehicle_number: str) -> bool:
        """Проверяет корректность номера транспортного средства для выбранного формата."""
        try:
            vehicle_pattern = VehicleValidator._formats.get(selected_format)
            if not vehicle_pattern or not vehicle_pattern["vehicle"]:
                return False

            # Нормализуем номер если выбран белорусский формат
            if selected_format == "by":
                vehicle_number = VehicleValidator.__normalize_belarus_vehicle_number(vehicle_number)

            if re.match(vehicle_pattern["vehicle"], vehicle_number):
                return True
        except re.error as e:
            logger.error(f"Regex error in vehicle validation: {e}")
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

    @staticmethod
    def validate_trailer(selected_format: str, trailer_number: str) -> bool:
        """Проверяет корректность номера прицепа для выбранного формата."""
        original_number = trailer_number.upper()
        try:
            # Временное решение - используем общий шаблон вместо специфичного для формата
            if re.match(VehicleValidator.TEMP_TRAILER_PATTERN, original_number, re.IGNORECASE):
                return True

            format_data = VehicleValidator._formats.get(selected_format)
            if not format_data or not format_data["trailer"]:
                return False

            # Нормализуем номер прицепа если выбран казахстанский формат
            if selected_format == "kz":
                trailer_number = VehicleValidator.__normalize_kazakhstan_trailer_number(trailer_number)

            trailer_pattern = format_data["trailer"]
            if re.match(trailer_pattern, trailer_number):
                return True
        except re.error as e:
            logger.error(f"Regex error in trailer validation: {e}")
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

    @staticmethod
    def validate_orders_type(input_str: str) -> bool:
        if input_str.lower() == "заявки":
            return True
        elif input_str.lower() == "контейнер":
            return False
        else:
            raise ValueError(f'Некорректно указан тип заявки: {input_str}')

    @staticmethod
    def validate_job_type(input_str: str) -> str:
        if input_str.lower() == "поступление":
            return "Прием"
        elif input_str.lower() == "возврат":
            return "Отгрузка"
        else:
            raise ValueError(f'Некорректно указана цель визита: {input_str}')

    @staticmethod
    def validate_contact_point(input_str: str) -> str:
        if input_str.lower() == "м19":
            return "М19"
        elif input_str.lower() == "м70":
            return "М70"
        elif input_str.lower() == "уткина_заводь":
            return "Уткина Заводь"
        elif input_str.lower() == "открытая_площадка":
            return "Открытая площадка"
        elif input_str.lower() == "к8":
            return "K8"
        else:
            raise ValueError(f'Некорректно указана площадка: {input_str}')


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


class IDValidator:
    """Класс для проверки ID пользователей."""
    id_vocabulary = r'^\d{6,10}$'

    @staticmethod
    def is_correct_id(user_id: str) -> bool:
        """Проверяет корректность telegram ID пользователя перед добавлением в конфиг."""
        try:
            if re.match(IDValidator.id_vocabulary, user_id):
                user_id = int(user_id)  # cannot make it int than raise error
                return True
        except re.error as e:
            logger.error(f"Regex error in is correct id: {e}")
        except Exception as ex:
            logger.error(f"Cannot make user ID to int. User ID: {user_id}. Error: {ex}")
        return False


# Bot-specific validation functions that use the validators above
async def validate_vehicle_input(input_text: str, state: FSMContext):
    """Валидация ввода информации о транспортном средстве для бота."""
    lines = input_text.split(' ')
    for i, line in enumerate(lines, 1):
        if i == 1:
            if VehicleValidator.validate_vehicle_number(line.strip().upper()):
                await state.update_data(vehicle_number=line.strip().upper())
            else:
                raise ValueError(f"Некорректный ввод номера ТС: {line.strip().upper()}")
        if i == 2:
            if line.strip().lower() == "нет":
                await state.update_data(trailer=False)
                await state.update_data(trailer_number="")
            elif VehicleValidator.validate_trailer_number(line.strip().upper()):
                await state.update_data(trailer=True)
                await state.update_data(trailer_number=line.strip().upper())
            else:
                raise ValueError(f"Некорректный ввод номера прицепа {line.strip().upper()}")
        if i == 3:
            match line.strip().lower():
                case "больше":
                    await state.update_data(trailer_weight="Да")
                case "меньше":
                    await state.update_data(trailer_weight="Нет")
                case default:
                    raise ValueError(f"Некорректный ввод класса грузоподъемности: {line.strip()}")
    return await state.get_data()


async def validate_orders_numbers(input_text: str, state: FSMContext, current_orders: List[Dict[str, Any]]):
    """
    Обрабатывает ввод номеров заявок, разделенных пробелами или переносами строк.
    :param input_text: Строка с номерами заявок, разделенными пробелами или переносами строк.
    :param state: Машина состояний.
    :param current_orders: Текущий список заявок.
    :return: Обновленные данные из машины состояний.
    """
    # Разделяем строку по пробелам и переносам строк
    text = re.sub(r'\s+', " ", input_text.strip())
    lines = re.split(r'[ \n]+', text.strip())  # Разбиваем по пробелам и переносам строк
    orders = current_orders

    for line in lines:
        order_number = line.strip()
        if not order_number:
            continue

        order = {
            "Number": validate_order(order_number),
            "Status": None,
            "row_number": None
        }
        orders.append(order)

    # Обновляем данные в состоянии
    await state.update_data(orders=orders)
    return await state.get_data()


async def validate_orders(input_text: str, state: FSMContext):
    """Валидация ввода заявок для бота."""
    lines = input_text.split(' ')
    orders = []
    for i, line in enumerate(lines, 1):
        if i == 1:
            await state.update_data(contact_point=OrdersInfoValidator.validate_contact_point(line.strip()))
        elif i == 2:
            await state.update_data(job_type=OrdersInfoValidator.validate_job_type(line.strip()))
        elif i == 3:
            await state.update_data(partner=validate_partner(format_partner(line.strip())))
        elif i == 4:
            await state.update_data(use_orders=OrdersInfoValidator.validate_orders_type(line.strip()))
        elif i > 4:
            order = {
                "Number": validate_order(line.strip()),
                "Status": None,
                "row_number": None
            }
            orders.append(order)
            await state.update_data(orders=orders)
    return await state.get_data()


def validate_order(input_str: str) -> str:
    """Валидация номера заявки."""
    if OrdersInfoValidator.validate_order(input_str):
        return input_str
    else:
        raise ValueError(f'Некорректно указана заявка: {input_str}')


def validate_partner(input_str: str) -> str:
    """Валидация контрагента."""
    if OrdersInfoValidator.validate_partner(input_str):
        return input_str
    else:
        raise ValueError(f'Некорректно указан контрагент: {input_str}')


async def validate_user_data(input_text: str, state: FSMContext):
    """Валидация персональных данных пользователя для бота."""
    lines = input_text.split(' ')
    for i, line in enumerate(lines, 1):
        if i == 1:
            if DriverValidator.validate_surname(format_name(line.strip())):
                await state.update_data(surname=format_name(line.strip()))
            else:
                raise ValueError(f"Некорректно указана фамилия: {line.strip()}")
        elif i == 2:
            if DriverValidator.validate_name(format_name(line.strip())):
                await state.update_data(name=format_name(line.strip()))
            else:
                raise ValueError(f"Некорректно указано имя: {line.strip()}")
        elif i == 3:
            if DriverValidator.validate_middle_name(format_name(line.strip())):
                await state.update_data(middle_name=format_name(line.strip()))
            else:
                raise ValueError(f"Некорректно указано отчество: {line.strip()}")
        elif i == 4:
            if DriverValidator.validate_phone_number(line.strip()):
                await state.update_data(number=line.strip())
            else:
                raise ValueError(f"Неверно введен номер телефона: {line.strip()}")
    return await state.get_data()


def format_user_data(input_text):
    """Форматирование данных пользователя."""
    lines = input_text.split('\n')
    result = {}

    for i, line in enumerate(lines, 1):
        if i == 1:
            result['name'] = format_name(line.strip())
        elif i == 2:
            result['surname'] = format_name(line.strip())
        elif i == 3:
            result['middle_name'] = format_name(line.strip())
        elif i == 4:
            result['number'] = line.strip()
        elif i == 5:
            result['licence_series'] = line.strip()
        elif i == 6:
            result['licence_number'] = line.strip()
        else:
            print(f"Пропуск неизвестной строки {i}")
    return result


def is_formated_number(number: str) -> bool:
    """Проверка формата номера телефона."""
    return DriverValidator.validate_phone_number(number)
