import random

from aiogram import types

import common
import default_menu
import keyboard
import replies
from game import Game
from keyboard import kb_host


async def create_new_game(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if await Game.is_in_game(message.from_user.id):
        await message.answer(replies.ALREADY_CONNECTED_TO_THE_GAME)
        return

    game_code = await generate_random_token()
    game = Game(code=game_code, host=message.from_user.id, limit_players=8)

    await message.answer(replies.THE_GAME_HAS_BEEN_CREATED.format(code=game_code), reply_markup=kb_host)


# Очень кринжовая кривая функция ради того, чтобы была. Ради бога, перепиши её когда-нибудь
async def generate_random_token():
    code = random.randint(100, 999)
    while common.used_codes.__contains__(code):
        code = random.randint(100, 999)

    return str(code)


async def leave_and_destroy_game(message: types.Message):
    await common.update_caches(message)

    common.action[message.from_user.id] = ""

    if not await Game.is_in_game(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_CONNECTED_TO_THE_GAME, reply_markup=default_menu.kb_default)
        return

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = common.code_to_game[common.host_to_game_code[message.from_user.id]]
    await game.destroy()


async def start_game(message: types.Message):
    await common.update_caches(message)

    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = common.code_to_game[common.host_to_game_code[message.from_user.id]]

    if game.is_started:
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    if len(game.players) == 1:
        await message.answer(replies.YOU_CANNOT_START_THE_GAME_ALONE)
        return

    await game.start()


async def options(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)
    if game.mode == 1:
        game_mode = "Нейро"
    elif game.mode == 2:
        game_mode = "Смешанный"
    else:
        game_mode = "Классичесикй"
    await message.answer(replies.OPTIONS.format(game_mode=game_mode, round_limit=game.round_limit, players_count=len(game.players)), reply_markup=keyboard.kb_host_options)


async def enter_round_limit(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    await message.answer(replies.ENTER_ROUND_LIMIT)
    common.action[message.from_user.id] = "enter_round_limit"


async def set_round_limit(message: types.Message):
    await common.update_caches(message)

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        common.action[message.from_user.id] = ""
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)

    if game.is_started:
        common.action[message.from_user.id] = ""
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    try:
        int(message.text)
    except:
        await message.answer(replies.WRONG_ROUND_LIMIT)
        return

    if int(message.text) > 10 or int(message.text) < 1:
        await message.answer(replies.WRONG_ROUND_LIMIT)
        return

    game.round_limit = int(message.text)

    common.action[message.from_user.id] = ""
    await message.answer(replies.ROUND_LIMIT_HAS_BEEN_SET, reply_markup=keyboard.kb_host_options)


async def back_to_menu(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        await message.answer(replies.MENU, reply_markup=keyboard.kb_client)
    else:
        await message.answer(replies.MENU, reply_markup=keyboard.kb_host)


async def set_classic_mode(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        common.action[message.from_user.id] = ""
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)

    if game.is_started:
        common.action[message.from_user.id] = ""
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    game.mode = 0
    await message.answer(replies.CLASSIC_MODE_HAS_BEEN_SET, reply_markup=keyboard.kb_host_game_mode)


async def set_ai_mode(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        common.action[message.from_user.id] = ""
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)

    if game.is_started:
        common.action[message.from_user.id] = ""
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    game.mode = 1
    await message.answer(replies.AI_MODE_HAS_BEEN_SET, reply_markup=keyboard.kb_host_game_mode)


async def set_mixed_mode(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        common.action[message.from_user.id] = ""
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)

    if game.is_started:
        common.action[message.from_user.id] = ""
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    game.mode = 2
    await message.answer(replies.MIXED_MODE_HAS_BEEN_SET, reply_markup=keyboard.kb_host_game_mode)


async def game_mode(message: types.Message):
    await common.update_caches(message)
    common.action[message.from_user.id] = ""

    if not common.host_to_game_code.keys().__contains__(message.from_user.id):
        common.action[message.from_user.id] = ""
        await message.answer(replies.YOU_ARE_NOT_A_GAME_HOST)
        return

    game = await Game.get_game(message.from_user.id)

    if game.is_started:
        common.action[message.from_user.id] = ""
        await message.answer(replies.THE_GAME_IS_ALREADY_STARTED)
        return

    await message.answer(replies.SELECT_GAME_MODE, reply_markup=keyboard.kb_host_game_mode)
