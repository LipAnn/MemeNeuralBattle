from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

import common

kb_default_buttons = [
    [
        KeyboardButton(text="Создать игру"),
        KeyboardButton(text="Присоединиться к игре")
    ]
]
kb_default = ReplyKeyboardMarkup(keyboard=kb_default_buttons, resize_keyboard=True)


async def start(message: types.Message):

    common.user_id_to_chat_id[message.from_user.id] = message.chat.id

    first_name = message.from_user.first_name if message.from_user.first_name is not None else ""
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ""

    common.user_id_to_name[message.from_user.id] = first_name + " " + last_name

    await message.answer("Старт", reply_markup=kb_default)
