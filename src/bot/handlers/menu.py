from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

# custom imports
from src.bot.states import SetLang, Authorization
from src.bot.filters.manage_access import get_stand_chat_ids
from src.services.settings import settings
# keyboards
from src.bot.keyboards.menu import lang_kb, finish_kb, return_to_menu_kb, menu_kb
# database
from src.database.scripts.lang import set_user_lang, get_user_lang
# texts
from src.bot.texts.menu import *
from src.bot.texts.authorization import get_format_messages

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    if msg.from_user.id in get_stand_chat_ids():
        await state.set_state(SetLang.lang)
        await msg.answer(text=choose_lang_text(await get_user_lang(session, msg)), reply_markup=lang_kb())
    else:
        await cmd_menu(msg, state, session, await get_user_lang(session, msg))


@router.callback_query(F.data == "start_program")
async def start_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    if call.from_user.id in get_stand_chat_ids():
        await state.set_state(SetLang.lang)
        await call.message.edit_text(text=choose_lang_text(await get_user_lang(session, call)), reply_markup=lang_kb())
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await cmd_menu(call.message, state, session, await get_user_lang(session, call))


@router.message(Command("change_lang"))
async def cmd_lang(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.set_state(SetLang.lang)
    await msg.answer(text=choose_lang_text(await get_user_lang(session, msg)), reply_markup=lang_kb())


@router.message(Command("help"))
async def cmd_help(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.clear()
    await msg.answer(text=help_text(lang), reply_markup=return_to_menu_kb(lang))


@router.message(Command("user_agree"))
async def cmd_user_agree(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.clear()
    await msg.answer(text=user_agreement_text(lang, settings.bot['user_agree']), reply_markup=return_to_menu_kb(lang))


@router.message(Command("menu"))
async def cmd_menu(msg: Message, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.clear()

    if msg.from_user.id in get_stand_chat_ids():
        await msg.answer(text=stand_menu_text(lang), reply_markup=menu_kb(lang))
    else:
        await msg.answer(text=user_menu_text(lang))
        await state.set_state(Authorization.licence_input)
        await msg.answer(text=get_format_messages(lang, 'ru'))  # TODO изменить генерацию текстов


@router.callback_query(StateFilter(None), F.data == "change_lang")
async def change_lang(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str) -> None:
    await state.set_state(SetLang.lang)
    await call.message.edit_text(text=choose_lang_text(lang), reply_markup=lang_kb())


@router.callback_query(SetLang.lang, F.data.startswith("lang_"))
async def show_menu(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    await set_user_lang(call, session)
    user_lang = await get_user_lang(session, call)

    if call.from_user.id in get_stand_chat_ids():
        await call.message.edit_text(text=selected_lang_text(user_lang), reply_markup=None)
        await call.message.answer(text=greeting_text(user_lang), reply_markup=finish_kb())
        await call.message.answer(text=commands_text(user_lang), reply_markup=menu_kb(user_lang))
    else:
        await call.message.edit_text(text=user_menu_text(user_lang))
        await state.set_state(Authorization.licence_input)
        await call.message.answer(text=get_format_messages(user_lang, 'ru'))  # TODO изменить генерацию текстов


@router.callback_query(F.data.in_(["back_to_menu", "confirm"]))
async def back_to_menu(call: CallbackQuery, state: FSMContext, session: AsyncSession, lang: str):
    await state.clear()
    if call.from_user.id in get_stand_chat_ids():
        await call.message.edit_text(text=stand_menu_text(lang), reply_markup=menu_kb(lang))
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(text=user_menu_text(lang))
        await state.set_state(Authorization.licence_input)
        await call.message.answer(text=get_format_messages(lang, 'ru'))  # TODO изменить генерацию текстов
