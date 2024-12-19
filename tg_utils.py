import os.path

from aiogram.utils.media_group import MediaGroupBuilder

import common
from aiogram.types import FSInputFile
import aiogram.types


async def send_message(user_id, message):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message)


async def send_message_kb(user_id, message, reply_markup):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message, reply_markup=reply_markup)


async def send_group_message_kb(users, message, reply_markup):
    for user in users:
        await common.bot.send_message(chat_id=common.user_id_to_chat_id[user], text=message, reply_markup=reply_markup)


async def send_group_message(users, message):
    for user in users:
        await common.bot.send_message(chat_id=common.user_id_to_chat_id[user], text=message)


async def send_image(user, image_name):
    image_name += ".jpg"
    await common.bot.send_photo(chat_id=common.user_id_to_chat_id[user],
                                photo=FSInputFile(path=os.path.join(common.images_dir, image_name)))


async def send_images(user, caption, image_names):
    media = MediaGroupBuilder(caption=caption)
    for image_name in image_names:
        image_name += ".jpg"
        media.add_photo(FSInputFile(path="images/" + image_name))

    await common.bot.send_media_group(chat_id=common.user_id_to_chat_id[user], media=media.build())
