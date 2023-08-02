# Импорт необходимых модулей
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import Text



# Импорт пользовательских модулей
from database.database import users_db
from keyboards.inline_keyboard import anime_keyboard
from fsm.main_FCM import FSM_main, Genre
from utils.handlers_btn import handle_next_page_btn, handle_previous_page, handle_press_animation

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
                                                              start=users_db[callback.from_user.id]["page"],
                                                              state="all"))

    await callback.message.delete()
    # Установка состояния FSM в состояние "anime"
    await state.set_state(Genre.anime)


@router.callback_query(Genre.anime, Text('next_page'))
async def touch_genre_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='all')


@router.callback_query(Genre.anime, Text(text='previous_page'))
async def touch_genre_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='all')


@router.callback_query(Genre.anime)
async def press_genre_animation(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback, state='all', status=state)


@router.callback_query(Genre.description, Text(text='come_back'))
async def press_animation(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(Genre.anime)
    await callback.message.delete()
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_genre(*users_db[callback.from_user.id]['state'])
    await callback.answer()