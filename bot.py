# Импорт необходимых модулей
import asyncio
from aiogram import Bot, Dispatcher

# Импорт пользовательских модулей
from config_reader import config
from handlers import command, touch_main_button, inline_handlers, admin_handlers, search_handlers, \
    feature_film_handlers, serials_handler, OVA_handlers, specials_handler

# Создание экземпляра бота с использованием токена из конфигурационного файла
bot: Bot = Bot(token=config.bot_token.get_secret_value())

# Создание экземпляра диспетчера (отвечает за обработку входящих сообщений и команд)
dp: Dispatcher = Dispatcher()


# Функция, выполняющаяся при старте бота.
# Отправляет сообщение в чат при перезапуске бота.
async def on_startup():
    await bot.send_message(chat_id=bot.id, text="Пожалуйста пропишите команду /start, для корректной работы бота")


# Главная функция, запускающая бота и настраивающая обработчики.
async def main():
    # Включение обработчиков (routers) в диспетчер.
    dp.include_routers(
        command.router,
        search_handlers.router,
        admin_handlers.router,
        touch_main_button.router,
        feature_film_handlers.router,
        serials_handler.router,
        OVA_handlers.router,
        specials_handler.router,
        inline_handlers.router
    )

    # Удаление вебхука (если был настроен) и удаление ожидающих обновлений перед запуском бота
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск бота в режиме "получение обновлений с помощью long polling"
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запуск функции main() с помощью asyncio.run()
    asyncio.run(main())



