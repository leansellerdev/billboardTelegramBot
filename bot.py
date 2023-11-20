from aiogram import Bot, Dispatcher

import logging
import asyncio

from creds import BOT_TOKEN

from core.handlers import action_handlers, registration_handlers, command_handlers
from core.states.states import storage

from core.middlewares.throttling import ThrottlingMiddleware

bot: Bot = Bot(BOT_TOKEN, parse_mode='html')
dp: Dispatcher = Dispatcher(storage=storage)


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

    # Регистрируем middlewares
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))

    # Регистрируем обработчики
    dp.include_router(action_handlers.router)
    dp.include_router(registration_handlers.reg_router)
    dp.include_router(command_handlers.command_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot Stopped!')
