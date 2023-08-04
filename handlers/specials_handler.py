from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.touch_main_button import press_specials_btn
from keyboards.inline_keyboard import anime_keyboard
from fsm.main_FCM import FSM_main, Specials
from database.database import users_db
from utils.handlers_btn import handle_previous_page, handle_next_page_btn, handle_press_animation


router: Router = Router()


@router.callback_query(FSM_main.specials)
async def press_specials_film_genre_btn(callback: CallbackQuery, state: FSMContext):

    users_db[callback.from_user.id]['state'] = (callback, state)

    await callback.message.answer(text=f'{callback.data}',
                                  reply_markup=anime_keyboard(callback.data,
                                                              start=users_db[callback.from_user.id]["page"],
                                                              state="specials"))

    try:
        await callback.message.delete()
    except Exception:
        # Обработка ошибки, если сообщение уже было удалено
        pass

    # Установка состояния FSM в состояние "anime" для сериалов
    await state.set_state(Specials.anime)


@router.callback_query(Specials.anime, Text(text='next_page'))
async def touch_specials_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='specials')


@router.callback_query(Specials.anime, Text(text='previous_page'))
async def touch_specials_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='specials')


@router.callback_query(Specials.anime, Text('back_to_genre'))
async def touch_back_to_genre_btn(callback: CallbackQuery):
    await callback.message.delete()
    await press_specials_btn(*users_db[callback.from_user.id]['state'])



@router.callback_query(Specials.anime)
async def press_ova_animation(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback, state='specials', status=state)


@router.callback_query(Specials.description, Text(text='come_back'))
async def press_ova_come_back(callback: CallbackQuery, state: FSMContext):
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(Specials.anime)
    await callback.message.delete()
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await press_specials_film_genre_btn(*users_db[callback.from_user.id]['state'])
    await callback.answer()

