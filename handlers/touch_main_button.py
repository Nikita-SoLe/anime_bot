from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from fsm.main_FCM import FSM_main
from keyboards.inline_keyboard import genre_keyboard, main_menu_btn
from database.database import users_db
from keyboards.main_keyboards import get_main_kb

router: Router = Router()


@router.callback_query(Text("genre"))
async def press_genre_button(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Жанры".
    Args:
        callback: Объект сообщения от пользователя.
        state: Состояние FSMContext.
    """
    users_db[callback.from_user.id]['state'] = (callback, state)
    await state.set_state(FSM_main.genre)
    users_db[callback.from_user.id]['page'] = 1

    try:
        await callback.message.delete()
    except Exception as ex:
        pass

    await callback.message.answer(text='Жанры', reply_markup=genre_keyboard())


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
    await callback.message.edit_text(text='Введите название, которое хотели бы найти.\n'
                                          'Пожалуйста вводите на русском.',
                                     reply_markup=main_menu_btn())


@router.callback_query(Text("feature_film"))
async def press_feature_btn(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['state'] = (callback, state)
    await state.set_state(FSM_main.feature_film)
    users_db[callback.from_user.id]['page'] = 1

    try:
        await callback.message.delete()
    except Exception as ex:
        pass

    await callback.message.answer(text='Полнометражные фильмы', reply_markup=genre_keyboard())


@router.callback_query(Text("serials"))
async def press_serials_btn(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['state'] = (callback, state)
    await state.set_state(FSM_main.serials)
    users_db[callback.from_user.id]['page'] = 1

    try:
        await callback.message.delete()
    except Exception as ex:
        pass

    await callback.message.answer(text='Сериалы', reply_markup=genre_keyboard())


@router.callback_query(Text("OVA"))
async def press_ova_btn(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['state'] = (callback, state)
    await state.set_state(FSM_main.OVA)
    users_db[callback.from_user.id]['page'] = 1

    try:
        await callback.message.delete()
    except Exception as ex:
        pass

    await callback.message.answer(text='OVA и ONA', reply_markup=genre_keyboard())


@router.callback_query(Text("specials"))
async def press_specials_btn(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['state'] = (callback, state)
    await state.set_state(FSM_main.specials)
    users_db[callback.from_user.id]['page'] = 1

    try:
        await callback.message.delete()
    except Exception as ex:
        pass

    await callback.message.answer(text='Спешлы', reply_markup=genre_keyboard())


@router.callback_query(Text("main_menu"))
async def press_main_menu_btn(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    users_db[callback.from_user.id]['page'] = 1
    users_db[callback.from_user.id]['state'] = None
    users_db[callback.from_user.id]['search'] = None
    await callback.message.delete()
    await callback.message.answer("Добро пожаловать!!!\n"
                                  f"{callback.from_user.first_name}\n"
                                  "Вы нашли Самую Большую\n"
                                  "Коллекцию Аниме в телеграмме.\n"
                                  "В моей базе находятся:\n"
                                  "Более 3500 аниме-сериалов,\n"
                                  "Свыше 870 полнометражных фильмов,\n"
                                  "Больше чем 2000 различных OVA и ONA,\n"
                                  "А так же 360+ Спешлов.\n"
                                  "И все это для вас,\n"
                                  "Наслаждайтесь просмотром\n"
                                  "И делитесь ботом с друзьями.",
                                  reply_markup=get_main_kb())
