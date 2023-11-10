from aiogram import Bot, Dispatcher

import logging
import asyncio

from creds import BOT_TOKEN

from core.handlers import users_handlers

bot: Bot = Bot(BOT_TOKEN, parse_mode='html')
dp: Dispatcher = Dispatcher()


# Инициализируем логгер
logger: logging = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting Bot')

    # Регистрируем обработчики
    dp.include_router(users_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot Stopped!')
