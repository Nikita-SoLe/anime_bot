from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from fsm.main_FCM import FSM_main
from keyboards.inline_keyboard import genre_keyboard, search_kb
from database.database import users_db


router: Router = Router()


@router.callback_query(Text("genre"))
async def genre_button(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Жанры".
    Args:
        callback: Объект сообщения от пользователя.
        state: Состояние FSMContext.
    """

    await state.set_state(FSM_main.genre)
    users_db[callback.from_user.id]['page'] = 1
    await callback.message.edit_text(text='Жанры', reply_markup=genre_keyboard())


@router.callback_query(Text("search"))
async def search_for_name(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Поиск по названию".
    Args:
        callback: Объект сообщения от пользователя.
        state: Состояние FSMContext.
    """
    await state.set_state(FSM_main.search)
    users_db[callback.from_user.id]['page'] = 1
    users_db[callback.from_user.id]['search'] = None
    await callback.message.edit_text(text='Введите название, которое хотели бы найти.',
                                     reply_markup=search_kb())

