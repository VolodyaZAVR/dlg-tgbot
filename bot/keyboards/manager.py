from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def manager_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Зарегистрировать заявки", callback_data="manager_reg_orders"))
    kb.row(InlineKeyboardButton(text="Управлять водителями", callback_data="manager_show_users"))
    kb.row(InlineKeyboardButton(text="Управлять заявками", callback_data="manager_show_orders"))
    kb.row(InlineKeyboardButton(text="Выйти", callback_data="exit"))
    return kb.as_markup(resize_keyboard=True)


def search_users_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Поиск по ID", callback_data="manager_by_id"))
    kb.row(InlineKeyboardButton(text="Поиск по фамилии", callback_data="manager_by_surname"))
    kb.row(InlineKeyboardButton(text="Поиск по паспорту", callback_data="manager_by_licence"))
    kb.row(InlineKeyboardButton(text="Добавить запись", callback_data="manager_add_user"))
    kb.row(InlineKeyboardButton(text="Редактировать запись", callback_data="manager_edit_user"))
    kb.row(InlineKeyboardButton(text="Удалить запись", callback_data="manager_delete_user"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manager_kb"))
    return kb.as_markup(resize_keyboard=True)


def search_orders_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Найти заявки по коду активации", callback_data="manager_by_key"))
    kb.row(InlineKeyboardButton(text="Найти заявки по номеру", callback_data="manager_by_number"))
    kb.row(InlineKeyboardButton(text="Найти заявки по водителю", callback_data="manager_by_driver"))
    kb.row(InlineKeyboardButton(text="Удалить заявку", callback_data="manager_delete_order"))
    kb.row(InlineKeyboardButton(text="Аннулировать код активации", callback_data="manager_purge_key"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manager_kb"))
    return kb.as_markup(resize_keyboard=True)


def to_manager_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="manager_to_user_kb"))
    return kb.as_markup(resize_keyboard=True)


def edit_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Изменить имя", callback_data="manager_edit_name"))
    kb.row(InlineKeyboardButton(text="Изменить фамилию", callback_data="manager_edit_surname"))
    kb.row(InlineKeyboardButton(text="Изменить отчество", callback_data="manager_edit_middle_name"))
    kb.row(InlineKeyboardButton(text="Изменить номер", callback_data="manager_edit_number"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manager_kb"))
    return kb.as_markup(resize_keyboard=True)
