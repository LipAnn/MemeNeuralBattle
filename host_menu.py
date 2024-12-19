import random

from aiogram import types

import common
import replies
from game import Game
from keyboard import kb_host


async def create_new_game(message: types.Message):

    common.action[message.from_user.id] = ""

    game_code = await generate_random_token()
    game = Game(code=game_code, host=message.from_user.id, limit_players=8)

    await message.answer("Игра создана, код игры: " + str(game_code), reply_markup=kb_host)

# Очень кринжовая кривая функция ради того, чтобы была. Ради бога, перепиши её когда-нибудь
async def generate_random_token():

    code = random.randint(100, 999)
    while common.used_codes.__contains__(code):
        code = random.randint(100, 999)

    return str(code)


async def leave_and_destroy_game(message: types.Message):

    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = common.code_to_game[common.host_to_game_code[message.from_user.id]]
    await game.destroy()


async def start_game(message: types.Message):

    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = common.code_to_game[common.host_to_game_code[message.from_user.id]]
    await game.start()
