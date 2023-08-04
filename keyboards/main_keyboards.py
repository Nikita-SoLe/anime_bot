from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def main_btn():

    main_buttons = [
        InlineKeyboardButton(text='📖 Жанры 📖', callback_data='genre'),
        InlineKeyboardButton(text='🔍 Поиск 🔎', callback_data='search')
    ]

    return main_buttons


def get_main_kb() -> InlineKeyboardMarkup:
    """
    Возвращает ReplyKeyboardMarkup с основными кнопками.
    Returns:
        ReplyKeyboardMarkup: Объект с основными кнопками.
    """
    kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb.button(text="Полнометражные", callback_data="feature_film")
    kb.button(text="Сериалы", callback_data="serials")
    kb.button(text="OVA", callback_data="OVA")
    kb.button(text="Спешлы", callback_data="specials")
    kb.row(*main_btn())
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='📋 Отложенные 📋', callback_data='saved'))

    return kb.as_markup()


def admin_kb() -> InlineKeyboardMarkup:

    kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb.button(text='scrap_start', callback_data='scrap')

    return kb.as_markup()


