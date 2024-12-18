from aiogram import types
import common
import replies
from game import Game


async def answer(message: types.Message):

    if message.text not in ["1", "2", "3", "4", "5", "6"]:
        await message.answer(replies.WRONG_PIC_NUMBER)
        return

    common.action[message.from_user.id] = ""

    game = await Game.get_game(message.from_user.id)

    if game.answer.keys().__contains__(message.from_user.id):
        await message.answer(replies.YOU_HAVE_ALREADY_SET_AN_ANSWER)
        return

    await game.set_answer(message.from_user.id, message.text)
