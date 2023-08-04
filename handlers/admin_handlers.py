from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from parse.scrap import start_scrap

router = Router()


@router.callback_query(Text('scrap'))
async def press_scrap_anime(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Scrap start')
    start_scrap()
    await message.answer(text='Finish scrap')


