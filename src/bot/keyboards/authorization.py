from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.texts.authorization import auth_kb_text, edit_licence_kb_text, apply_authorization_kb_text, \
    deny_authorization_kb_text


def auth_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=auth_kb_text(lang), callback_data="authorization"))
    kb.row(InlineKeyboardButton(text=edit_licence_kb_text(lang), callback_data="edit_licence"))
    return kb.as_markup(resize_keyboard=True)


def confirm_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=apply_authorization_kb_text(lang), callback_data="correct_data"))
    kb.row(InlineKeyboardButton(text=deny_authorization_kb_text(lang), callback_data="edit_licence"))
    return kb.as_markup(resize_keyboard=True)
