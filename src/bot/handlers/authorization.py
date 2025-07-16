import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

# custom imports
from src.bot.states import Authorization
from src.utils.texts_utils import InputUtils
# handlers
from src.bot.handlers.orders import enter_contact_point
from src.bot.handlers.registration import accept_user_licence
# keyboards
from src.bot.keyboards.authorization import auth_kb, confirm_kb
from src.bot.keyboards.menu import return_to_menu_kb
# database
from src.database.scripts.authorization import get_user
# texts
from src.bot.translations.authorization import *
from src.bot.translations.common import get_no_callback_text
from src.utils.validation import DriverValidator

router = Router()
router.message.filter(F.chat.type == "private")

logger = logging.getLogger("bot")


@router.message(Authorization.licence_input)
async def auth_set_licence(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        license_series, license_number = await InputUtils.split_licence_input(msg.text)

        if DriverValidator.validate_full_passport(license_series, license_number):
            await state.update_data(licence_series=license_series, licence_number=license_number)
            await msg.answer(text=show_authorization_info_text(lang, await state.get_data()),
                             reply_markup=auth_kb(lang))
            await state.set_state(Authorization.confirm)
        else:
            await msg.answer(text=get_error_messages(lang, 'ru'))  # TODO изменить генерацию текстов

    except Exception as ex:
        logger.error(f"Ошибка при обработке ввода паспорта: {ex}", exc_info=True)
        await state.clear()
        await msg.answer(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(Authorization.confirm, F.data == "authorization")
async def authorization(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    try:
        user = await get_user(session, data)
        if user:
            await call.message.edit_text(text=show_driver_info_text(lang, user), reply_markup=confirm_kb(lang))
        else:
            await call.message.edit_text(text=need_registration_text(lang))
            await accept_user_licence(call, state, session, lang)
    except Exception as ex:
        logger.error(f"Ошибка при авторизации: {ex}", exc_info=True)
        await state.clear()
        await call.message.answer(text=failed_authorization_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(Authorization.confirm, F.data == "correct_data")
async def continue_to_orders(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await enter_contact_point(call.message, state, session, lang)


@router.callback_query(Authorization.confirm, F.data == "edit_licence")
async def edit_licence(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(Authorization.licence_input)
    await call.message.edit_text(text=get_format_messages(lang, 'ru'))  # TODO изменить генерацию текстов
