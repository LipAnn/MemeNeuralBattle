from aiogram import types

import common
import default_menu
import replies
from game import Game
from default_menu import kb_default
from keyboard import kb_client


async def join_game(message: types.Message):

    await common.update_caches(message)

    common.action[message.from_user.id] = ""

    if await Game.is_in_game(message.from_user.id):
        await message.answer(replies.ALREADY_CONNECTED_TO_THE_GAME)
        return

    common.action[message.from_user.id] = "Присоединиться к игре"
    await message.answer(replies.WRITE_A_GAME_CODE_TO_CONNECT)


async def join_specified_game(message: types.Message):

    await common.update_caches(message)

    common.action[message.from_user.id] = ""

    if await Game.is_in_game(message.from_user.id):
        await message.answer(replies.ALREADY_CONNECTED_TO_THE_GAME, reply_markup=default_menu.kb_default)
        return

    common.action[message.from_user.id] = ""
    code = message.text

    if not common.code_to_game.keys().__contains__(code):
        await message.answer(replies.THE_GAME_DOES_NOT_EXIST, reply_markup=kb_default)
        return

    game = common.code_to_game[code]

    if game.is_started:
        await message.answer(replies.CANNOT_JOIN_TO_STARTED_GAME)
        return

    if len(game.players) >= game.limit_players:
        await message.answer(replies.TOO_MANY_PLAYERS)
        return

    await game.join(message.from_user.id)
    await message.answer(replies.SUCCESSFULLY_CONNECTED_TO_THE_GAME, reply_markup=kb_client)


async def leave_game(message: types.Message):

    await common.update_caches(message)

    common.action[message.from_user.id] = ""

    if not await Game.is_in_game(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_CONNECTED_TO_THE_GAME, reply_markup=default_menu.kb_default)
        return

    game = await Game.get_game(message.from_user.id)
    await game.leave(message.from_user.id)

    await message.answer(replies.YOU_LEFT_THE_GAME, reply_markup=default_menu.kb_default)
