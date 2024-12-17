import asyncio
import logging

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram import F

from default_menu import start
from host_menu import create_new_game, leave_and_destroy_game
from client_menu import join_game, join_specified_game, leave_game
from common import action, bot

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


async def main():

    dp.message.register(start, Command("start"))
    dp.message.register(create_new_game, F.text.lower() == "создать игру")
    dp.message.register(join_game, F.text.lower() == "присоединиться к игре")
    dp.message.register(join_specified_game, F.from_user.id.func(
        lambda x: action.keys().__contains__(x) and action[x] == "Присоединиться к игре"))
    dp.message.register(leave_and_destroy_game, F.text.lower() == "выйти и завершить игру")
    dp.message.register(leave_game, F.text.lower() == "выйти из игры")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
