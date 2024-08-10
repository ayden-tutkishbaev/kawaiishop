import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import users, admins

from database.queries import *

from configs import BOT_TOKEN


async def main() -> None:
    await async_main()
    await set_tables()
    dp = Dispatcher()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(
        admins.admin,
        users.user
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("BOT IS OFF")