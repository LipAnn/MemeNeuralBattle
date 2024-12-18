from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import common
import default_menu
import replies
from default_menu import kb_default
from classes import Game

kb_client_buttons = [
    [
        KeyboardButton(text="Выйти из игры")
    ]
]
kb_client = ReplyKeyboardMarkup(keyboard=kb_client_buttons, resize_keyboard=True)


async def join_game(message: types.Message):
    if await Game.is_in_game(message.from_user.id):
        await message.answer(replies.ALREADY_CONNECTED_TO_THE_GAME)
        return

    common.action[message.from_user.id] = "Присоединиться к игре"
    await message.answer(replies.WRITE_A_GAME_CODE_TO_CONNECT)


async def join_specified_game(message: types.Message):
    if await Game.is_in_game(message.from_user.id):
        await message.answer(replies.ALREADY_CONNECTED_TO_THE_GAME, reply_markup=default_menu.kb_default)
        return

    common.action[message.from_user.id] = ""
    code = message.text

    if not common.code_to_game.keys().__contains__(code):
        await message.answer(replies.THE_GAME_DOES_NOT_EXIST, reply_markup=kb_default)
        return

    game = common.code_to_game[code]
    if len(game.players) >= game.limit_players:
        await message.answer(replies.TOO_MANY_PLAYERS)
        return

    await game.join(message.from_user.id)
    await message.answer(replies.SUCCESSFULLY_CONNECTED_TO_THE_GAME, reply_markup=kb_client)


async def leave_game(message: types.Message):
    if not await Game.is_in_game(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_CONNECTED_TO_THE_GAME)
        return

    game = await Game.get_game(message.from_user.id)
    await game.leave(message.from_user.id)

    await message.answer(replies.YOU_LEFT_THE_GAME, reply_markup=default_menu.kb_default)
