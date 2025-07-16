import re
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.states import Manager
from src.utils.texts_utils import show_orders_with_false_status, is_any_false_status, format_name
from src.utils.validation import validate_vehicle_input, validate_orders, validate_user_data, format_user_data, \
    is_formated_number
from src.utils.input_formats import RegistrationFormats, OrdersFormats, KeyFormats

# handlers
from src.bot.handlers.menu import back_to_menu
from src.bot.handlers.qr_code import generate_unique_6_digit_key
from src.bot.handlers.orders import fill_orders_status

# keyboards
from src.bot.keyboards.manager import manager_kb, search_orders_kb, search_users_kb, edit_user_kb, to_manager_kb
from src.bot.keyboards.registration import skip_middle_name_kb
from src.bot.keyboards.menu import return_to_menu_kb

# database
from src.database.scripts.admin import select_users_by_surname, select_users_by_licence, delete_user_from_db, \
    update_user_name, update_user_surname, update_user_middle_name, update_user_number, select_orders, \
    delete_order_from_db, order_reset_key, add_user, select_orders_by_driver, search_fast_reg_user, add_fast_reg_user, \
    select_users_by_id, add_fast_reg_vehicle, remove_fast_reg_vehicle, \
    update_orders_key_admin, vehicle_reset_key, select_orders_by_key, select_vehicle_by_key
from src.database.scripts.vehicle_info import update_vehicle_info_key
from src.database.scripts.orders import add_fast_reg_orders, remove_fast_reg_orders

# texts
from src.bot.translations.registration import get_enter_name_text, get_incorrect_name_text, get_enter_surname_text, \
    get_incorrect_surname_text, get_enter_middle_name_text, get_incorrect_middle_name_text, get_user_number_text, \
    get_incorrect_user_number_text
from src.bot.translations.orders import get_incorrect_order_text
from src.bot.translations.qr_code import incorrect_key_text, failed_generate_key_text
from src.bot.translations.vehicle_info import show_contact_point, show_trailer_number, show_trailer_weight

from src.services.api_service import api_service
from src.services.settings import settings
from src.services.google_sheets_manager import sheets_manager

from src.bot.filters.manage_access import IsManager
from src.utils.validation import DriverValidator

manager_router = Router()
manager_router.message.filter(F.chat.type == "private")
manager_router.message.filter(IsManager())
manager_router.callback_query.filter(IsManager())

logger = logging.getLogger("bot")


@manager_router.message(Command("manager"))
async def show_manager_panel(
        msg: Message,
        state: FSMContext) -> None:
    await state.clear()
    await msg.answer(text="Вы вошли в менеджер панель!\n\n"
                          "Ваша <b>СИЛА</b> дает вам возможность:\n\n"
                          "<b>Зарегистрировать заявки</b>: быстрая регистрация заявок водителя.\n\n"
                          "<b>Управлять водителями</b>: поиск по Фамилии или номеру паспорта, редактирование записей и "
                          "добавление новых водителей.\n\n"
                          "<b>Управлять заявками</b>: поиск по номеру заявки или по id записи, удалять заявки и "
                          "аннулировать код активации.\n\n"
                          "Выберите ваше действие:", reply_markup=manager_kb())


@manager_router.callback_query(F.data == "exit")
async def exit_manager_panel(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.clear()
    await back_to_menu(call, state, session, lang)


@manager_router.callback_query(F.data == "to_manager_kb")
async def return_main_kb(call: CallbackQuery) -> None:
    await call.message.edit_reply_markup(reply_markup=manager_kb())


@manager_router.callback_query(F.data == "manager_show_users")
async def ask_user_searching(call: CallbackQuery) -> None:
    await call.message.edit_reply_markup(reply_markup=search_users_kb())


@manager_router.callback_query(F.data == "manager_show_orders")
async def ask_order_searching(call: CallbackQuery) -> None:
    await call.message.edit_reply_markup(reply_markup=search_orders_kb())


@manager_router.callback_query(F.data == "manager_by_surname")
async def ask_surname(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите фамилию водителя")
    await state.set_state(Manager.surname_searching)


@manager_router.callback_query(F.data == "manager_by_id")
async def ask_driver_id(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите ID водителя")
    await state.set_state(Manager.id_searching)


@manager_router.callback_query(F.data == "manager_reg_orders")
async def user_fast_activation_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Вы вошли в функцию быстрой регистрации водителя. "
        "Пожалуйста, учтите что как <b>вы введете</b> данные так они и отправятся на проверку!\n"
        "Введите номер и серию паспорта водителя")
    await state.set_state(Manager.fast_activation)


""" 
                                Быстрая регистрация 
"""


@manager_router.message(Manager.fast_activation)
async def find_user(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        licence, number = await DriverValidator.get_passport_form_msg(msg, state)
    except ValueError as ex:
        logger.error(f"Ошибка ввода паспорта {ex}", exc_info=True)
        await msg.answer(text=f"Некорректный ввод данных. Введите паспортные данные в формате <b>Серия Номер</b> "
                              f"(через пробел) ещё раз.")
        return
    try:
        user = await search_fast_reg_user(session, licence, number)

        if user:
            user_data = (f"Фамилия: <b>{user[0].surname}</b>\n"
                         f"Имя: <b>{user[0].name}</b>\n"
                         f"Отчество: <b>{user[0].middle_name}</b>\n"
                         f"Номер телефона: <b>{user[0].number}</b>\n"
                         f"Серия: <b>{user[0].licence_series}</b>\n"
                         f"Номер: <b>{user[0].licence_number}</b>\n\n")
            await state.update_data(name=user[0].name)
            await state.update_data(surname=user[0].surname)
            await state.update_data(middle_name=user[0].middle_name)
            await state.update_data(number=user[0].number)
            await msg.answer(f"Проверьте корректность найденных данных:\n\n" + user_data +
                             f"Для выбранного водителя отправьте заявки для активации в формате "
                             f"<b>Площадка Цель визита Контрагент Заявки</b>\n\n"
                             f"Формат данных:\n"
                             f"<b>Площадка</b> - М19 или М70 или Уткина_Заводь или Открытая_площадка или К8\n"
                             f"<b>Цель визита</b> - Поступление или Возврат\n"
                             f"<b>Контрагент</b> - Название контрагента\n"
                             f"<b>Тип заявок</b> - Заявки или Контейнер\n"
                             f"<b>Заявки</b> - Номера заявок указанные через пробел")
            await state.set_state(Manager.fast_orders)
        else:
            await msg.answer(f"Для быстрой регистрации введите данные водителя:\n\n"
                             f"<b>Фамилия Имя Отчество Номер телефона</b> (через пробел)\n"
                             f"Если у водителя нет отчества - введите один любой символ вместо него.")
            await state.set_state(Manager.fast_registration)
    except Exception as ex:
        logger.error(f"Ошибка быстрой активации {ex}", exc_info=True)
        await msg.answer(f"Ошибка быстрой регистрации. Попробуйте ещё раз.")


@manager_router.message(Manager.fast_registration)
async def fast_reg_user(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        user_data = await validate_user_data(msg.text, state)
    except ValueError as ex:
        logger.error(f"Ошибка ввода информации о водителе {ex}", exc_info=True)
        await msg.answer(text=f"{ex}\nПовторите ввод ещё раз.")
        return
    try:
        await add_fast_reg_user(session, msg, user_data['name'], user_data['surname'], user_data['middle_name'],
                                user_data['number'], user_data['licence_series'], user_data['licence_number'])
        await msg.answer(f"Для зарегистрированного водителя отправьте заявки для активации в одну строку в формате "
                         f"<b>Площадка Цель визита Контрагент Заявки</b>\n\n"
                         f"<b>Площадка</b> - М19 или М70 или Уткина_Заводь или Открытая_площадка или К8\n"
                         f"<b>Цель визита</b> - Поступление или Возврат\n"
                         f"<b>Контрагент</b> - Название контрагента, если в названии есть пробелы замените их на _\n"
                         f"<b>Тип заявок</b> - Заявки или Контейнер\n"
                         f"<b>Заявки</b> - Номера заявок указанные через пробел")
        await state.set_state(Manager.fast_orders)
    except Exception as ex:
        logger.error(f"Ошибка быстрой регистрации {ex}", exc_info=True)
        await msg.answer(f"Некорректный ввод данных. Введите данные ещё раз в формате "
                         f"<b>Фамилия Имя Отчество Номер телефона</b> (через пробел)")


@manager_router.message(Manager.fast_orders)
async def fast_check_orders(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        orders_data = await validate_orders(msg.text, state)
    except ValueError as ex:
        logger.error(f"Ошибка ввода заявок {ex}", exc_info=True)
        await msg.answer(text=f"{ex}\nПовторите ввод ещё раз.")
        return
    try:
        if orders_data["partner"] == settings.google_sheet["partner"]:
            if sheets_manager.is_online:
                orders_data = await sheets_manager.check_orders_existing(state)
            else:
                orders_data = await state.get_data()
        else:
            response = await api_service.send_orders_to_api(orders_data)
            if not response:
                raise Exception("Нет ответа от сервиса проверки заявок.")

            orders_data = await fill_orders_status(state, response["payload"])

        if not is_any_false_status(orders_data["orders"]):
            await msg.answer(f'Для завершении регистрации водителя отправьте данные о ТС в одну строку в формате'
                             f'<b>Номер ТС Номер прицепа Класс грузоподъемности в 1,5 тонны</b>\n\n'
                             f'Формат данных:\n'
                             f'<b>Номер ТС</b> - Введите номер ТС с регионом\n'
                             f'<b>Номер прицепа</b> - Введите номер прицепа либо <b>Нет</b> если нет прицепа\n'
                             f'<b>Класс грузоподъемности в 1,5 тонны</b> - <b>Больше</b> либо <b>Меньше</b>')
            await state.set_state(Manager.fast_vehicle)
        else:
            await msg.answer(f'Следующие заявки не прошли проверку. Повторите попытку ещё раз.\n\n'
                             f'{show_orders_with_false_status(orders_data["orders"])}')
            await remove_fast_reg_orders(session, orders_data)
    except Exception as ex:
        logger.error(f"Ошибка быстрой проверки заявок {ex}", exc_info=True)
        await msg.answer('Возникла ошибка быстрой активации заявок. Повторите попытку ещё раз.')


def show_orders_in_list(orders) -> str:
    text = "Заявки:\n"
    for order in orders:
        text += f"<b>{str(order['Number'])}</b>\n"
    return text


def show_user_data(data):
    return (f"Запишите код активации для водителя, зарегистрированного на:\n\n"
            f"Фамилия: <b>{data['surname']}</b>\n"
            f"Имя: <b>{data['name']}</b>\n"
            f"Отчество: <b>{data['middle_name']}</b>\n"
            f"Номер: <b>{data['number']}</b>\n"
            f"Серия паспорта: <b>{data['licence_series']}</b>\n"
            f"Номер паспорта:<b> {data['licence_number']}</b>\n"
            f"Площадка: <b>{show_contact_point(data['contact_point'], 'ru')}</b>\n"
            f"Цель визита:  <b>{show_job_type_for_admins(data['job_type'], 'ru')}</b>\n"
            + show_orders_in_list(data['orders']) +
            f"Контрагент: <b>{data['partner']}</b>\n"
            f"Номер ТС: <b>{data['vehicle_number']}</b>\n"
            + show_trailer_number('ru', bool(data["trailer"]), data["trailer_number"]) +
            f"Класс грузоподъемности в 1,5 тонны: <b>{show_trailer_weight('ru', data['trailer_weight'])}</b>\n\n")


def show_job_type_for_admins(text: str, lang: str) -> str:
    match text:
        case "Прием":
            return "Поступление"
        case "Отгрузка":
            return "Возврат"
        case default:
            return "Error"


async def generate_key_admin(msg: Message, state: FSMContext, session: AsyncSession, lang: str):
    data = await state.get_data()
    key = await generate_unique_6_digit_key(session)
    # проставляем ключи в записях конкретного юзера
    try:
        await update_orders_key_admin(session, data, key)
        await update_vehicle_info_key(session, data, key)
        return key
    except Exception as ex:
        logger.error(f"Произошла ошибка при создании уникального ключа: {str(ex)}")
        await msg.answer(text=failed_generate_key_text(lang), reply_markup=return_to_menu_kb(lang))
        return None


@manager_router.message(Manager.fast_vehicle)
async def fast_generate_code(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        full_data = await validate_vehicle_input(msg.text, state)
    except ValueError as ex:
        logger.error(f"Ошибка ввода информации о ТС {ex}", exc_info=True)
        await msg.answer(text=f"{ex}\nПовторите ввод ещё раз.")
        return
    try:
        await add_fast_reg_orders(session, full_data)
        await add_fast_reg_vehicle(session, full_data)
    except Exception as ex:
        logger.error(f"Ошибка записи инфо р ТС в базу данных {ex}", exc_info=True)
        await msg.answer(text=f"Произошла ошибка с записью данных о ТС. Повторите попытку ещё раз.")
        await remove_fast_reg_orders(session, full_data)
        await remove_fast_reg_vehicle(session, full_data)
        return
    key = await generate_key_admin(msg, state, session, 'ru')
    if not key:
        return
    await msg.answer(text=show_user_data(full_data) + f"Код активации: <b>{key}</b>", reply_markup=manager_kb())
    await state.clear()


""" 
                                    Пользователи 
"""


@manager_router.message(Manager.id_searching)
async def show_users(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        driver_id = int(msg.text)
        users = await select_users_by_id(session, driver_id)
        text = ""
        for user in users:
            text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                     f"ID водителя: <b>{user[0].id}</b>\n"
                     f"ID чата: <b>{user[0].chat_id}</b>\n"
                     f"Имя: <b>{user[0].name}</b>\n"
                     f"Фамилия: <b>{user[0].surname}</b>\n"
                     f"Отчество: <b>{user[0].middle_name}</b>\n"
                     f"Номер телефона: <b>{user[0].number}</b>\n"
                     f"Серия паспорта: <b>{user[0].licence_series}</b>\n"
                     f"Номер паспорта: <b>{user[0].licence_number}</b>")
        await state.clear()
        await msg.answer(f"Результат поиска по ID {driver_id}:" + text, reply_markup=search_users_kb())
    except Exception as ex:
        logger.error(f"Error in searching driver within ID: {msg.text} {ex}", exc_info=True)
        await msg.answer("Некорректный ввод ID. Введите цифрами ID водителя ещё раз")


@manager_router.message(Manager.surname_searching)
async def show_users(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    surname = format_name(msg.text)
    users = await select_users_by_surname(session, surname)
    text = ""
    for user in users:
        text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                 f"ID водителя: <b>{user[0].id}</b>\n"
                 f"ID чата: <b>{user[0].chat_id}</b>\n"
                 f"Имя: <b>{user[0].name}</b>\n"
                 f"Фамилия: <b>{user[0].surname}</b>\n"
                 f"Отчество: <b>{user[0].middle_name}</b>\n"
                 f"Номер телефона: <b>{user[0].number}</b>\n"
                 f"Серия паспорта: <b>{user[0].licence_series}</b>\n"
                 f"Номер паспорта: <b>{user[0].licence_number}</b>")
    await state.clear()
    await msg.answer(f"Результат поиска по фамилии {surname}:" + text, reply_markup=search_users_kb())


@manager_router.callback_query(F.data == "manager_by_licence")
async def ask_licence(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите паспорт в формате: серия номер (через пробел)")
    await state.set_state(Manager.licence_searching)


@manager_router.message(Manager.licence_searching)
async def show_users(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        licence = msg.text.split(' ')[0]
        number = msg.text.split(' ')[1]
        users = await select_users_by_licence(session, licence, number)
        text = ""
        for user in users:
            text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                     f"ID водителя: <b>{user[0].id}</b>\n"
                     f"ID чата: <b>{user[0].chat_id}</b>\n"
                     f"Имя: <b>{user[0].name}</b>\n"
                     f"Фамилия: <b>{user[0].surname}</b>\n"
                     f"Отчество: <b>{user[0].middle_name}</b>\n"
                     f"Номер телефона: <b>{user[0].number}</b>\n"
                     f"Серия паспорта: <b>{user[0].licence_series}</b>\n"
                     f"Номер паспорта: <b>{user[0].licence_number}</b>")
        await state.clear()
        await msg.answer(f"Результат поиска по паспорту {licence} {number}:" + text, reply_markup=search_users_kb())
    except Exception as ex:
        logger.error(f"Ошибка с удаление пользователя {ex}", exc_info=True)
        await msg.answer("Некорректный ввод паспорта. Введите паспорт в формате серия номер (через пробел)")


@manager_router.callback_query(F.data == "manager_add_user")
async def request_user_data(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите данные о водителе.\n"
                              "Ввод данных производится одним сообщением как указано в примере:\n"
                              "Иван\n"
                              "Иванов\n"
                              "Иванович (или пустая строка)\n"
                              "+79991112233\n"
                              "1234\n"
                              "123456", reply_markup=to_manager_kb())
    await state.set_state(Manager.add_user)


@manager_router.message(Manager.add_user)
async def add_user_to_db(msg: Message, state: FSMContext, session: AsyncSession):
    try:
        user = format_user_data(msg.text)
        await add_user(session, msg, user)
        await state.clear()
        await msg.answer(f"Водитель со следующими данными успешно добавлен!\n\n"
                         f"Имя: <b>{user['name']}</b>\n"
                         f"Фамилия: <b>{user['surname']}</b>\n"
                         f"Отчество: <b>{user['middle_name']}</b>\n"
                         f"Номер телефона: <b>{user['number']}</b>\n"
                         f"Серия паспорта: <b>{user['licence_series']}</b>\n"
                         f"Номер паспорта: <b>{user['licence_number']}</b>\n",
                         reply_markup=search_users_kb())
    except Exception as ex:
        logger.error(f"Ошибка с отображением водителя {ex}", exc_info=True)
        await msg.answer("Не удалось добавить запись. Введите данные водителя ещё раз")


@manager_router.callback_query(Manager.add_user, F.data == "manager_to_user_kb")
async def return_to_manager_panel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_reply_markup(reply_markup=search_users_kb())


@manager_router.callback_query(F.data == "manager_edit_user")
async def select_user(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Выберите водителя данные которого хотите изменить.\n"
                              "Введите паспорт в формате: серия номер (через пробел)")
    await state.set_state(Manager.edit_user)


@manager_router.message(Manager.edit_user)
async def edit_user(msg: Message, state: FSMContext, session: AsyncSession):
    try:
        licence = msg.text.split(' ')[0]
        number = msg.text.split(' ')[1]
        await show_selected_user(msg, state, session, licence, number)
    except Exception as ex:
        logger.error(f"Ошибка с отображением водителя {ex}", exc_info=True)
        await msg.answer("Некорректный ввод паспорта. Введите паспорт в формате серия номер (через пробел)")


async def show_selected_user(msg: Message, state: FSMContext, session: AsyncSession, licence, number):
    users = await select_users_by_licence(session, licence, number)
    text = ""
    for user in users:
        text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                 f"ID водителя: <b>{user[0].id}</b>\n"
                 f"ID чата: <b>{user[0].chat_id}</b>\n"
                 f"Имя: <b>{user[0].name}</b>\n"
                 f"Фамилия: <b>{user[0].surname}</b>\n"
                 f"Отчество: <b>{user[0].middle_name}</b>\n"
                 f"Номер телефона: <b>{user[0].number}</b>\n"
                 f"Серия паспорта: <b>{user[0].licence_series}</b>\n"
                 f"Номер паспорта: <b>{user[0].licence_number}</b>")
    await state.update_data(licence_series=licence)
    await state.update_data(licence_number=number)
    await msg.answer(f"Результат поиска по паспорту {licence} {number}:" + text +
                     "\n\nВыберите какие данные вы хотите изменить", reply_markup=edit_user_kb())


@manager_router.callback_query(Manager.edit_user, F.data == "manager_edit_name")
async def ask_user_edit_name(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Manager.edit_user_name)
    await call.message.answer(text=get_enter_name_text('ru'))


@manager_router.message(Manager.edit_user_name)
async def set_edited_user_name(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    name = format_name(msg.text)
    tpl = RegistrationFormats.name
    if re.match(tpl, name):
        await state.update_data(name=name)
        data = await state.get_data()
        await update_user_name(session, data['licence_series'], data['licence_number'], data['name'])
        await state.set_state(Manager.edit_user)
        await show_selected_user(msg, state, session, data['licence_series'], data['licence_number'])
    else:
        await msg.answer(text=get_incorrect_name_text('ru'))


@manager_router.callback_query(Manager.edit_user, F.data == "manager_edit_surname")
async def ask_user_edit_surname(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Manager.edit_user_surname)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_enter_surname_text('ru'))


@manager_router.message(Manager.edit_user_surname)
async def set_edited_user_surname(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    surname = format_name(msg.text)
    tpl = RegistrationFormats.surname
    if re.match(tpl, surname):
        await state.update_data(surname=surname)
        data = await state.get_data()
        await update_user_surname(session, data['licence_series'], data['licence_number'], data['surname'])
        await state.set_state(Manager.edit_user)
        await show_selected_user(msg, state, session, data['licence_series'], data['licence_number'])
    else:
        await msg.answer(text=get_incorrect_surname_text('ru'))


@manager_router.callback_query(Manager.edit_user, F.data == "manager_edit_middle_name")
async def ask_user_edit_middle_name(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Manager.edit_user_middle_name)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text=get_enter_middle_name_text('ru'), reply_markup=skip_middle_name_kb('ru'))


@manager_router.message(Manager.edit_user_middle_name)
async def set_edited_user_middle_name(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    middle_name = format_name(msg.text)
    tpl = RegistrationFormats.middle_name
    if re.match(tpl, middle_name):
        await state.update_data(middle_name=middle_name)
        data = await state.get_data()
        await update_user_middle_name(session, data['licence_series'], data['licence_number'], data['middle_name'])
        await state.set_state(Manager.edit_user)
        await show_selected_user(msg, state, session, data['licence_series'], data['licence_number'])
    else:
        await msg.answer(text=get_incorrect_middle_name_text('ru'))


# Выбрана опция нет отчества #
@manager_router.callback_query(Manager.edit_user_middle_name, F.data == "skip")
async def set_edited_user_no_middle_name(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(middle_name="")
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    await update_user_middle_name(session, data['licence_series'], data['licence_number'], data['middle_name'])
    await state.set_state(Manager.edit_user)
    await show_selected_user(call.message, state, session, data['licence_series'], data['licence_number'])


@manager_router.callback_query(Manager.edit_user, F.data == "manager_edit_number")
async def ask_user_edit_number(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Manager.edit_user_number)
    await call.message.answer(text=get_user_number_text('ru'))


@manager_router.message(Manager.edit_user_number)
async def set_edited_number(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    number = msg.text.lower()
    if is_formated_number(number):
        await state.update_data(number=number)
        data = await state.get_data()
        await update_user_number(session, data['licence_series'], data['licence_number'], data['number'])
        await state.set_state(Manager.edit_user)
        await show_selected_user(msg, state, session, data['licence_series'], data['licence_number'])
    else:
        await msg.answer(text=get_incorrect_user_number_text('ru'))


@manager_router.callback_query(F.data == "manager_delete_user")
async def ask_user_to_delete(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Manager.delete_user)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите паспорт водителя которого надо удалить в формате серия номер (через пробел)")


@manager_router.message(Manager.delete_user)
async def delete_user(msg: Message, state: FSMContext, session: AsyncSession):
    try:
        licence = msg.text.split(' ')[0]
        number = msg.text.split(' ')[1]
        await state.clear()
        if await delete_user_from_db(session, licence, number):
            await msg.answer(f"Пользователь удален с данными паспорта: {licence} {number}",
                             reply_markup=search_users_kb())
        else:
            await msg.answer(f"Пользователь не удален: не найден пользователь с паспортом {licence} {number}",
                             reply_markup=search_users_kb())
    except Exception as ex:
        logger.error(f"Ошибка с удаление пользователя {ex}", exc_info=True)
        await msg.answer("Некорректный ввод паспорта. Введите паспорт в формате серия номер (через пробел)")


"""  
                                    Заявки 
"""


@manager_router.callback_query(F.data == "manager_show_orders")
async def ask_order_searching(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    await call.message.answer("Выберите ваше действие:", reply_markup=search_orders_kb())


@manager_router.callback_query(F.data == "manager_by_key")
async def ask_key_searching(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите код активации")
    await state.set_state(Manager.order_by_key)


@manager_router.message(Manager.order_by_key)
async def show_orders_by_key(msg: Message, state: FSMContext, session: AsyncSession):
    key = msg.text.strip()
    tpl = KeyFormats.key
    if re.match(tpl, key):
        orders = await select_orders_by_key(session, key)
        vehicles = await select_vehicle_by_key(session, key)
        result = generate_text_from_key_data(orders, vehicles)
        await state.clear()
        await msg.answer(f"Результат поиска с кодом активации {key}:" + result, reply_markup=search_orders_kb())
    else:
        await msg.answer(text=incorrect_key_text('ru'))


def generate_text_from_key_data(orders, vehicles) -> str:
    text = ""
    if orders:
        text += "\nЗаявки:\n\n"
        for item in orders:
            text += (f"ID записи: <b>{item[0].id}</b>\n"
                     f"ID водителя: <b>{item[0].worker_id}</b>\n"
                     f"Точка визита: <b>{item[0].contact_point}</b>\n"
                     f"Тип обращения: <b>{item[0].job_type}</b>\n"
                     f"Номер заявки: <b>{item[0].order}</b>\n"
                     f"Контрагент: <b>{item[0].partner}</b>\n"
                     f"Код: <b>{item[0].key}</b>\n"
                     f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    if vehicles:
        text += "\nДанные о ТС:\n\n"
        for item in vehicles:
            text += (f"ID записи: <b>{item[0].id}</b>\n"
                     f"ID водителя: <b>{item[0].worker_id}</b>\n"
                     f"Номер ТС: <b>{item[0].vehicle_number}</b>\n"
                     f"Наличие прицепа: <b>{item[0].has_trailer}</b>\n"
                     f"Номер прицепа: <b>{item[0].trailer_number}</b>\n"
                     f"Класс грузоподъемности: <b>{item[0].trailer_weight}</b>\n"
                     f"Код: <b>{item[0].key}</b>\n"
                     f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    return text


@manager_router.callback_query(F.data == "manager_by_number")
async def ask_order_number(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите номер заявки")
    await state.set_state(Manager.order_by_number)


@manager_router.message(Manager.order_by_number)
async def show_orders_by_number(msg: Message, state: FSMContext, session: AsyncSession):
    order = msg.text
    tpl = OrdersFormats.order
    if re.match(tpl, order):
        orders = await select_orders(session, order)
        text = ""
        for item in orders:
            text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                     f"ID записи: <b>{item[0].id}</b>\n"
                     f"ID водителя: <b>{item[0].worker_id}</b>\n"
                     f"Точка визита: <b>{item[0].contact_point}</b>\n"
                     f"Тип обращения: <b>{item[0].job_type}</b>\n"
                     f"Номер заявки: <b>{item[0].order}</b>\n"
                     f"Контрагент: <b>{item[0].partner}</b>\n"
                     f"Код: <b>{item[0].key}</b>\n")
        await state.clear()
        await msg.answer(f"Результат поиска заявок с номером {order}:" + text, reply_markup=search_orders_kb())
    else:
        await msg.answer(text=get_incorrect_order_text('ru'))


@manager_router.callback_query(F.data == "manager_by_driver")
async def ask_order_search_by_driver(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите ID водителя")
    await state.set_state(Manager.order_by_driver)


@manager_router.message(Manager.order_by_driver)
async def show_orders_by_driver(msg: Message, state: FSMContext, session: AsyncSession):
    try:
        worker_id = int(msg.text)
        orders = await select_orders_by_driver(session, worker_id)
        text = ""
        for item in orders:
            text += (f"\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                     f"ID записи: <b>{item[0].id}</b>\n"
                     f"ID водителя: <b>{item[0].worker_id}</b>\n"
                     f"Точка визита: <b>{item[0].contact_point}</b>\n"
                     f"Тип обращения: <b>{item[0].job_type}</b>\n"
                     f"Номер заявки: <b>{item[0].order}</b>\n"
                     f"Контрагент: <b>{item[0].partner}</b>\n"
                     f"Код: <b>{item[0].key}</b>\n")
        await state.clear()
        await msg.answer(f"Результат поиска заявок с ID водителя {worker_id}:" + text, reply_markup=search_orders_kb())
    except Exception as ex:
        logger.error(f"Ошибка поиска заявок по ID водителя в админ панели: {ex}")
        await msg.answer(text="Вы ввели некорректный ID водителя. Попробуйте ещё раз")


@manager_router.callback_query(F.data == "manager_delete_order")
async def ask_order_to_delete(call: CallbackQuery, state: FSMContext):
    await state.set_state(Manager.delete_order)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите ID записи заявки которую надо удалить.")


@manager_router.message(Manager.delete_order)
async def delete_order(msg: Message, state: FSMContext, session: AsyncSession):
    try:
        order_id = int(msg.text)
        await state.clear()
        if await delete_order_from_db(session, order_id):
            await msg.answer(f"Заявка с ID записи <b>{order_id}</b> удалена", reply_markup=search_orders_kb())
        else:
            await msg.answer(f"Заявка не удалена: не найдена заявка с ID записи <b>{order_id}</b>",
                             reply_markup=search_orders_kb())
    except Exception as ex:
        logger.error(f"Ошибка удаления заявок в админ панели: {ex}")
        await msg.answer(text="Вы ввели некорректный ID записи заявки. Попробуйте ещё раз")


@manager_router.callback_query(F.data == "manager_purge_key")
async def ask_order_to_purge_key(call: CallbackQuery, state: FSMContext):
    await state.set_state(Manager.purge_key)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введите код активации который надо аннулировать.\n"
                              "Ключ аннулируется только если есть соответсвующая запись в БД")


@manager_router.message(Manager.purge_key)
async def purge_key(msg: Message, state: FSMContext, session: AsyncSession):
    key = msg.text.lower()
    tpl = KeyFormats.key
    if re.match(tpl, key) is not None:
        try:
            await state.clear()
            text = ""
            if await order_reset_key(session, key) is not None:
                text = f"Код активации <b>{key}</b>:\nАннулирован для заявок\n"
            else:
                text = f"Код активации <b>{key}</b>:\nНе аннулирован для заявок. Не найдено записи в базе\n"

            if await vehicle_reset_key(session, key) is not None:
                text += f"Аннулирован для информации о ТС"
            else:
                text += f"Не аннулирован для информации о ТС. Не найдено записи в базе"

            await msg.answer(text=text, reply_markup=search_orders_kb())
        except Exception as ex:
            logger.error(f"Ошибка аннулирования кода в менеджер панели: {ex}")
            await msg.answer(text="Возникла ошибка с аннулированием кода. Попробуйте ещё раз")
    else:
        await msg.answer(text=incorrect_key_text('ru'))
