import common


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
