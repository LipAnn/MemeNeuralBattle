import os.path

from aiogram.utils.media_group import MediaGroupBuilder

import common
from aiogram.types import FSInputFile
import aiogram.types


async def send_message(user_id, message):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message)


async def send_message_kb(user_id, message, keyboard):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message, reply_markup=keyboard)


async def send_group_message_kb(users, message, keyboard):
    for user in users:
        await common.bot.send_message(chat_id=common.user_id_to_chat_id[user], text=message, reply_markup=keyboard)


async def send_group_message(users, message):
    for user in users:
        await common.bot.send_message(chat_id=common.user_id_to_chat_id[user], text=message)


async def send_images(user, caption, image_names, ai):
    media = MediaGroupBuilder(caption=caption)
    for image_name in image_names:
        image_name += ".jpg"
        if ai == 1:
            media.add_photo(FSInputFile(path="ai_images/" + image_name))
        elif ai == 0:
            media.add_photo(FSInputFile(path="images/" + image_name))
        else:
            media.add_photo(FSInputFile(path="mixed_images/" + image_name))

    await common.bot.send_media_group(chat_id=common.user_id_to_chat_id[user], media=media.build())
