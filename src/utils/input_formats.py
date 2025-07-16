import re
import logging
from typing import List, Dict, Any

from aiogram.fsm.context import FSMContext

from src.utils.texts_utils import format_partner, format_name
from src.utils.validation import (
    LanguageValidator, DriverValidator, VehicleValidator,
    OrdersInfoValidator, KeyValidator, IDValidator,
    validate_vehicle_input, validate_orders_numbers, validate_orders,
    validate_user_data, format_user_data, is_formated_number
)

logger = logging.getLogger("bot")


# Legacy function for backward compatibility
def validate_lang_code(lang_code: str):
    return LanguageValidator.validate_lang_code(lang_code)


# Legacy classes for backward compatibility - these now use the validators from validation.py
class AuthorizationFormat:
    """Legacy class - use DriverValidator instead."""

    @staticmethod
    def validate_license(selected_format: str, license_series: str, license_number: str) -> bool:
        return DriverValidator.validate_license(selected_format, license_series, license_number)

    @staticmethod
    def validate_any_license(license_series: str, license_number: str) -> bool:
        return DriverValidator.validate_any_license(license_series, license_number)


class PersonalDataFormat:
    """Legacy class - use DriverValidator instead."""

    @staticmethod
    def validate(field: str, value: str) -> bool:
        if field == "name":
            return DriverValidator.validate_name(value)
        elif field == "surname":
            return DriverValidator.validate_surname(value)
        elif field == "middle_name":
            return DriverValidator.validate_middle_name(value)
        elif field == "phone":
            return DriverValidator.validate_phone_number(value)
        else:
            raise ValueError(f"Неизвестное поле: {field}")


class ApplicationFormat:
    """Legacy class - use OrdersInfoValidator instead."""

    @staticmethod
    def validate(field: str, value: str) -> bool:
        if field == "order":
            return OrdersInfoValidator.validate_order(value)
        elif field == "partner":
            return OrdersInfoValidator.validate_partner(value)
        elif field == "key":
            return KeyValidator.validate_key(value)
        else:
            raise ValueError(f"Неизвестное поле: {field}")


class VehicleFormat:
    """Legacy class - use VehicleValidator instead."""

    @staticmethod
    def validate_vehicle(selected_format: str, vehicle_number: str) -> bool:
        return VehicleValidator.validate_vehicle(selected_format, vehicle_number)

    @staticmethod
    def validate_any_vehicle(vehicle_number: str) -> bool:
        return VehicleValidator.validate_vehicle_number(vehicle_number)

    @staticmethod
    def validate_trailer(selected_format: str, trailer_number: str) -> bool:
        return VehicleValidator.validate_trailer(selected_format, trailer_number)

    @staticmethod
    def validate_any_trailer(trailer_number: str) -> bool:
        return VehicleValidator.validate_trailer_number(trailer_number)


class IDFormats:
    """Legacy class - use IDValidator instead."""

    @staticmethod
    def is_correct_id(user_id: str) -> bool:
        return IDValidator.is_correct_id(user_id)


# Legacy functions for backward compatibility
async def validate_vehicle(input_text: str, state: FSMContext):
    """Legacy function - use validate_vehicle_input from validation.py instead."""
    return await validate_vehicle_input(input_text, state)


async def validate_orders_numbers(input_text: str, state: FSMContext, current_orders: List[Dict[str, Any]]):
    """Legacy function - use validate_orders_numbers from validation.py instead."""
    return await validate_orders_numbers(input_text, state, current_orders)


async def validate_orders(input_text: str, state: FSMContext):
    """Legacy function - use validate_orders from validation.py instead."""
    return await validate_orders(input_text, state)


def validate_order(input_str: str) -> str:
    """Legacy function - use OrdersInfoValidator.validate_order instead."""
    if OrdersInfoValidator.validate_order(input_str):
        return input_str
    else:
        raise ValueError(f'Некорректно указана заявка: {input_str}')


def validate_partner(input_str: str) -> str:
    """Legacy function - use OrdersInfoValidator.validate_partner instead."""
    if OrdersInfoValidator.validate_partner(input_str):
        return input_str
    else:
        raise ValueError(f'Некорректно указан контрагент: {input_str}')


def validate_orders_type(input_str: str) -> bool:
    """Legacy function - use OrdersInfoValidator.validate_orders_type instead."""
    return OrdersInfoValidator.validate_orders_type(input_str)


def validate_job_type(input_str: str) -> str:
    """Legacy function - use OrdersInfoValidator.validate_job_type instead."""
    return OrdersInfoValidator.validate_job_type(input_str)


def validate_contact_point(input_str: str) -> str:
    """Legacy function - use OrdersInfoValidator.validate_contact_point instead."""
    return OrdersInfoValidator.validate_contact_point(input_str)


async def validate_user_data(input_text: str, state: FSMContext):
    """Legacy function - use validate_user_data from validation.py instead."""
    return await validate_user_data(input_text, state)


def format_user_data(input_text):
    """Legacy function - use format_user_data from validation.py instead."""
    return format_user_data(input_text)


def is_formated_number(number: str) -> bool:
    """Legacy function - use is_formated_number from validation.py instead."""
    return is_formated_number(number)


"""Legacy classes - need to use classes from validation.py instead."""


class RegistrationFormats:
    name = r'^[А-ЯЁа-яё]\w{2,24}$'
    surname = r'^[А-ЯЁа-яё]\w{2,24}(?:-[А-ЯЁа-яё]\w{2,24})?$'
    middle_name = r'^([А-ЯЁа-яё]\w{2,24})?$'

    def validate_name(self, name: str):
        try:
            if re.match(self.name, name):
                return name
        except re.error as e:
            logging.error(f"Regex error: {e}")

        raise ValueError(f"Имя введено неверно: {name}")

    def validate_surname(self, surname: str):
        try:
            if re.match(self.surname, surname):
                return surname
        except re.error as e:
            logging.error(f"Regex error: {e}")

        raise ValueError(f"Фамилия введена неверно: {surname}")

    def validate_middle_name(self, middle_name: str):
        try:
            if re.match(self.middle_name, middle_name) or middle_name == "":
                return middle_name
        except re.error as e:
            logging.error(f"Regex error: {e}")

        raise ValueError(f"Отчество введено неверно: {middle_name}")


class NumbersFormats:
    format1 = r'^[+][7]\d\d\d\d\d\d\d\d\d\d$'
    format2 = r'^[+][3][7][2]\d\d\d\d\d\d\d\d$'
    format3 = r'^[+][3][7][5]\d\d\d\d\d\d\d\d$'
    format4 = r'^[+][9][9][6]\d\d\d\d\d\d\d\d\d$'


class OrdersFormats:
    order = r'^[A-Za-zА-Яа-я0-9_№#-\\/\s]{1,60}$'


class PartnersFormats:
    partner = r'^[A-Za-zА-Яа-я0-9-\s]{1,50}$'


class KeyFormats:
    key = r'^\d\d\d\d\d\d$'
