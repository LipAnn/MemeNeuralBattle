from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import common
import replies

kb_default_buttons = [
    [
        KeyboardButton(text="Создать игру"),
        KeyboardButton(text="Присоединиться к игре")
    ],
    [
        KeyboardButton(text="Правила")
    ]
]
kb_default = ReplyKeyboardMarkup(keyboard=kb_default_buttons, resize_keyboard=True)


async def start(message: types.Message):
    await common.update_caches(message)
    await message.answer(replies.START_MESSAGE, reply_markup=kb_default)


async def help(message: types.Message):
    await common.update_caches(message)
    await message.answer(replies.HELP)
