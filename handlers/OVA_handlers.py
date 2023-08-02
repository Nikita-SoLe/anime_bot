from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboard import anime_keyboard
from fsm.main_FCM import FSM_main, OVA_State
from database.database import users_db
from utils.handlers_btn import handle_previous_page, handle_next_page_btn, handle_press_animation


router: Router = Router()


@router.callback_query(FSM_main.OVA)
async def press_ova_film_genre_btn(callback: CallbackQuery, state: FSMContext):

    users_db[callback.from_user.id]['state'] = (callback, state)

    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=anime_keyboard(callback.data,
                                                              start=users_db[callback.from_user.id]["page"],
                                                              state="OVA"))

    await callback.message.delete()
    # Установка состояния FSM в состояние "anime" для сериалов
    await state.set_state(OVA_State.anime)


@router.callback_query(OVA_State.anime, Text(text='next_page'))
async def touch_ova_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='OVA')


@router.callback_query(OVA_State.anime, Text(text='previous_page'))
async def touch_ova_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='OVA')


@router.callback_query(OVA_State.anime)
async def press_ova_animation(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback, state='OVA', status=state)


@router.callback_query(OVA_State.description, Text(text='come_back'))
async def press_ova_come_back(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(OVA_State.anime)
    await callback.message.delete()
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_ova_film_genre_btn(*users_db[callback.from_user.id]['state'])
    await callback.answer()

