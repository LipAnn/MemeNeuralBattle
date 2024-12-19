from aiogram import types
from game import Game

import common
import replies


async def vote(message: types.Message):

    try:
        int(message.text)
    except:
        await message.answer(replies.WRONG_PIC_NUMBER)
        return

    game = await Game.get_game(message.from_user.id)

    if int(message.text) not in range(1, len(game.players) + 1):
        await message.answer(replies.WRONG_PIC_NUMBER)
        return

    if game.players[int(message.text) - 1] == message.from_user.id:
        await message.answer(replies.YOU_CANNOT_VOTE_FOR_YOURSELF)
        return

    common.action[message.from_user.id] = ""
    await game.set_vote(message.from_user.id, message.text)