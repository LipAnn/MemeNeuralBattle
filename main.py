import asyncio
import logging

from aiogram import Dispatcher, types
from aiogram import F
from aiogram.filters import Command

import common
from client_menu import join_game, join_specified_game, leave_game
from common import action, bot
from default_menu import start
from host_menu import create_new_game, leave_and_destroy_game, start_game, set_round_limit, enter_round_limit, options,\
    back_to_menu, set_classic_mode, set_ai_mode, game_mode
from answer import answer
from vote import vote

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


async def unknown_command(message: types.Message):
    await common.update_caches(message)
    await message.answer("Неизвестная команда")


async def main():

    dp.message.register(start, Command("start"))
    dp.message.register(create_new_game, F.text.lower() == "создать игру")
    dp.message.register(join_game, F.text.lower() == "присоединиться к игре")
    dp.message.register(join_specified_game, F.from_user.id.func(
        lambda x: action.keys().__contains__(x) and action[x] == "Присоединиться к игре"))
    dp.message.register(leave_and_destroy_game, F.text.lower() == "выйти и завершить игру")
    dp.message.register(leave_game, F.text.lower() == "выйти из игры")
    dp.message.register(start_game, F.text.lower() == "начать игру")
    dp.message.register(options, F.text.lower() == "настройки игры")
    dp.message.register(enter_round_limit, F.text.lower() == "установить количество раундов")
    dp.message.register(back_to_menu, F.text.lower() == "выйти в меню")
    dp.message.register(set_classic_mode, F.text.lower() == "классический режим")
    dp.message.register(set_ai_mode, F.text.lower() == "ии-режим")
    dp.message.register(game_mode, F.text.lower() == "режим игры")

    dp.message.register(answer, F.from_user.id.func(
        lambda x: action.keys().__contains__(x) and action[x] == "раунд"
    ))

    dp.message.register(vote, F.from_user.id.func(
        lambda x: action.keys().__contains__(x) and action[x] == "vote"
    ))
    dp.message.register(set_round_limit, F.from_user.id.func(
        lambda x: action.keys().__contains__(x) and action[x] == "enter_round_limit"
    ))

    dp.message.register(unknown_command)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
