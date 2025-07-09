from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Зарегистрировать заявки", callback_data="reg_orders"))
    kb.row(InlineKeyboardButton(text="Управлять водителями", callback_data="show_users"))
    kb.row(InlineKeyboardButton(text="Управлять заявками", callback_data="show_orders"))
    kb.row(InlineKeyboardButton(text="Ограничить доступ", callback_data="block_user"))
    kb.row(InlineKeyboardButton(text="Управлять правами", callback_data="manage_access"))
    kb.row(InlineKeyboardButton(text="Выйти", callback_data="exit"))
    return kb.as_markup(resize_keyboard=True)


def search_users_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Поиск по ID", callback_data="by_id"))
    kb.row(InlineKeyboardButton(text="Поиск по фамилии", callback_data="by_surname"))
    kb.row(InlineKeyboardButton(text="Поиск по паспорту", callback_data="by_licence"))
    kb.row(InlineKeyboardButton(text="Добавить запись", callback_data="admin_add_user"))
    kb.row(InlineKeyboardButton(text="Редактировать запись", callback_data="admin_edit_user"))
    kb.row(InlineKeyboardButton(text="Удалить запись", callback_data="admin_delete_user"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_kb"))
    return kb.as_markup(resize_keyboard=True)


def search_orders_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Найти заявки по коду активации", callback_data="by_key"))
    kb.row(InlineKeyboardButton(text="Найти заявки по номеру", callback_data="by_number"))
    kb.row(InlineKeyboardButton(text="Найти заявки по водителю", callback_data="by_driver"))
    kb.row(InlineKeyboardButton(text="Удалить заявку", callback_data="admin_delete_order"))
    kb.row(InlineKeyboardButton(text="Аннулировать код активации", callback_data="admin_purge_key"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_kb"))
    return kb.as_markup(resize_keyboard=True)


def to_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_user_kb"))
    return kb.as_markup(resize_keyboard=True)


def edit_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Изменить имя", callback_data="admin_edit_name"))
    kb.row(InlineKeyboardButton(text="Изменить фамилию", callback_data="admin_edit_surname"))
    kb.row(InlineKeyboardButton(text="Изменить отчество", callback_data="admin_edit_middle_name"))
    kb.row(InlineKeyboardButton(text="Изменить номер", callback_data="admin_edit_number"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_kb"))
    return kb.as_markup(resize_keyboard=True)


def block_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Заблокировать", callback_data="block"))
    kb.row(InlineKeyboardButton(text="Разблокировать", callback_data="unblock"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_kb"))
    return kb.as_markup(resize_keyboard=True)


def manage_access_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Управлять стойками", callback_data="manage_stands"))
    kb.row(InlineKeyboardButton(text="Управлять админами", callback_data="manage_admins"))
    kb.row(InlineKeyboardButton(text="Управлять менеджерами", callback_data="manage_managers"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_kb"))
    return kb.as_markup(resize_keyboard=True)


def manage_stands_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Вывести список стоек", callback_data="access_show_stands"))
    kb.row(InlineKeyboardButton(text="Добавить стойку", callback_data="add_stand"))
    kb.row(InlineKeyboardButton(text="Удалить стройку", callback_data="remove_stand"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manage_access_kb"))
    return kb.as_markup(resize_keyboard=True)


def manage_admins_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Вывести список админов", callback_data="access_show_admins"))
    kb.row(InlineKeyboardButton(text="Добавить админа", callback_data="add_admin"))
    kb.row(InlineKeyboardButton(text="Удалить админа", callback_data="remove_admin"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manage_access_kb"))
    return kb.as_markup(resize_keyboard=True)


def manage_managers_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Вывести список менеджеров", callback_data="access_show_managers"))
    kb.row(InlineKeyboardButton(text="Добавить менеджера", callback_data="add_manager"))
    kb.row(InlineKeyboardButton(text="Удалить менеджера", callback_data="remove_manager"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="to_manage_access_kb"))
    return kb.as_markup(resize_keyboard=True)
