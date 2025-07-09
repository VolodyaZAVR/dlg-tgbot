import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import LinkPreviewOptions

# custom imports
from src.bot.states import RegistrationForm, Orders
from src.utils.texts_utils import InputUtils
from src.services.settings import settings
# handlers
from src.bot.handlers.orders import enter_contact_point
# keyboards
from src.bot.keyboards.registration import skip_middle_name_kb, accept_kb, registration_kb, edit_data_kb
from src.bot.keyboards.menu import return_to_menu_kb
# database
from src.database.scripts.registration import reg_user
# text
from src.bot.texts.authorization import *
from src.bot.texts.registration import *
from src.utils.validation import DriverValidator

router = Router()
router.message.filter(F.chat.type == "private")

logger = logging.getLogger("bot")


# Универсальное отображение данных о регистрации для пользователя
async def show_registration_data(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await msg.answer(text=show_full_info(lang, await state.get_data()), reply_markup=registration_kb(lang))


# Запрос подтверждения пользовательского соглашения
async def accept_user_licence(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(RegistrationForm.user_agree)
    await state.update_data(user_agree=False)
    # await state.update_data(selected_format=driver_licence['selected_format'],
    #                         licence_series=driver_licence['licence_series'],
    #                         licence_number=driver_licence['licence_number'])
    link = LinkPreviewOptions(
        is_disabled=False,
        url=settings.bot['user_agree'],
        prefer_small_media=True,
        show_above_text=True)
    await call.message.answer(text=get_user_agree_text(lang), reply_markup=accept_kb(lang),
                              link_preview_options=link)


# Обработчик подтверждения пользовательского соглашения
@router.callback_query(RegistrationForm.user_agree, F.data == "accept")
async def menu_user_data(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(user_agree=True)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_data_list_text(lang))
    await call.message.answer(text=get_enter_surname_text(lang))
    await state.set_state(RegistrationForm.surname)


# Ввели что-то во время ожидания пользовательское соглашение
@router.message(RegistrationForm.user_agree)
async def user_agree_incorrect_input(msg: Message, session: AsyncSession, lang: str) -> None:
    await msg.answer(text=get_incorrect_user_agree_text(lang))

""" Форма ввода данных о водителе """


@router.message(RegistrationForm.surname)
async def set_user_surname(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    surname = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_surname(surname):
        await state.update_data(surname=surname)
        await msg.answer(text=get_enter_name_text(lang))
        await state.set_state(RegistrationForm.name)
    else:
        await msg.answer(text=get_incorrect_surname_text(lang))


@router.message(RegistrationForm.name)
async def set_user_name(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    name = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_name(name):
        await state.update_data(name=name)
        await msg.answer(text=get_enter_middle_name_text(lang), reply_markup=skip_middle_name_kb(lang))
        await state.set_state(RegistrationForm.middle_name)
    else:
        await msg.answer(text=get_incorrect_name_text(lang))


@router.message(RegistrationForm.middle_name)
async def set_user_middle_name(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    middle_name = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_middle_name(middle_name):
        await state.update_data(middle_name=middle_name)
        await msg.answer(text=get_user_number_text(lang))
        await state.set_state(RegistrationForm.number)
    else:
        await msg.answer(text=get_incorrect_middle_name_text(lang))


# Выбрана опция нет отчества
@router.callback_query(RegistrationForm.middle_name, F.data == "skip")
async def set_no_middle_name(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(middle_name="")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_user_number_text(lang))
    await state.set_state(RegistrationForm.number)


@router.message(RegistrationForm.number)
async def set_user_number(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        number = DriverValidator.format_phone_number(msg.text)
        if DriverValidator.validate_phone_number(number):
            await state.update_data(number=number)
            await show_registration_data(msg, state, session, lang)
            await state.set_state(RegistrationForm.confirm)
        else:
            await msg.answer(text=get_incorrect_user_number_text(lang))
    except ValueError:
        await msg.answer(text=get_incorrect_user_number_text(lang))


@router.callback_query(RegistrationForm.confirm, F.data == "registration")
async def registration(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    try:
        await reg_user(session, call, data, lang)
        await state.set_state(Orders.contact_point)
        # await state.update_data(licence_series=data['licence_series'], licence_number=data['licence_number'])

        await call.message.answer(text=get_successful_registration_text(lang))
        await enter_contact_point(call.message, state, session, lang)
    except Exception as ex:
        logger.error(
            f"Невозможно зарегистрировать пользователя с ВУ {data['licence_series']} {data['licence_number']} : {ex}")
        await state.clear()
        await call.message.answer(text=get_unable_to_registration_text(lang), reply_markup=return_to_menu_kb(lang))


""" Функции для перехода между клавиатурами """


@router.callback_query(RegistrationForm.confirm, F.data == "edit")
async def get_data_to_edit(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=edit_data_kb(lang))


@router.callback_query(RegistrationForm.confirm, F.data == "back")
async def get_back_to_reg_menu(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=registration_kb(lang))

""" Функции изменения введенных данных """


@router.callback_query(RegistrationForm.confirm, F.data == "edit_name")
async def edit_name(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationForm.edit_name)
    await call.message.answer(text=get_enter_name_text(lang))


@router.message(RegistrationForm.edit_name)
async def set_edited_user_name(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    name = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_name(name):
        await state.update_data(name=name)
        await show_registration_data(msg, state, session, lang)
        await state.set_state(RegistrationForm.confirm)
    else:
        await msg.answer(text=get_incorrect_name_text(lang))


@router.callback_query(RegistrationForm.confirm, F.data == "edit_surname")
async def edit_surname(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationForm.edit_surname)
    await call.message.answer(text=get_enter_surname_text(lang))


@router.message(RegistrationForm.edit_surname)
async def set_edited_user_surname(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    surname = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_surname(surname):
        await state.update_data(surname=surname)
        await show_registration_data(msg, state, session, lang)
        await state.set_state(RegistrationForm.confirm)
    else:
        await msg.answer(text=get_incorrect_surname_text(lang))


@router.callback_query(RegistrationForm.confirm, F.data == "edit_middle_name")
async def edit_middle_name(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationForm.edit_middle_name)
    await call.message.answer(text=get_enter_middle_name_text(lang), reply_markup=skip_middle_name_kb(lang))


@router.message(RegistrationForm.edit_middle_name)
async def set_edited_user_middle_name(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    middle_name = InputUtils.clear_string(InputUtils.format_name(msg.text))
    if DriverValidator.validate_middle_name(middle_name):
        await state.update_data(middle_name=middle_name)
        await show_registration_data(msg, state, session, lang)
        await state.set_state(RegistrationForm.confirm)
    else:
        await msg.answer(text=get_incorrect_middle_name_text(lang))


# Выбрана опция нет отчества #
@router.callback_query(RegistrationForm.edit_middle_name, F.data == "skip")
async def set_edited_user_no_middle_name(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationForm.confirm)
    await state.update_data(middle_name="")
    await show_registration_data(call.message, state, session, lang)


@router.callback_query(RegistrationForm.confirm, F.data == "edit_number")
async def edit_number(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationForm.number)  # Возвращаемся в state number тк он идет перед подтверждением
    await call.message.answer(text=get_user_number_text(lang))


@router.callback_query(RegistrationForm.confirm, F.data == "edit_licence")
async def edit_user_licence(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(RegistrationForm.licence_input)
    await call.message.edit_text(text=get_format_messages(lang,'ru'))  # TODO изменить генерацию текстов


@router.message(RegistrationForm.licence_input)
async def set_edited_licence(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    license_series, license_number = await InputUtils.split_licence_input(msg.text)

    if DriverValidator.validate_full_passport(license_series, license_number):
        await state.update_data(licence_series=license_series, licence_number=license_number)
        await state.set_state(RegistrationForm.confirm)
        await show_registration_data(msg, state, session, lang)
    else:
        await msg.answer(text=get_error_messages(lang, 'ru'))  # TODO изменить генерацию текстов
