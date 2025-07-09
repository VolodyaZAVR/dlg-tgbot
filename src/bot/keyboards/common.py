from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb() -> InlineKeyboardMarkup:
    """
    kb_list = [
        [KeyboardButton(text="Начать работу")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите на кнопку"
    )
    return keyboard
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Начать работу", callback_data='start_program'))
    return kb.as_markup(resize_keyboard=True)


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_row_inline_keyboard(items: dict[str, str]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками в один ряд
    :param items: список текстов и коллбеков для кнопок
    :return: объект инлайн-клавиатуры
    """
    row = [InlineKeyboardButton(text=item, callback_data=items.get(item)) for item in items]
    return InlineKeyboardMarkup(inline_keyboard=[row], resize_keyboard=True)
