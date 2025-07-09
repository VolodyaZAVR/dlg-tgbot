import random
import string
# import hashlib
# import pyqrcode
import re
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
# from aiogram.types.input_file import InputFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.api_service import api_service
from src.services.google_sheets_manager import sheets_manager
from src.services.settings import settings
from src.bot.states import QRcode, Authorization
from src.utils.texts_utils import show_response_error
from src.bot.filters.manage_access import get_stand_chat_ids
from input_format import KeyFormats

# handlers
from src.bot.handlers.menu import back_to_menu

# keyboards
from src.bot.keyboards.qr_code import clear_history_kb, activate_key_kb
from src.bot.keyboards.menu import return_to_menu_kb

# database
from src.database.scripts.authorization import get_user_by_id
from src.database.scripts.orders import orders_check_key_existing, update_orders_key, delete_orders_by_key, \
    select_worker_by_key, find_order_by_key
from src.database.scripts.vehicle_info import update_vehicle_info_key, delete_vehicle_info_by_key, \
    vehicle_info_check_existing_key, select_vehicle_info_by_key

# texts
from src.bot.texts.qr_code import *
from src.bot.texts.menu import user_menu_text
from src.bot.texts.authorization import get_format_messages


router = Router()
router.message.filter(F.chat.type == "private")

logger = logging.getLogger("bot")


@router.callback_query(StateFilter(None), F.data == "no_qr")
async def ask_user_registration(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str):
    await call.message.edit_text(text=user_menu_text(lang))
    await state.set_state(Authorization.licence_input)
    await call.message.answer(text=get_format_messages(lang, 'ru'))  # TODO изменить генерацию текстов


@router.callback_query(StateFilter(None), F.data == "has_qr")
async def has_qr_code(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str):
    await state.set_state(QRcode.scan)
    await call.message.edit_text(text=request_key_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(QRcode.scan, F.data == "back_to_menu")
async def confirm_quit(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str):
    await back_to_menu(call, state, session, lang)


async def generate_unique_6_digit_key(session: AsyncSession):
    # Генерируем 6 случайных цифр
    key = ''.join(random.choices(string.digits, k=6))
    # Проверяем, является ли ключ уникальным
    while True:
        # Проверяем существование ключа в базе данных
        existing_keys = await orders_check_key_existing(session, key)
        if not existing_keys:
            break
        # Если ключ существует, генерим новый
        key = ''.join(random.choices(string.digits, k=6))
    return key


async def generate_key(msg: Message, state: FSMContext, session: AsyncSession, lang: str):
    data = await state.get_data()
    key = await generate_unique_6_digit_key(session)
    # проставляем ключи в записях конкретного юзера
    try:
        if not key:
            raise ValueError("Failed to generate key")
        await update_orders_key(session, data, key)
        await update_vehicle_info_key(session, data, key)
        return key
    except Exception as ex:
        logger.error(f"Произошла ошибка при создании уникального ключа: {str(ex)}")
        return None


async def generate_api_v1_key(session: AsyncSession, data: dict):
    key = await generate_unique_6_digit_key(session)
    # проставляем ключи в записях конкретного юзера
    try:
        if not key:
            raise Exception("Не удалось сгенерировать ключ")
        await update_orders_key(session, data, key)
        await update_vehicle_info_key(session, data, key)
        return key
    except Exception as ex:
        logger.error(f"Произошла ошибка при создании уникального ключа: {str(ex)}")
        await update_orders_key(session, data, key="")
        await update_vehicle_info_key(session, data, key="key")
        return None


async def send_key_to_user(msg: Message, state: FSMContext, session: AsyncSession, lang: str, user_id):
    key = await generate_key(msg, state, session, lang)
    try:
        if not key:
            raise Exception("Failed to generate key")
        else:
            if user_id in get_stand_chat_ids():
                await state.update_data(key=key)
                await msg.answer(text=activate_key_text(lang, key), reply_markup=activate_key_kb(lang))
            else:
                await msg.answer(text=write_code_text(lang, key), reply_markup=return_to_menu_kb(lang))
                await state.clear()
    except Exception as ex:
        logger.error(f"Произошла ошибка при отправке ключа: {ex}")
        await msg.answer(text=failed_generate_key_text(lang), reply_markup=return_to_menu_kb(lang))
        await state.clear()


@router.message(QRcode.scan)
async def scan_key(msg: Message, session: AsyncSession, lang: str):
    key = msg.text.lower()
    tpl = KeyFormats.key
    if re.match(tpl, key) is not None:
        await activate_key(msg, session, lang, key)
    else:
        await msg.answer(text=incorrect_key_text(lang), reply_markup=return_to_menu_kb(lang))


async def delete_rows_by_key(msg: Message, session: AsyncSession, lang: str, key):
    deleted_count = await delete_orders_by_key(session, key)
    deleted_count += await delete_vehicle_info_by_key(session, key)
    if (deleted_count > 0 and
            not await orders_check_key_existing(session, key) and
            not await vehicle_info_check_existing_key(session, key)):
        await msg.answer(text=successful_activation_text(lang), reply_markup=clear_history_kb(lang))
    else:
        raise Exception(f"Произошла ошибка в удалении заявок. Количество удалений: {deleted_count}")


async def activate_key(msg: Message, session: AsyncSession, lang: str, key):
    try:
        # collect user data
        worker_id = await select_worker_by_key(session, key)
        if worker_id is None:
            raise Exception(f"Не найден пользователь по QR коду. Ключ: {key}")
        else:
            vehicle_info = await select_vehicle_info_by_key(session, key)
            if vehicle_info is None:
                raise Exception(f"Не найдена информация о ТС по ключу: {key}")
            else:
                user = await get_user_by_id(session, worker_id)
                order = await find_order_by_key(session, key)
                data = {'licence_series': user.licence_series,
                        'licence_number': user.licence_number,
                        'contact_point': order.contact_point,
                        'job_type': order.job_type,
                        'use_orders': order.use_orders,
                        'partner': order.partner,
                        'key': key,
                        'vehicle_number': vehicle_info.vehicle_number,
                        'has_trailer': vehicle_info.has_trailer,
                        'trailer_number': vehicle_info.trailer_number,
                        'trailer_weight': vehicle_info.trailer_weight
                        }
        if not data:
            raise Exception(f"Ошибка в получении данных от пользователя")

        # check if partner is from sheets
        if order.partner == settings.google_sheet["partner"]:
            if sheets_manager.is_online:
                await sheets_manager.write_data_to_row(session, data)
            else:
                await msg.answer(text=contact_dispatcher_text(lang) + "\nНет ответа от сервиса проверки заявок.",
                                 reply_markup=clear_history_kb(lang))
                return
        else:
            # collect data and send it to api
            response = await api_service.send_full_data_to_api(session, data)
            if not response:
                await msg.answer(text=contact_dispatcher_text(lang) + "\nНет ответа от сервиса проверки заявок.",
                                 reply_markup=clear_history_kb(lang))
                return
            if response['is_error']:
                await msg.answer(text=contact_dispatcher_text(lang) + show_response_error(response["error"]),
                                 reply_markup=clear_history_kb(lang))
                return
        await delete_rows_by_key(msg, session, lang, key)
    except Exception as ex:
        logger.error(f"Ошибка в считывании кода активации: {ex}", exc_info=True)
        await msg.answer(text=contact_dispatcher_text(lang) + failed_activation_text(lang),
                         reply_markup=clear_history_kb(lang))


# async def generate_qr_code(session: AsyncSession):
#     # Генерируем уникальный 6-значный ключ
#     key = await generate_unique_6_digit_key(session)
#
#     # Создаем hash-значение для набора заявок
#     record_hash = hashlib.md5(key.encode()).hexdigest()
#
#     # Создаем URL для удаления заявок
#     delete_url = f"/delete/{record_hash}?key={key}"
#
#     # Генерируем QR-код
#     qr = pyqrcode.create(delete_url)
#
#     qr_dir = os.getenv('QR_FOLDER')
#     os.makedirs(qr_dir, exist_ok=True)
#     # Сохраняем QR-код в файл
#     filename = os.path.join(qr_dir, f"qr_{key}.png")
#     qr.png(filename, scale=6)
#
#     return filename, key

# qr not used right now
# async with aiofiles.open(filename, mode='rb') as file:
#     qr_image = await file.read()
# buffered_input_file = BufferedInputFile(qr_image, filename)
# await msg.answer_photo(buffered_input_file, caption=get_create_qr_text(lang) + key)
# await msg.answer(text=get_to_menu_text(lang), reply_markup=get_menu_kb(lang))
# await state.clear()
# finally:
#     # Удаляем QR после отправки
#     os.remove(filename)
