import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

# custom imports
from src.bot.states import Orders
from src.services.api_service import api_service
from src.services.google_sheets_manager import sheets_manager
from src.services.settings import settings

from src.utils.input_formats import validate_orders_numbers, validate_order
from src.utils.texts_utils import show_response_error, is_any_false_status, get_orders_type, get_job_type, \
    get_contact_point
# handlers
from src.bot.handlers.vehicle_info import ask_vehicle_numer
# keyboards
from src.bot.keyboards.orders import *
from src.bot.keyboards.menu import return_to_menu_kb
# database
from src.database.scripts.orders import add_fast_reg_orders
# texts
from src.bot.texts.orders import *
from src.bot.texts.qr_code import contact_dispatcher_text

router = Router()
router.message.filter(F.chat.type == "private")

logger = logging.getLogger("bot")


async def enter_contact_point(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    data = await state.get_data()
    await state.set_state(Orders.contact_point)
    await state.update_data(licence_series=data['licence_series'])
    await state.update_data(licence_number=data['licence_number'])
    await state.update_data(partner="")
    await msg.answer(text=ask_point_text(lang), reply_markup=get_contact_point_kb(lang))


@router.callback_query(Orders.contact_point, F.data.startswith("point_"))
async def enter_job_type(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(contact_point=get_contact_point(call.data))
    await state.set_state(Orders.job_type)
    await call.message.edit_text(text=ask_job_type_text(lang), reply_markup=get_job_type_kb(lang))


@router.callback_query(Orders.job_type, F.data.startswith("type_"))
async def enter_order(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(job_type=get_job_type(call.data))
    await state.update_data(use_orders=get_orders_type(call.data))
    await state.set_state(Orders.order)
    await call.message.edit_text(text=ask_order_text(lang))


@router.message(Orders.order)
async def input_orders(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    try:
        orders_data = await validate_orders_numbers(msg.text, state, [])
    except ValueError as ex:
        logger.error(f"Ошибка ввода заявок {ex}", exc_info=True)
        await msg.answer(text=f"{ex}\nПовторите ввод ещё раз.")
        return
    try:
        await state.set_state(Orders.confirm)
        await msg.answer(text=get_orders_info_text(lang, orders_data), reply_markup=get_checkin_kb(lang))
    except Exception as ex:
        logger.error(f"Orders input error: {ex}")
        await state.clear()
        await msg.answer(text=get_order_error_text(lang), reply_markup=return_to_menu_kb(lang))


""" show info handlers """


async def show_orders(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    orders_data = await state.get_data()
    try:
        await call.message.edit_text(text=get_orders_info_text(lang, orders_data), reply_markup=get_checkin_kb(lang))
    except Exception as ex:
        logger.error(f"Show orders error: {ex}")
        await state.clear()
        await call.message.edit_text(text=get_order_error_text(lang), reply_markup=return_to_menu_kb(lang))


async def show_orders_using_msg(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    if await state.get_state() != Orders.confirm:
        await state.set_state(Orders.confirm)
    orders_data = await state.get_data()
    try:
        await msg.answer(text=get_orders_info_text(lang, orders_data), reply_markup=get_checkin_kb(lang))
    except Exception as ex:
        logger.error(f"Show orders error: {ex}")
        await state.clear()
        await msg.answer(text=get_order_error_text(lang), reply_markup=return_to_menu_kb(lang))


async def show_orders_with_status(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    data = await state.get_data()
    try:
        if data.get('partner') != "":
            await call.message.answer(text=get_full_info_text(lang, data),
                                      reply_markup=get_commit_kb(lang))
        else:
            await call.message.answer(text=get_orders_with_status_text(lang, data),
                                      reply_markup=get_checkin_kb(lang))
    except Exception as ex:
        logger.error(f"Show orders with status error: {ex}")
        await state.clear()
        await call.message.answer(text=get_order_error_text(lang), reply_markup=return_to_menu_kb(lang))


async def show_partners(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    data = await state.get_data()
    try:
        await call.message.answer(text=get_partners_text(lang, data), reply_markup=get_checkin_kb(lang))
    except Exception as ex:
        logger.error(f"Ошибка получения заявок с указанным контрагентом: {ex}", exc_info=True)
        await state.clear()
        await call.message.answer(text=get_order_error_text(lang), reply_markup=return_to_menu_kb(lang))


@router.callback_query(Orders.confirm, F.data == "edit_point")
async def edit_contact_point(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(Orders.edit_contact_point)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=ask_point_text(lang), reply_markup=get_contact_point_kb(lang))


@router.callback_query(Orders.edit_contact_point, F.data.startswith("point_"))
async def set_updated_contact_point(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(contact_point=get_contact_point(call.data))
    await state.set_state(Orders.confirm)
    await show_orders(call, state, session, lang)


@router.callback_query(Orders.confirm, F.data == "edit_job_type")
async def edit_job_type(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(Orders.edit_job_type)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=ask_job_type_text(lang), reply_markup=get_job_type_kb(lang))


@router.callback_query(Orders.edit_job_type, F.data.startswith("type_"))
async def set_updated_job_type(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(job_type=get_job_type(call.data))
    await state.update_data(use_orders=get_orders_type(call.data))
    await state.set_state(Orders.confirm)
    await show_orders(call, state, session, lang)


""" Change keyboard handlers """


@router.callback_query(Orders.confirm, F.data == "back")
async def back_from_edit_menu(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=get_checkin_kb(lang))


@router.callback_query(Orders.confirm, F.data.in_(["edit", "step_back"]))
async def get_data_to_edit(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=get_edit_kb(lang))


@router.callback_query(Orders.confirm, F.data == "edit_order")
async def edit_order(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=get_edit_order_kb(lang))


@router.callback_query(Orders.confirm, F.data == "edit_orders")
async def edit_order(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=get_edit_order_with_partners_kb(lang))


@router.callback_query(Orders.confirm, F.data == "back_to_commit")
async def edit_order(call: CallbackQuery, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=get_commit_kb(lang))


""" Edit orders handlers """


@router.callback_query(Orders.confirm, F.data == "add_order")
async def add_order_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(Orders.add_order)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_enter_application_number_to_add_text(lang))


@router.message(Orders.add_order)
async def add_new_order(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    data = await state.get_data()
    try:
        orders_data = await validate_orders_numbers(msg.text, state, data.get("orders"))
    except ValueError as ex:
        logger.error(f"Ошибка ввода заявок {ex}", exc_info=True)
        await msg.answer(text=f"{ex}\nПовторите ввод ещё раз.")
        return
    await state.set_state(Orders.confirm)
    await show_orders_using_msg(msg, state, session, lang)


@router.callback_query(Orders.confirm, F.data == "delete_order")
async def delete_order_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(Orders.order_to_delete)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_enter_application_number_to_delete_text(lang))


@router.message(Orders.order_to_delete)
async def get_order_to_delete(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    """
    Обрабатывает удаление заявки из списка.
    :param msg: Сообщение от пользователя.
    :param state: Состояние FSM.
    :param session: Асинхронная сессия подключения к БД.
    :param lang: Язык ответа.
    """
    try:
        order_number_to_delete = validate_order(msg.text.strip())  # Сохраняем номер удаляемой заявки
    except ValueError:
        await msg.answer(text=get_incorrect_order_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)
        return

    data = await state.get_data()  # Получаем текущие данные состояния
    orders = data.get("orders", [])  # Получаем список заявок или пустой список, если его нет

    # Находим индекс заявки по номеру
    order_number_to_delete = msg.text.strip()
    found_index = None
    for index, order in enumerate(orders):
        if order["Number"] == order_number_to_delete:
            found_index = index
            break

    if found_index is not None:
        # Удаляем заявку из списка
        deleted_order = orders.pop(found_index)
        logger.info(f"Заявка {deleted_order['Number']} успешно удалена.")

        # Проверяем, остались ли ещё заявки
        if not orders:
            await state.set_state(Orders.order)
            await msg.answer(text=get_all_orders_deleted_text(lang))
        else:
            await state.set_state(Orders.confirm)
            await state.update_data(orders=orders)  # Обновляем состояние с новым списком заявок
            await show_orders_using_msg(msg, state, session, lang)
    else:
        # Заявка не найдена
        await msg.answer(text=get_no_match_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)


@router.callback_query(Orders.confirm, F.data == "select_order")
async def select_order_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    """
    Начинает процесс редактирования заявки.
    :param call: Колбэк-запрос от пользователя.
    :param state: Состояние FSM.
    :param session: Асинхронная сессия подключения к БД.
    :param lang: Язык ответа.
    """
    await state.set_state(Orders.order_to_edit)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_enter_application_number_text(lang))


@router.message(Orders.order_to_edit)
async def get_order_to_edit_handler(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    """
    Обрабатывает выбор заявки для редактирования.
    :param msg: Сообщение от пользователя.
    :param state: Состояние FSM.
    :param session: Асинхронная сессия подключения к БД.
    :param lang: Язык ответа.
    """
    try:
        order_number_to_edit = validate_order(msg.text.strip())
    except ValueError:
        await msg.answer(text=get_incorrect_order_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)
        return

    orders = (await state.get_data()).get("orders", [])

    # Находим индекс заявки по номеру
    found_index = None
    for index, order in enumerate(orders):
        if order["Number"] == order_number_to_edit:
            found_index = index
            break

    if found_index is not None:
        # Сохраняем индекс заявки для дальнейшего редактирования
        await state.update_data(order_to_edit=found_index)
        await state.set_state(Orders.edit_order)
        await msg.answer(text=get_enter_new_order_number_text(lang))
    else:
        # Заявка не найдена
        await msg.answer(text=get_no_match_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)


@router.message(Orders.edit_order)
async def edit_order_handler(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    """
    Обрабатывает новый номер заявки и обновляет существующую заявку.
    :param msg: Сообщение от пользователя.
    :param state: Состояние FSM.
    :param session: Асинхронная сессия подключения к БД.
    :param lang: Язык ответа.
    """
    try:
        new_order_number = validate_order(msg.text.strip())
    except ValueError:
        await msg.answer(text=get_incorrect_order_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)
        return

    orders = (await state.get_data()).get("orders", [])
    order_to_edit_index = (await state.get_data()).get("order_to_edit", None)

    if order_to_edit_index is not None and isinstance(order_to_edit_index, int):
        # Обновляем номер заявки
        orders[order_to_edit_index]["Number"] = new_order_number
        logger.info(f"Заявка {new_order_number} успешно отредактирована.")
        await state.update_data(orders=orders)  # Обновляем состояние с новым списком заявок
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)
    else:
        # Не удалось найти индекс заявки для редактирования
        await msg.answer(text=get_no_match_text(lang))
        await state.set_state(Orders.confirm)
        await show_orders_using_msg(msg, state, session, lang)


async def fill_orders_only_true_status(state: FSMContext, response: list):
    orders = (await state.get_data()).get("orders", [])

    for response_order in response:
        status = response_order.get("Status")
        if not status:
            continue
        order_number = response_order.get("Number")
        for order in orders:
            if order["Number"] == order_number:
                order["Status"] = True
    await state.update_data(orders=orders)
    return await state.get_data()


async def fill_orders_status(state: FSMContext, response: list):
    orders = (await state.get_data()).get("orders", [])

    for response_order in response:
        status = response_order.get("Status")
        order_number = response_order.get("Number")
        for order in orders:
            if order["Number"] == order_number:
                order["Status"] = status
    await state.update_data(orders=orders)
    return await state.get_data()


@router.callback_query(Orders.confirm, F.data == "send")
async def check_orders(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    partners = []

    if sheets_manager.is_online:
        data = await sheets_manager.check_orders_existing(state)
        if data.get("partner") == "":
            if await sheets_manager.is_any_order_exists(data["orders"]):
                partners.append(settings.google_sheet["partner"])
                await state.update_data(use_orders=True)

    response = await api_service.send_orders_to_api(data)
    try:
        if not response:
            raise Exception(contact_dispatcher_text(lang) + "\nНет ответа от сервиса проверки заявок.")

        if response["is_error"]:
            raise Exception(contact_dispatcher_text(lang) + show_response_error(response["error"]))

        if data.get("partner") != settings.google_sheet["partner"] and data.get("partner") != "":
            data = await fill_orders_status(state, response["payload"])
            if is_any_false_status(data["orders"]):
                await show_orders_with_status(call, state, session, lang)
                return

        if data.get("partner") == "":
            data = await fill_orders_only_true_status(state, response["payload"])
            if len(response['partners']) != 0:
                for partner in response['partners']:
                    partners.append(partner)
            await state.update_data(use_orders=response['use_orders'])

        if not isinstance(partners, list):
            raise Exception(contact_dispatcher_text(lang) +
                            "\nОшибка при получении списка контрагентов: не пришел список контрагентов.")

        if data.get("partner") != "":
            if data.get("partner") == settings.google_sheet["partner"]:
                await state.update_data(use_orders=True)
            await show_orders_with_status(call, state, session, lang)
            return

        if not partners or len(partners) == 0:
            await state.update_data(partner="")
            raise Exception(contact_dispatcher_text(lang) + "\nНе найдено ни одного контрагента.")

        if len(partners) > 7:
            await state.update_data(partner="")
            raise Exception(contact_dispatcher_text(lang) + "\nСлишком много контрагентов.")

        if len(partners) == 1:
            if partners[0] == settings.google_sheet["partner"]:
                await state.update_data(use_orders=True)
            await state.update_data(partner=partners[0])  # api send partners in list
            await show_orders_with_status(call, state, session, lang)
        else:
            # Выбор контрагента если таковых больше одного
            await state.update_data(partner=partners)
            await call.message.answer(text=ask_partner_text(lang), reply_markup=generate_kb(partners))
    except Exception as ex:
        logger.error(f"Ошибка при обработке данных с апи: {ex}")
        if response:
            await call.message.edit_text(f"{ex}")
            await show_orders_with_status(call, state, session, lang)
        else:
            await show_orders(call, state, session, lang)
            await call.message.answer(f"{ex}")


@router.callback_query(Orders.confirm, F.data.startswith("button_"))
async def set_selected_partner(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    partner = data['partner'][int(call.data[-1])]
    await state.update_data(partner=partner)
    await show_partners(call, state, session, lang)


@router.callback_query(Orders.confirm, F.data == "reset_partner")
async def reset_partners(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.update_data(partner="")
    await show_orders(call, state, session, lang)


@router.callback_query(Orders.confirm, F.data == "commit")
async def commit_orders(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    data = await state.get_data()
    if sheets_manager.is_online:
        data = await sheets_manager.check_orders_existing(state)
    response = await api_service.send_orders_to_api(data)
    try:
        if data["partner"] == settings.google_sheet["partner"]:
            if not is_any_false_status(data["orders"]):
                await add_fast_reg_orders(session, await state.get_data())
                await ask_vehicle_numer(call, state, session, lang)
            else:
                raise Exception(contact_dispatcher_text(lang) + "\nНельзя зарегистрироваться на непроверенные заявки.")
        else:
            if not response:
                raise Exception(contact_dispatcher_text(lang) + "\nНет ответа от сервиса проверки заявок.")
            if response["is_error"]:
                raise Exception(contact_dispatcher_text(lang) + show_response_error(response["error"]))

            data = await fill_orders_status(state, response["payload"])
            if not is_any_false_status(data["orders"]):
                await add_fast_reg_orders(session, await state.get_data())
                await ask_vehicle_numer(call, state, session, lang)
            else:
                raise Exception(contact_dispatcher_text(lang) + "\nНельзя зарегистрироваться на непроверенные заявки.")
    except Exception as ex:
        logger.error(f"Ошибка отправки проверенных данных: {ex}, данные на которых произошла ошибка: {data}")
        if response:
            await call.message.edit_reply_markup(reply_markup=None)
            await show_orders_with_status(call, state, session, lang)
            await call.message.answer(f"{ex}")
        else:
            await show_orders(call, state, session, lang)
            await call.message.answer(f"{ex}")
