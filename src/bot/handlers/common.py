from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(F.text)
async def no_catch_message(msg: Message):
    await msg.answer("Ваш запрос не обработан, попробуйте ещё раз!")


@router.callback_query(F.data)
async def no_catch_callback(call: CallbackQuery):
    await call.message.edit_text(text="Ваш запрос не обработан, попробуйте ещё раз!", reply_markup=None)
