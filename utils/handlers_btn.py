from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, URLInputFile

from database.database import users_db
from database.db_buttons import genre, serials, feature_film, OVA, specials, anime_dict
from fsm.main_FCM import Genre, FeatureFilm, Serials, OVA_State, Specials, Save
from keyboards.inline_keyboard import anime_keyboard, description_kb


async def handle_next_page_btn(callback: CallbackQuery, state: str):
    # Общий обработчик нажатия кнопки "Следующая страница" для списка аниме выбранного жанра.
    gnr = callback.message.text

    print(gnr)
    if state == 'all':
        names = genre[gnr]['name']
    elif state == 'feature_film':
        names = feature_film[gnr]
    elif state == 'serials':
        names = serials[gnr]
    elif state == 'OVA':
        names = OVA[gnr]
    elif state == 'specials':
        names = specials[gnr]
    else:
        names = users_db[callback.from_user.id]['save']
        gnr = names

    # Вычисление общего количества страниц для списка аниме выбранного жанра (по 10 аниме на странице)
    count_page = len(names) // 10 if len(names) % 10 == 0 else (len(names) // 10) + 1

    # Проверка, что пользователь находится не на последней странице списка
    if users_db[callback.from_user.id]['page'] < count_page:
        users_db[callback.from_user.id]['page'] += 1
        # Редактирование сообщения с текущим жанром аниме и обновленной клавиатурой аниме
        await callback.message.edit_text(text=callback.message.text,
                                         reply_markup=anime_keyboard(gnr,
                                                                     start=users_db[callback.from_user.id]["page"],
                                                                     state=state))
    await callback.answer()


async def handle_previous_page(callback: CallbackQuery, state: str):
    # Обработчик нажатия кнопки "Предыдущая страница" для списка аниме выбранного жанра.

    if state == 'save':
        names = users_db[callback.from_user.id]['save']
    else:
        names = callback.message.text

    # Проверка, что пользователь не находится на первой странице списка
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        # Редактирование сообщения с текущим жанром аниме и обновленной клавиатурой аниме
        await callback.message.edit_text(text=callback.message.text,
                                         reply_markup=anime_keyboard(names,
                                                                     start=users_db[callback.from_user.id]["page"],
                                                                     state=state))
    await callback.answer()


async def handle_press_animation(callback: CallbackQuery, state: str, status: FSMContext):

    if state == 'all':
        name_anime = genre[callback.message.text]['name'][int(callback.data)]
    elif state == 'feature_film':
        name_anime = feature_film[callback.message.text][int(callback.data)]
    elif state == 'serials':
        name_anime = serials[callback.message.text][int(callback.data)]
    elif state == 'OVA':
        name_anime = OVA[callback.message.text][int(callback.data)]
    elif state == 'specials':
        name_anime = specials[callback.message.text][int(callback.data)]
    else:
        name_anime = users_db[callback.from_user.id]['save'][int(callback.data)]

    description = anime_dict[name_anime]['description']

    if len(description) > 0:
        # Отправка сообщения с описанием аниме и клавиатурой для дальнейшего взаимодействия
        image_from_url = URLInputFile(anime_dict[name_anime]['description']['img'])
        rating = anime_dict[name_anime]['description']['Рейтинг']
        await callback.message.answer_photo(
            image_from_url,
            caption=f"{name_anime}\n"
                    f"Рейтинг: {'Нет оценок' if rating == 'Нет оценок' else f'{rating}/10'}\n"
                    f"Тип: {description['Тип'] if 'Тип' in description else '??'}\n"
                    f"Дата выходы: {description['Год выхода'] if 'Год выхода' in description else '??'}\n"
                    f"Страна: {description['Страна'] if 'Страна' in description else '??'}",
            reply_markup=description_kb(name_anime, callback=callback)
        )
        await callback.message.delete()
    else:
        await callback.message.answer('К сожалению, это аниме пока недоступно',
                                      reply_markup=description_kb(name_anime, callback=callback))
        await callback.message.delete()

    # Установка состояния FSM в состояние "description"
    if state == 'all':
        await status.set_state(Genre.description)
    elif state == 'feature_film':
        await status.set_state(FeatureFilm.description)
    elif state == 'serials':
        await status.set_state(Serials.description)
    elif state == 'OVA':
        await status.set_state(OVA_State.description)
    elif state == 'specials':
        await status.set_state(Specials.description)
    else:
        await status.set_state(Save.description)

    await callback.answer()
