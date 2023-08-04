from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.touch_main_button import press_feature_btn
from keyboards.inline_keyboard import anime_keyboard
from fsm.main_FCM import FSM_main, FeatureFilm
from database.database import users_db
from utils.handlers_btn import handle_previous_page, handle_next_page_btn, handle_press_animation

router: Router = Router()


@router.callback_query(FSM_main.feature_film)
async def press_feature_film_genre_btn(callback: CallbackQuery, state: FSMContext):

    users_db[callback.from_user.id]['state'] = (callback, state)

    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=anime_keyboard(callback.data,
                                                              start=users_db[callback.from_user.id]["page"],
                                                              state="feature_film"))

    try:
        await callback.message.delete()
    except Exception:
        # Обработка ошибки, если сообщение уже было удалено
        pass

    # Установка состояния FSM в состояние "anime" для полнометражных фильмов
    await state.set_state(FeatureFilm.anime)


@router.callback_query(FeatureFilm.anime, Text(text='next_page'))
async def touch_feature_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='feature_film')


@router.callback_query(FeatureFilm.anime, Text(text='previous_page'))
async def touch_feature_film_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='feature_film')


@router.callback_query(FeatureFilm.anime, Text('back_to_genre'))
async def touch_back_to_genre_btn(callback: CallbackQuery):
    await callback.message.delete()
    await press_feature_btn(*users_db[callback.from_user.id]['state'])


@router.callback_query(FeatureFilm.anime)
async def press_feature_film_animation(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback, state='feature_film', status=state)


@router.callback_query(FeatureFilm.description, Text(text='come_back'))
async def press_feature_film_come_back(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(FeatureFilm.anime)
    await callback.message.delete()
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_feature_film_genre_btn(*users_db[callback.from_user.id]['state'])
    await callback.answer()
