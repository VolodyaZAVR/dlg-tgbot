from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.texts.authorization import edit_licence_kb_text, go_back_kb_text
from src.bot.texts.registration import skip_middle_name_kb_text, accept_user_agree_kb_text, apply_registration_kb_text, \
    edit_reg_data_kb_text, edit_name_kb_text, edit_surname_kb_text, edit_middle_name_kb_text, edit_number_kb_text


def skip_middle_name_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=skip_middle_name_kb_text(lang), callback_data="skip"))
    return kb.as_markup(resize_keyboard=True)


def accept_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=accept_user_agree_kb_text(lang), callback_data="accept"))
    return kb.as_markup(resize_keyboard=True)


def registration_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=apply_registration_kb_text(lang), callback_data="registration"))
    kb.row(InlineKeyboardButton(text=edit_reg_data_kb_text(lang), callback_data="edit"))
    return kb.as_markup(resize_keyboard=True)


def edit_data_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=edit_name_kb_text(lang), callback_data="edit_name"))
    kb.row(InlineKeyboardButton(text=edit_surname_kb_text(lang), callback_data="edit_surname"))
    kb.row(InlineKeyboardButton(text=edit_middle_name_kb_text(lang), callback_data="edit_middle_name"))
    kb.row(InlineKeyboardButton(text=edit_number_kb_text(lang), callback_data="edit_number"))
    kb.row(InlineKeyboardButton(text=edit_licence_kb_text(lang), callback_data="edit_licence"))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='back'))
    return kb.as_markup(resize_keyboard=True)
