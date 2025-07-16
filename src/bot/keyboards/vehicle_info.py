from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.translations.vehicle_info import *
from src.bot.translations.authorization import go_back_kb_text
from src.bot.translations.orders import edit_data_button_text
from src.bot.translations.registration import edit_name_kb_text, edit_surname_kb_text, edit_middle_name_kb_text, edit_number_kb_text


def weight_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_lang_more(lang), callback_data='weight_more'))
    kb.row(InlineKeyboardButton(text=get_lang_less(lang), callback_data='weight_less'))
    return kb.as_markup(resize_keyboard=True)


def create_code_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_generate_code_text(lang), callback_data='create_code'))
    kb.row(InlineKeyboardButton(text=edit_data_button_text(lang), callback_data='edit'))
    return kb.as_markup(resize_keyboard=True)


def activate_code_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=activate_code_button_text(lang), callback_data='activate_code'))
    kb.row(InlineKeyboardButton(text=edit_data_button_text(lang), callback_data='edit'))
    return kb.as_markup(resize_keyboard=True)


def edit_vehicle_info_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ask_edit_personal_data(lang), callback_data='edit_personal_info'))
    kb.row(InlineKeyboardButton(text=ask_edit_vehicle(lang), callback_data='edit_vehicle_info'))
    kb.row(InlineKeyboardButton(text=ask_edit_trailer(lang), callback_data='edit_trailer_info'))
    kb.row(InlineKeyboardButton(text=get_lang_edit_tc_weight(lang), callback_data='edit_weight'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='back'))
    return kb.as_markup(resize_keyboard=True)


def edit_personal_data_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=edit_name_kb_text(lang), callback_data="edit_name"))
    kb.row(InlineKeyboardButton(text=edit_surname_kb_text(lang), callback_data="edit_surname"))
    kb.row(InlineKeyboardButton(text=edit_middle_name_kb_text(lang), callback_data="edit_middle_name"))
    kb.row(InlineKeyboardButton(text=edit_number_kb_text(lang), callback_data="edit_number"))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='step_back'))
    return kb.as_markup(resize_keyboard=True)


def edit_vehicle_number_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ask_edit_format(lang), callback_data='edit_vehicle_format'))
    kb.row(InlineKeyboardButton(text=ask_edit_tc(lang), callback_data='edit_vehicle_number'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='step_back'))
    return kb.as_markup(resize_keyboard=True)


def edit_trailer_info_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ask_edit_has_trailer(lang), callback_data='edit_trailer'))
    kb.row(InlineKeyboardButton(text=ask_edit_format(lang), callback_data='edit_trailer_format'))
    kb.row(InlineKeyboardButton(text=ask_edit_trailer_number(lang), callback_data='edit_trailer_number'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='step_back'))
    return kb.as_markup(resize_keyboard=True)


def select_vehicle_format_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ask_format_ru(lang), callback_data='vehicle_ru'))
    kb.row(InlineKeyboardButton(text=ask_format_by(lang), callback_data='vehicle_by'))
    kb.row(InlineKeyboardButton(text=ask_format_eu(lang), callback_data='vehicle_en'))
    kb.row(InlineKeyboardButton(text=ask_format_kz(lang), callback_data='vehicle_kz'))
    return kb.as_markup(resize_keyboard=True)


def select_trailer_format_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=ask_format_ru(lang), callback_data='trailer_ru'))
    kb.row(InlineKeyboardButton(text=ask_format_by(lang), callback_data='trailer_by'))
    kb.row(InlineKeyboardButton(text=ask_format_eu(lang), callback_data='trailer_en'))
    kb.row(InlineKeyboardButton(text=ask_format_kz(lang), callback_data='trailer_kz'))
    return kb.as_markup(resize_keyboard=True)
