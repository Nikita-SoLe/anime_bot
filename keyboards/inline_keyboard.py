from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_buttons import genre, anime_dict, feature_film, OVA, serials, specials


def get_subscribed_kb() -> InlineKeyboardMarkup:

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text='Kon-Anime', url='https://t.me/kon_anime')

    return builder.as_markup()


def main_menu_btn() -> InlineKeyboardMarkup:

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text='⬇ Главное меню ⬇', callback_data='main_menu')

    return builder.as_markup()


def get_pagination_btn(names, page_num) -> list:

    row_with_three_buttons = [
        InlineKeyboardButton(text='⬅️ Предыдущая', callback_data='previous_page'),
        InlineKeyboardButton(text=f'{page_num} / {len(names) // 10 if len(names) % 10 == 0 else (len(names) // 10) + 1}',
                             callback_data='done'),
        InlineKeyboardButton(text='Следующая ➡️', callback_data='next_page')
    ]

    return row_with_three_buttons


def genre_keyboard() -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup с кнопками для выбора жанра аниме.
    Returns:
        InlineKeyboardMarkup: Объект с кнопками жанров аниме.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for key in genre.keys():
        builder.button(text=f'{key}', callback_data=f'{key}')

    builder.adjust(4)
    builder.row(InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

    return builder.as_markup()


def anime_keyboard(genr, start=1, state: str = None) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup с кнопками аниме выбранного жанра и определенной страницы.
    Args:
        genr (str): Выбранный жанр аниме.
        start (int): Номер страницы.
        state (str): Передает из какого состояния вызывают клавиатуру
    Returns:
        InlineKeyboardMarkup: Объект с кнопками аниме.
    """

    if state == 'all':
        names = genre[genr]['name']
    elif state == 'feature_film':
        names = feature_film[genr]
    elif state == 'serials':
        names = serials[genr]
    elif state == 'OVA':
        names = OVA[genr]
    else:
        names = specials[genr]

    builder = InlineKeyboardBuilder()

    page_num = start

    if start == 1:
        stop = start * 10

        if len(names) >= stop:
            for i in range(0, stop):
                builder.row(InlineKeyboardButton(text=names[i], callback_data=f'{i}'), width=1)
        else:
            for i in range(0, len(names)):
                builder.row(InlineKeyboardButton(text=names[i], callback_data=f'{i}'), width=1)
    else:
        stop = start * 10
        start = (start - 1) * 10

        if len(names) >= stop:
            for i in range(start, stop):
                builder.row(InlineKeyboardButton(text=names[i], callback_data=f'{i}'), width=1)
        else:
            for i in range(start, len(names)):
                builder.row(InlineKeyboardButton(text=names[i], callback_data=f'{i}'), width=1)

    builder.adjust(1)

    builder.row(*get_pagination_btn(page_num=page_num, names=names))
    builder.row(InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

    return builder.as_markup()


def description_kb(name) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup с кнопками для описания аниме.
    Args:
        name (str): Название аниме.
    Returns:
        InlineKeyboardMarkup: Объект с кнопками описания аниме.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text='▶️~~Перейти к просмотру~~▶️', url=anime_dict[name]['url'])
    builder.button(text='🔙~~Вернуться к списку~~🔙', callback_data='come_back')

    builder.adjust(1)

    return builder.as_markup()


def anime_search_kb(names, page: int = None) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup с кнопками для списка найденного аниме.
    Args:
        names: Переменное количество аргументов с информацией о найденных аниме.
        page (int): Номер страницы по умолчанию None
    Returns:
        InlineKeyboardMarkup: Объект с кнопками найденного аниме.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if not page:
        for name in names:
            builder.button(text=str(name[1]), callback_data=f'{name[0]}')
            builder.adjust(1)
    else:
        start = (page - 1) * 10
        stop = page * 10

        if stop < len(names):
            for i in range(start, stop):
                builder.button(text=str(names[i][1]), callback_data=f'{names[i][0]}')
        else:
            for i in range(start, len(names)):
                builder.button(text=str(names[i][1]), callback_data=f'{names[i][0]}')

        builder.adjust(1)
        builder.row(*get_pagination_btn(names=names, page_num=page))
        builder.row(InlineKeyboardButton(text="🔍 Найти другое 🔎", callback_data='find_another'))

    return builder.as_markup()

