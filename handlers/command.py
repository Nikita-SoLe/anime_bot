from copy import deepcopy
from aiogram import Router, Bot
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from database.database import user_dict_template, users_db

from keyboards.main_keyboards import get_main_kb, admin_kb
from keyboards.inline_keyboard import get_subscribed_kb
from config_reader import config

router: Router = Router()


@router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    """
    Обработчик команды /start. Отправляет приветственное сообщение и создает запись пользователя в базе данных, если она еще не существует.
    Args:
        message: Объект сообщения от пользователя.
        bot: xxx
    """
    print(message.from_user.id)
    print(bot.id)
    is_subscribed = await bot.get_chat_member(chat_id='-1001826045814', user_id=message.from_user.id)
    print(type(is_subscribed))
    if is_subscribed.status not in ['creator', 'member']:
        await message.answer("Здравствуй!\n"
                             f"{message.from_user.first_name}\n"
                             f"Для корректной работы бота,\n"
                             f"Пожалуйста подпишитесь на этот канал.\n"
                             f"После подписки нажмите сюда -> /start",
                             reply_markup=get_subscribed_kb())
    else:
        await message.answer("Добро пожаловать!!!\n"
                             f"{message.from_user.first_name}\n"
                             "Вы нашли самую большую\n"
                             "коллекцию Аниме в телеграмме.\n"
                             "В моей базе находятся:\n"
                             "Более 1400 аниме-сериалов,\n"
                             "Свыше 250 полнометражных фильмов,\n"
                             "Больше чем 350 различных OVA и ONA,\n"
                             "А так же 200+ Спешилов.\n"
                             "И все это для вас,\n"
                             "Мой Дорогой Гость!\n"
                             "Наслаждайтесь просмотром\n"
                             "И делитесь ботом с друзьями.",
                             reply_markup=get_main_kb())

        if message.from_user.id not in users_db:
            # Создание записи пользователя в базе данных, используя шаблон
            users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command('admin'))
async def command_admin(message: Message):

    if message.from_user.id == config.admin_id_nikita:
        await message.answer(text='Admin panel',
                             reply_markup=admin_kb())


@router.callback_query(Text(text='done'))
async def press_number_pagination(callback: CallbackQuery):
    # Обработчик завершения пагинации аниме.
    await callback.answer()