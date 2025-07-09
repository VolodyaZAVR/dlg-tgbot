from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.texts.orders import *
from src.bot.texts.authorization import go_back_kb_text


def get_contact_point_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_first_point_kb_text(lang), callback_data='point_1'))
    kb.row(InlineKeyboardButton(text=get_second_point_kb_text(lang), callback_data='point_2'))
    kb.row(InlineKeyboardButton(text=get_third_point_kb_text(lang), callback_data='point_3'))
    kb.row(InlineKeyboardButton(text=get_fourth_point_kb_text(lang), callback_data='point_4'))
    kb.row(InlineKeyboardButton(text=get_fifth_point_kb_text(lang), callback_data='point_5'))
    return kb.as_markup(resize_keyboard=True)


def get_job_type_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_job_first_kb_text(lang), callback_data='type_accept'))
    kb.row(InlineKeyboardButton(text=get_job_second_kb_text(lang), callback_data='type_pickup'))
    return kb.as_markup(resize_keyboard=True)


def get_checkin_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=send_to_review_button_text(lang), callback_data='send'))
    kb.row(InlineKeyboardButton(text=edit_data_button_text(lang), callback_data='edit'))
    return kb.as_markup(resize_keyboard=True)


def get_edit_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_edit_site_kb_text(lang), callback_data='edit_point'))
    kb.row(InlineKeyboardButton(text=get_edit_purpose_of_visit_kb_text(lang), callback_data='edit_job_type'))
    kb.row(InlineKeyboardButton(text=get_edit_applications_kb_text(lang), callback_data='edit_order'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='back'))
    return kb.as_markup(resize_keyboard=True)


def get_edit_order_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_add_application_kb_text(lang), callback_data='add_order'))
    kb.row(InlineKeyboardButton(text=get_edit_application_kb_text(lang), callback_data='select_order'))
    kb.row(InlineKeyboardButton(text=get_delete_application_kb_text(lang), callback_data='delete_order'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='step_back'))
    return kb.as_markup(resize_keyboard=True)


def get_yes_no_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text=get_lang_yes(lang), callback_data='yes'),
        InlineKeyboardButton(text=get_lang_no(lang), callback_data='no')
    )
    return kb.as_markup(resize_keyboard=True)


def generate_kb(partners) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for count, item in enumerate(partners):
        kb.row(InlineKeyboardButton(text=item, callback_data=f'button_{count}'))
    return kb.as_markup(resize_keyboard=True)


def get_commit_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=submit_orders_button_text(lang), callback_data='commit'))
    kb.row(InlineKeyboardButton(text=edit_data_button_text(lang), callback_data='edit_orders'))
    kb.row(InlineKeyboardButton(text=get_reset_partner_kb_text(lang), callback_data='reset_partner'))
    return kb.as_markup(resize_keyboard=True)


def get_edit_order_with_partners_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=get_add_application_kb_text(lang), callback_data='add_order'))
    kb.row(InlineKeyboardButton(text=get_edit_application_kb_text(lang), callback_data='select_order'))
    kb.row(InlineKeyboardButton(text=get_delete_application_kb_text(lang), callback_data='delete_order'))
    kb.row(InlineKeyboardButton(text=go_back_kb_text(lang), callback_data='back_to_commit'))
    return kb.as_markup(resize_keyboard=True)
