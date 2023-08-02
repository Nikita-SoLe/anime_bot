from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.types.callback_query import CallbackQuery

from fsm.main_FCM import FSM_main, Search
from parse.scrap import anime_dict
from database.database import users_db
from keyboards.inline_keyboard import anime_search_kb, description_kb, main_menu_btn


router: Router = Router()


@router.message(FSM_main.search)
async def process_search_anime(message: Message, state: FSMContext):
    """
    Обработчик ввода названия для поиска аниме.
    Args:
        message: Объект сообщения от пользователя.
        state: Состояние FSMContext.
    """

    users_db[message.from_user.id]['state'] = (message, state)
    await state.set_state(Search.search_inline)

    lst_anime = []
    for i, key in enumerate(anime_dict.keys()):
        if message.text.lower() in key.lower():
            lst_anime.append([i, key])

    users_db[message.from_user.id]['search'] = lst_anime

    if not lst_anime:
        await message.edit_text(text='К сожалению, мне не удалось найти что-то похожее.\n\n'
                                     'Убедитесь в правильности написания вашего названия.\n\n'
                                     'Или же в моей базе пока нет этого аниме',
                                reply_markup=main_menu_btn())
        await state.set_state(FSM_main.search)
    elif len(lst_anime) < 10:
        await message.answer(text='Вот что я нашел', reply_markup=anime_search_kb(lst_anime))
    elif len(lst_anime) > 10:
        users_db[message.from_user.id]['search'] = lst_anime
        await message.answer(text='Вот что я нашел',
                             reply_markup=anime_search_kb(lst_anime, page=users_db[message.from_user.id]['page']))


@router.callback_query(Search.search_inline, Text(text='find_another'))
async def find_another(callback: CallbackQuery, state: FSMContext):
    """
    Обрабочик кнопки "Найти другое".
        Args:
        callback: Объект сообщения от пользователя.
        state: Состояние FSMContext.
    """
    await callback.message.delete()

    users_db[callback.from_user.id]['page'] = 1
    users_db[callback.from_user.id]['search'] = None

    await state.set_state(FSM_main.search)
    await callback.message.answer(text='Введите название, которое хотели бы найти.\n\n'
                                       'Пожалуйста, перед тем, как отправить название, '
                                       'удостоверьтесь в правильности его написания.\n',
                                  reply_markup=main_menu_btn())
    await callback.answer()


@router.callback_query(Search.search_inline, Text(text='come_back'))
async def press_animation(callback: CallbackQuery):
    """
    Обработчик нажатия кнопки "Назад" в поиске аниме.
    Args:
        callback: Объект callback query.
    """
    await callback.message.delete()
    await process_search_anime(*users_db[callback.from_user.id]['state'])
    await callback.answer()


@router.callback_query(Search.search_inline, Text(text='next_page'))
async def touch_back_page_btn(callback: CallbackQuery):
    """
    Обработчик нажатия инлайн-кнопки "Следующая страница" для списка аниме в поиске по названию.
    Args:
        callback: Объект callback query.
    """
    text = callback.message.text

    names = users_db[callback.from_user.id]['search']

    count_page = len(names) // 10 if len(names) % 10 == 0 else (len(names) // 10) + 1

    if users_db[callback.from_user.id]['page'] < count_page:
        users_db[callback.from_user.id]['page'] += 1
        await callback.message.edit_text(text=text,
                                         reply_markup=anime_search_kb(names=users_db[callback.from_user.id]['search'],
                                                                      page=users_db[callback.from_user.id]["page"]))
    await callback.answer()


@router.callback_query(Search.search_inline, Text(text='previous_page'))
async def touch_back_page_btn(callback: CallbackQuery):
    """
    Обработчик нажатия инлайн-кнопки "Предыдущая страница" для списка аниме в поиске по названию.
    Args:
        callback: Объект callback query.
    """
    text = callback.message.text

    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(text=text,
                                         reply_markup=anime_search_kb(names=users_db[callback.from_user.id]['search'],
                                                                      page=users_db[callback.from_user.id]["page"]))
    await callback.answer()


@router.callback_query(Search.search_inline)
async def press_search_animation(callback: CallbackQuery):
    """
    Обработчик выбора конкретного аниме из результатов поиска.
    Args:
        callback: Объект callback query.
    """

    await callback.message.delete()
    lst_keys = list(anime_dict.keys())
    name_anime = lst_keys[int(callback.data)]

    description = anime_dict[name_anime]['description']

    if len(description) > 0:
        # Отправка файла по ссылке
        image_from_url = URLInputFile(anime_dict[name_anime]['description']['img'])
        rating = anime_dict[name_anime]['description']['Рейтинг']
        await callback.message.answer_photo(
            image_from_url,
            caption=f"{name_anime}\n"
                    f"Рейтинг: {'Нет оценок' if rating == 'Нет оценок' else f'{rating}/10'}\n"
                    f"Тип: {description['Тип']}\n"
                    f"Возрастные ограничения: {description['Возрастные ограничения']}\n"
                    f"Длительность: {description['Длительность']}",
            reply_markup=description_kb(name_anime)
        )
    else:
        await callback.message.answer(text='К сожалению это аниме пока не доступно',
                                      reply_markup=description_kb(name_anime))

    await callback.answer()

