# Импорт необходимых модулей
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import Text
from aiogram.types import URLInputFile


# Импорт пользовательских модулей
from database.database import users_db
from keyboards.inline_keyboard import anime_keyboard, description_kb
from fsm.main_FCM import FSM_main
from parse.scrap import genre, anime_dict

# Создание объекта роутера для обработки callback-кнопок
router: Router = Router()


@router.callback_query(FSM_main.genre)
async def press_genre(callback: CallbackQuery, state: FSMContext):
    # Обработчик выбора жанра аниме
    # Сохранение состояния (callback и state) пользователя в базе данных
    users_db[callback.from_user.id]['state'] = (callback, state)

    # Отправка сообщения с выбранным жанром аниме и клавиатурой аниме для данного жанра
    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=anime_keyboard(callback.data,
                                                              start=users_db[callback.from_user.id]["page"]))

    await callback.message.delete()
    # Установка состояния FSM в состояние "anime"
    await state.set_state(FSM_main.anime)


@router.callback_query(FSM_main.anime, Text(text='next_page'))
async def touch_next_page_btn(callback: CallbackQuery):
    # Обработчик нажатия кнопки "Следующая страница" для списка аниме выбранного жанра.
    file = genre
    gnr = callback.message.text
    names = file[gnr]['name']

    # Вычисление общего количества страниц для списка аниме выбранного жанра (по 10 аниме на странице)
    count_page = len(names) // 10 if len(names) % 10 == 0 else (len(names) // 10) + 1

    # Проверка, что пользователь находится не на последней странице списка
    if users_db[callback.from_user.id]['page'] < count_page:
        users_db[callback.from_user.id]['page'] += 1
        # Редактирование сообщения с текущим жанром аниме и обновленной клавиатурой аниме
        await callback.message.edit_text(text=gnr,
                                         reply_markup=anime_keyboard(gnr,
                                                                     start=users_db[callback.from_user.id]["page"]))
    await callback.answer()


@router.callback_query(FSM_main.anime, Text(text='previous_page'))
async def touch_next_page_btn(callback: CallbackQuery):
    # Обработчик нажатия кнопки "Предыдущая страница" для списка аниме выбранного жанра.
    gnr = callback.message.text

    # Проверка, что пользователь не находится на первой странице списка
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        # Редактирование сообщения с текущим жанром аниме и обновленной клавиатурой аниме
        await callback.message.edit_text(text=gnr,
                                         reply_markup=anime_keyboard(gnr,
                                                                     start=users_db[callback.from_user.id]["page"]))
    await callback.answer()


@router.callback_query(FSM_main.anime)
async def press_genre_animation(callback: CallbackQuery, state: FSMContext):
    # Обработчик выбора конкретного аниме.
    name_anime = genre[callback.message.text]['name'][int(callback.data)]
    description = anime_dict[name_anime]['description']

    if len(description) > 0:
        # Отправка сообщения с описанием аниме и клавиатурой для дальнейшего взаимодействия
        image_from_url = URLInputFile(anime_dict[name_anime]['description']['img'])
        rating = anime_dict[name_anime]['description']['Рейтинг']
        await callback.message.reply_photo(
            image_from_url,
            caption=f"{name_anime}\n"
                    f"Рейтинг: {'Нет оценок' if rating == 'Нет оценок' else f'{rating}/10'}\n"
                    f"Тип: {description['Тип']}\n"
                    f"Возрастные ограничения: {description['Возрастные ограничения']}\n"
                    f"Длительность: {description['Длительность']}",
            reply_markup=description_kb(name_anime)
        )
        await callback.message.delete()
    else:
        await callback.message.edit_text('К сожалению, это аниме пока недоступно',
                                         reply_markup=description_kb(name_anime))
        await callback.message.delete()

    # Установка состояния FSM в состояние "description"
    await state.set_state(FSM_main.description)
    await callback.answer()


@router.callback_query(FSM_main.description, Text(text='come_back'))
async def press_animation(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(FSM_main.anime)
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_genre(*users_db[callback.from_user.id]['state'])
