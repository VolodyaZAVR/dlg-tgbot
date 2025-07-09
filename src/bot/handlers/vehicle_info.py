import re
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboards.qr_code import clear_history_kb
from src.bot.states import VehicleInfo
from input_format import RegistrationFormats
from src.bot.texts.qr_code import contact_dispatcher_text
from src.utils.texts_utils import get_weight, format_name
from src.utils.input_formats import VehicleFormat, is_formated_number

# handlers
from src.bot.handlers.qr_code import send_key_to_user, activate_key, generate_key

# database #
from src.database.scripts.authorization import get_user
from src.database.scripts.orders import get_any_order
from src.database.scripts.vehicle_info import add_vehicle_info
from src.database.scripts.registration import update_name, update_surname, update_middle_name, update_number

# keyboards #
from src.bot.keyboards.orders import get_yes_no_kb
from src.bot.keyboards.menu import return_to_menu_kb
from src.bot.keyboards.registration import skip_middle_name_kb
from src.bot.keyboards.vehicle_info import weight_kb, select_vehicle_format_kb, activate_code_kb, edit_vehicle_info_kb, \
    create_code_kb, edit_vehicle_number_kb, edit_trailer_info_kb, edit_personal_data_kb, select_trailer_format_kb

# texts #
from src.bot.texts.vehicle_info import *
from src.bot.texts.registration import *
from src.bot.texts.common import get_no_callback_text

router = Router()
router.message.filter(F.chat.type == "private")

logger = logging.getLogger("bot")


async def ask_vehicle_numer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    # we are still in state Orders
    orders_data = await state.get_data()
    await state.set_state(VehicleInfo.select_format_vehicle)
    await state.update_data(licence_series=orders_data['licence_series'])
    await state.update_data(licence_number=orders_data['licence_number'])
    await state.update_data(contact_point=orders_data['contact_point'])
    await state.update_data(job_type=orders_data['job_type'])
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=ask_vehicle_format(lang), reply_markup=select_vehicle_format_kb(lang))


@router.callback_query(VehicleInfo.select_format_vehicle, F.data.startswith("vehicle_"))
async def set_vehicle_number_format(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        selected_format = call.data.split('_')[1]
        await state.update_data(select_format_vehicle=selected_format)
        await state.set_state(VehicleInfo.vehicle_number)
        await call.message.edit_text(text=ask_vehicle_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected input vehicle format error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.message(VehicleInfo.vehicle_number)
async def set_vehicle_number(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        selected_format = data['select_format_vehicle']
        vehicle_number = msg.text.strip().upper()

        if VehicleFormat.validate_vehicle(selected_format, vehicle_number):
            await state.update_data(vehicle_number=vehicle_number)
            await state.set_state(VehicleInfo.trailer)
            await msg.answer(text=get_lang_indicate_trailer(lang), reply_markup=get_yes_no_kb(lang))
        else:
            await msg.answer(text=incorrect_vehicle_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected input vehicle number error: {e}")
        await state.clear()
        await msg.answer(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(VehicleInfo.trailer, F.data == "yes")
async def set_has_trailer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.select_format_trailer)
    await state.update_data(trailer=True)
    await call.message.edit_text(text=ask_trailer_format(lang), reply_markup=select_trailer_format_kb(lang))


@router.callback_query(VehicleInfo.trailer, F.data == "no")
async def set_no_trailer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.vehicle_weight)
    await state.update_data(trailer=False)
    await state.update_data(trailer_number="")
    await call.message.edit_text(text=get_lang_load_capacity_class(lang), reply_markup=weight_kb(lang))


@router.callback_query(VehicleInfo.select_format_trailer, F.data.startswith("trailer_"))
async def set_trailer_format(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        await state.set_state(VehicleInfo.trailer_number)
        selected_format = call.data.split('_')[1]
        await state.update_data(select_format_trailer=selected_format)
        await call.message.edit_text(text=ask_trailer_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected trailer format selection error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.message(VehicleInfo.trailer_number)
async def set_trailer_number(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        selected_format = data['select_format_trailer']
        trailer_number = msg.text.strip().upper()

        if VehicleFormat.validate_trailer(selected_format, trailer_number):
            await state.update_data(trailer_number=trailer_number)
            await state.set_state(VehicleInfo.vehicle_weight)
            await msg.answer(text=get_lang_load_capacity_class(lang), reply_markup=weight_kb(lang))
        else:
            await msg.answer(text=incorrect_trailer_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected input trailer number error: {e}")
        await state.clear()
        await msg.answer(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data.startswith("weight_"))
async def set_trailer_weight(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(trailer_weight=get_weight(call.data))
    await call.message.edit_reply_markup(reply_markup=None)
    await show_trailer_info(call.message, state, session, lang, call.from_user.id)


@router.callback_query(VehicleInfo.vehicle_weight, F.data.in_(["edit", "step_back"]))
async def show_edit_vehicle_info_kb(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=edit_vehicle_info_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_vehicle_info")
async def show_edit_vehicle_number_kb(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=edit_vehicle_number_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_personal_info")
async def show_edit_personal_data_kb(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=edit_personal_data_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_trailer_info")
async def show_edit_trailer_info_kb(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=edit_trailer_info_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "back")
async def show_request_qr_kb(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=create_code_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_weight")
async def edit_trailer_weight(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_text(text=get_lang_load_capacity_class(lang), reply_markup=weight_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_name")
async def edit_name_lbc(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_name)
    await call.message.edit_text(text=get_enter_name_text(lang))


@router.message(VehicleInfo.edit_name)
async def set_edited_name_lbc(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    name = format_name(msg.text)
    tpl = RegistrationFormats.name
    if re.match(tpl, name):
        await state.update_data(edit_name=name)
        await state.set_state(VehicleInfo.vehicle_weight)
        await update_name(session, await state.get_data())
        await show_trailer_info(msg, state, session, lang, msg.from_user.id)
    else:
        await msg.answer(text=get_incorrect_name_text(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_surname")
async def edit_surname_lbc(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_surname)
    await call.message.edit_text(text=get_enter_surname_text(lang))


@router.message(VehicleInfo.edit_surname)
async def set_edited_surname_lbc(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    surname = format_name(msg.text)
    tpl = RegistrationFormats.surname
    if re.match(tpl, surname):
        await state.update_data(edit_surname=surname)
        await state.set_state(VehicleInfo.vehicle_weight)
        await update_surname(session, await state.get_data())
        await show_trailer_info(msg, state, session, lang, msg.from_user.id)
    else:
        await msg.answer(text=get_incorrect_surname_text(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_middle_name")
async def edit_middle_name_lbc(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_middle_name)
    await call.message.edit_text(text=get_enter_middle_name_text(lang), reply_markup=skip_middle_name_kb(lang))


@router.message(VehicleInfo.edit_middle_name)
async def set_edited_middle_name_lbc(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    middle_name = format_name(msg.text)
    tpl = RegistrationFormats.middle_name
    if re.match(tpl, middle_name):
        await state.update_data(edit_middle_name=middle_name)
        await state.set_state(VehicleInfo.vehicle_weight)
        await update_middle_name(session, await state.get_data())
        await show_trailer_info(msg, state, session, lang, msg.from_user.id)
    else:
        await msg.answer(text=get_incorrect_middle_name_text(lang))


# Выбрана опция нет отчества #
@router.callback_query(VehicleInfo.edit_middle_name, F.data == "skip")
async def set_edited_no_middle_name_lbc(call: CallbackQuery, state: FSMContext, session: AsyncSession,
                                        lang: str) -> None:
    await state.update_data(edit_middle_name="")
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(VehicleInfo.vehicle_weight)
    await update_middle_name(session, await state.get_data())
    await show_trailer_info(call.message, state, session, lang, call.from_user.id)


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_number")
async def edit_number_lbc(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_number)
    await call.message.edit_text(text=get_user_number_text(lang))


@router.message(VehicleInfo.edit_number)
async def set_edited_number_lbc(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    number = msg.text.lower()
    if is_formated_number(number):
        await state.update_data(edit_number=number)
        await state.set_state(VehicleInfo.vehicle_weight)
        await update_number(session, await state.get_data())
        await show_trailer_info(msg, state, session, lang, msg.from_user.id)
    else:
        await msg.answer(text=get_incorrect_user_number_text(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_vehicle_format")
async def edit_vehicle_number_format(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_format_vehicle)
    await call.message.edit_text(text=ask_vehicle_format(lang), reply_markup=select_vehicle_format_kb(lang))


@router.callback_query(VehicleInfo.edit_format_vehicle, F.data.startswith("vehicle_"))
async def set_new_vehicle_number_format(call: CallbackQuery, state: FSMContext, session: AsyncSession,
                                        lang: str) -> None:
    try:
        selected_format = call.data.split('_')[1]
        await state.update_data(select_format_vehicle=selected_format)
        await state.set_state(VehicleInfo.edit_vehicle_number)
        await call.message.edit_text(text=ask_vehicle_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit vehicle number format error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_vehicle_number")
async def edit_vehicle_number(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        selected_format = data['select_format_vehicle']
        await state.set_state(VehicleInfo.edit_vehicle_number)
        await call.message.edit_text(text=ask_vehicle_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit vehicle number error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.message(VehicleInfo.edit_vehicle_number)
async def set_new_vehicle_number(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        selected_format = data['select_format_vehicle']
        vehicle_number = msg.text.strip().upper()

        if VehicleFormat.validate_vehicle(selected_format, vehicle_number):
            await state.update_data(vehicle_number=vehicle_number)
            await state.set_state(VehicleInfo.vehicle_weight)
            await show_trailer_info(msg, state, session, lang, msg.from_user.id)
        else:
            await msg.answer(text=incorrect_vehicle_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit vehicle number error: {e}")
        await state.clear()
        await msg.answer(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_trailer")
async def edit_trailer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_trailer)
    await call.message.edit_text(text=get_lang_indicate_trailer(lang), reply_markup=get_yes_no_kb(lang))


@router.callback_query(VehicleInfo.edit_trailer, F.data == "yes")
async def set_new_has_trailer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(trailer=True)
    await edit_trailer_format(call, state, session, lang)


@router.callback_query(VehicleInfo.edit_trailer, F.data == "no")
async def set_new_no_trailer(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.vehicle_weight)
    await state.update_data(trailer=False)
    await state.update_data(trailer_number="")
    await call.message.edit_reply_markup(reply_markup=None)
    await show_trailer_info(call.message, state, session, lang, call.from_user.id)


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_trailer_format")
async def edit_trailer_format(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(VehicleInfo.edit_format_trailer)
    await call.message.edit_text(text=ask_trailer_format(lang), reply_markup=select_trailer_format_kb(lang))


@router.callback_query(VehicleInfo.edit_format_trailer, F.data.startswith("trailer_"))
async def set_new_trailer_format(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        await state.set_state(VehicleInfo.edit_trailer_number)
        selected_format = call.data.split('_')[1]
        await state.update_data(select_format_trailer=selected_format)
        await call.message.edit_text(text=ask_trailer_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit trailer format error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "edit_trailer_number")
async def edit_trailer_number(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        if not data['trailer']:
            await edit_trailer(call, state, session, lang)
        else:
            selected_format = data['select_format_trailer']
            await state.set_state(VehicleInfo.edit_trailer_number)
            await call.message.edit_text(text=ask_trailer_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit trailer number error: {e}")
        await state.clear()
        await call.message.edit_text(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


@router.message(VehicleInfo.edit_trailer_number)
async def input_edit_trailer_num_correct(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        data = await state.get_data()
        selected_format = data['select_format_trailer']
        trailer_number = msg.text.strip().upper()

        if VehicleFormat.validate_trailer(selected_format, trailer_number):
            await state.update_data(trailer_number=trailer_number)
            await state.set_state(VehicleInfo.vehicle_weight)
            await show_trailer_info(msg, state, session, lang, msg.from_user.id)
        else:
            await msg.answer(text=incorrect_trailer_number(lang, selected_format))

    except Exception as e:
        logger.error(f"Unexpected edit trailer number error: {e}")
        await state.clear()
        await msg.answer(text=get_no_callback_text(lang), reply_markup=return_to_menu_kb(lang))


async def show_trailer_info(msg: Message, state: FSMContext, session: AsyncSession, lang: str, chat_id) -> None:
    data = await state.get_data()
    user = await get_user(session, data)
    order_data = await get_any_order(session, data)
    if chat_id in get_stand_chat_ids():
        await msg.answer(text=show_full_info_vehicle(lang, data, user, order_data, data.get('orders'), chat_id),
                         reply_markup=activate_code_kb(lang))
    else:
        await msg.answer(text=show_full_info_vehicle(lang, data, user, order_data, data.get('orders'), chat_id),
                         reply_markup=create_code_kb(lang))


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "create_code")
async def create_code_request(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    await add_vehicle_info(session, data)
    await send_key_to_user(call.message, state, session, lang, call.from_user.id)


@router.callback_query(VehicleInfo.vehicle_weight, F.data == "activate_code")
async def run_key_activation(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str):
    try:
        await call.message.edit_reply_markup(reply_markup=None)
        data = await state.get_data()
        await add_vehicle_info(session, data)
        key = await generate_key(call.message, state, session, lang)
        if not key:
            raise ValueError("Не удалось создать ключ активации")
        await activate_key(call.message, session, lang, key)
    except ValueError as ve:
        logger.error(f"Не был создан ключ для активации: {ve}")
        await call.message.answer(text=contact_dispatcher_text(lang) + "\nНе удалось сгенерировать код активации.",
                                  reply_markup=clear_history_kb(lang))
    except Exception as ex:
        logger.error(f"Получено ошибка при активации ключа: {ex}")
        await call.message.answer(text=contact_dispatcher_text(lang) + "\nНе удалось сгенерировать код активации.",
                                  reply_markup=clear_history_kb(lang))
