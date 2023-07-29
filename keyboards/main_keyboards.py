from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_main():

    main_buttons = [
        InlineKeyboardButton(text='📖 Жанры 📖', callback_data='genre'),
        InlineKeyboardButton(text='🔍 Поиск по названию 🔎', callback_data='search')
    ]

    return main_buttons


def get_main_kb() -> InlineKeyboardMarkup:
    """
    Возвращает ReplyKeyboardMarkup с основными кнопками.
    Returns:
        ReplyKeyboardMarkup: Объект с основными кнопками.
    """
    kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb.add(*get_main())

    return kb.as_markup()


def admin_kb() -> InlineKeyboardMarkup:

    kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb.button(text='scrap_start', callback_data='scrap')

    return kb.as_markup()


