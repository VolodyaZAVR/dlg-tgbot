import re
from typing import Optional

from aiogram.types import Message


class InputUtils:
    @staticmethod
    async def split_licence_input(passport_data: str):
        parts = re.split(r"\s+", passport_data.upper(), maxsplit=1)
        license_series = parts[0] if len(parts) > 1 else ""
        license_number = parts[1] if len(parts) > 1 else parts[0]
        return license_series, license_number

    @staticmethod
    def clear_string(value: Optional[str]) -> Optional[str]:
        """
        Удаляет лишние пробелы, переносы строк и табуляции.
        Оставляет только одинарные пробелы между словами.
        """
        if value is None:
            return None
        return re.sub(r"\s+", " ", value.strip())

    @staticmethod
    def format_name(text: str) -> str:
        if len(text) > 50 or len(text) < 2:
            return ""
        res = text.lower().split("-", 1)
        if len(res) > 1:
            return res[0][0].upper() + res[0][1:] + "-" + res[1][0].upper() + res[1][1:]
        else:
            return res[0][0].upper() + res[0][1:]


def format_name(text: str) -> str:
    if len(text) > 50 or len(text) < 2:
        return ""
    res = text.lower().split("-", 1)
    if len(res) > 1:
        return res[0][0].upper() + res[0][1:] + "-" + res[1][0].upper() + res[1][1:]
    else:
        return res[0][0].upper() + res[0][1:]


def show_response_error(error: list[str] | str) -> str:
    if isinstance(error, list):
        err_text = ""
        for _, line in enumerate(error):
            err_text += "\n" + line + "\n"
        return err_text
    else:
        return error


def show_user_status(user_status, user_id):
    if user_status is not None:
        if bool(user_status):
            text_status = '<b>Заблокирован</b>'
        else:
            text_status = '<b>Активен</b>'
        return f"Статус пользователя с id: {user_id} " + text_status
    else:
        raise Exception(f"Не найден пользователь с {user_id}")


def format_partner(input_str: str) -> str:
    return input_str.replace("_", " ")


def show_orders_with_false_status(orders) -> str:
    result = ""
    for order in orders:
        if not order['Status']:
            result += f"{order['Number']}\n"
    return result


def is_any_false_status(orders) -> bool:
    order_not_found = False
    for order in orders:
        if not order['Status']:
            order_not_found = True
    return order_not_found


def get_weight(text: str) -> str:
    if text == "weight_less":
        return "Нет"
    elif text == "weight_more":
        return "Да"
    else:
        return "Error"


def get_icon(status: bool) -> str:
    return "✅" if status else "⛔️"


def get_orders_with_sheets_statis(orders) -> str:
    text = ""
    for order in orders:
        status = True if order["row_number"] else False
        text += f"<b>{str(order['Number'])} {get_icon(status)}</b>\n"
    return text


def get_orders_with_status(orders) -> str:
    text = ""
    for order in orders:
        text += f"<b>{str(order['Number'])} {get_icon(order['Status'])}</b>\n"
    return text


def get_orders_with_green_icon(orders) -> str:
    text = ""
    for order in orders:
        text += f"<b>{order['Number']} {get_icon(True)}</b>\n"
    return text


def get_orders_in_list(orders) -> str:
    text = ""
    for order in orders:
        text += "<b>" + order["Number"] + "</b>\n"
    return text


def get_orders_type(text: str) -> bool | None:
    if text == "type_accept":
        return None
    elif text == "type_pickup":
        return True
    else:
        return None


def get_job_type(text: str) -> str:
    if text == "type_accept":
        return "Прием"
    elif text == "type_pickup":
        return "Отгрузка"
    else:
        return "Error"


def sheets_weight_class_format(weight_class: bool) -> str:
    return "Больше" if weight_class else "Меньше"


def sheets_job_type_format(input_str: str) -> str:
    match input_str:
        case "Прием":
            return "Прием"
        case "Отгрузка":
            return "Возврат"
        case _:
            return ""


def sheets_contact_point_format(input_str: str) -> str:
    match input_str:
        case "М19":
            return "М19"
        case "М70":
            return "М70"
        case "Уткина Заводь":
            return "УЗ"
        case "Открытая площадка":
            return "ОП"
        case "K8":
            return "K8"
        case _:
            return ""


def get_contact_point(text: str) -> str:
    if text == "point_1":
        return "М19"
    elif text == "point_2":
        return "М70"
    elif text == "point_3":
        return "Уткина Заводь"
    elif text == "point_4":
        return "Открытая площадка"
    elif text == "point_5":
        return "К8"
    else:
        return "Error"
