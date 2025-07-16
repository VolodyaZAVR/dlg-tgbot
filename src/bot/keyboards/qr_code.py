from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.translations.qr_code import cls_button_text, activate_button_text


def clear_history_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=cls_button_text(lang), callback_data='clear'))
    return kb.as_markup(resize_keyboard=True)


def activate_key_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=activate_button_text(lang), callback_data='activate_key'))
    return kb.as_markup(resize_keyboard=True)
