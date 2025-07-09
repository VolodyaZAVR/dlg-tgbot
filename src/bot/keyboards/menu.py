from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.texts.menu import lang_button_text
from src.bot.texts.qr_code import menu_button_text, edit_lang_button_text, no_code_button_text, has_code_button_text


def lang_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text=lang_button_text('ru'), callback_data='lang_ru')
    btn2 = InlineKeyboardButton(text=lang_button_text('en'), callback_data='lang_en')
    btn3 = InlineKeyboardButton(text=lang_button_text('kz'), callback_data='lang_kz')
    btn4 = InlineKeyboardButton(text=lang_button_text('by'), callback_data='lang_by')
    btn5 = InlineKeyboardButton(text=lang_button_text('az'), callback_data='lang_az')
    btn6 = InlineKeyboardButton(text=lang_button_text('uz'), callback_data='lang_uz')
    btn7 = InlineKeyboardButton(text=lang_button_text('tg'), callback_data='lang_tg')
    kb.row(btn1)
    kb.row(btn2, btn3, btn4)
    kb.row(btn5, btn6, btn7)
    return kb.as_markup(resize_keyboard=True)


def finish_kb():
    kb_list = [
        [KeyboardButton(text="Завершить работу")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        input_field_placeholder="Перед завершением работы нажмите на кнопку"
    )
    return keyboard


def return_to_menu_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=menu_button_text(lang), callback_data='back_to_menu'))
    return kb.as_markup(resize_keyboard=True)


def menu_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=has_code_button_text(lang), callback_data='has_qr'))
    kb.row(InlineKeyboardButton(text=no_code_button_text(lang), callback_data='no_qr'))
    kb.row(InlineKeyboardButton(text=edit_lang_button_text(lang), callback_data='change_lang'))
    return kb.as_markup(resize_keyboard=True)
