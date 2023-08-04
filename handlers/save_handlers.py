from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from database.database import users_db
from fsm.main_FCM import Save
from keyboards.inline_keyboard import anime_keyboard, main_menu_btn
from utils.handlers_btn import handle_press_animation, handle_previous_page, handle_next_page_btn

router: Router = Router()


@router.callback_query(Text('save'))
async def touch_save_btn(callback: CallbackQuery):
    name = callback.message.caption.split('\n')[0]
    names = users_db[callback.from_user.id]['save']
    if name not in names:
        names.append(name)
        await callback.answer(text='Добавлено в отложенные.', show_alert=True)
    else:
        await callback.answer(text='Уже есть в вашем списке', show_alert=True)
    print(users_db[callback.from_user.id])


@router.callback_query(Text('delete_saved'))
async def touch_delete_saved_btn(callback: CallbackQuery):
    name = callback.message.caption.split('\n')[0]
    names = users_db[callback.from_user.id]['save']
    if name in names:
        names.remove(name)
        await callback.answer(text='Удалено из отложенных.', show_alert=True)
    else:
        await callback.answer(text='Уже отсутствует в отложенных.', show_alert=True)


@router.callback_query(Text('saved'))
async def touch_saved_btn(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id]['state'] = (callback, state)

    try:
        await callback.message.delete()
    except Exception:
        # Обработка ошибки, если сообщение уже было удалено
        pass

    if users_db[callback.from_user.id]['save']:
        await callback.message.answer(text='Отложенные',
                                      reply_markup=anime_keyboard(users_db[callback.from_user.id]['save'],
                                                                  users_db[callback.from_user.id]['page'],
                                                                  state='save'))
    else:
        await callback.message.answer(text='Пока что у вас ничего нет.',
                                      reply_markup=main_menu_btn())
    await state.set_state(Save.anime)


@router.callback_query(Save.anime, Text(text='next_page'))
async def touch_ova_next_page_btn(callback: CallbackQuery):
    await handle_next_page_btn(callback, state='save')


@router.callback_query(Save.anime, Text('previous_page'))
async def touch_saved_previous_page_btn(callback: CallbackQuery):
    await handle_previous_page(callback, state='save')


@router.callback_query(Save.description, Text(text='come_back'))
async def press_animation(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # Обработчик нажатия кнопки "Назад" в описании аниме.
    await state.set_state(Save.anime)
    # Возврат к предыдущему состоянию и сообщению с жанром аниме и клавиатурой
    await touch_saved_btn(*users_db[callback.from_user.id]['state'])
    await callback.answer()


@router.callback_query(Save.anime)
async def touch_saved_anime_btn(callback: CallbackQuery, state: FSMContext):
    await handle_press_animation(callback=callback, state='saved', status=state)
    await state.set_state(Save.description)

