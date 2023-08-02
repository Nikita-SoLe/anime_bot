from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboard import anime_keyboard
from fsm.main_FCM import FSM_main, Serials
from database.database import users_db
from utils.handlers_btn import handle_previous_page, handle_next_page_btn, handle_press_animation


router: Router = Router()


@router.callback_query(FSM_main.serials)
async def press_serials_film_genre_btn(callback: CallbackQuery, state: FSMContext):

    users_db[callback.from_user.id]['state'] = (callback, state)

    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=anime_keyboard(callback.data,
                                                              start=users_db[callback.from_user.id]["page"],
                                                              state="serials"))

    await callback.message.delete()
    # Установка состояния FSM в состояние "anime" для сериалов
    await state.set_state(Serials.anime)


@router.callback_query(Serials.anime, Text(text='next_page'))
async def touch_serials_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='serials')


@router.callback_query(Serials.anime, Text(text='previous_page'))
async def touch_serials_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='serials')


@router.callback_query(Serials.anime)
async def press_serials_animation(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback, state='serials', status=state)


@router.callback_query(Serials.description, Text(text='come_back'))
async def press_serials_come_back(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(Serials.anime)
    await callback.message.delete()
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_serials_film_genre_btn(*users_db[callback.from_user.id]['state'])
    await callback.answer()
