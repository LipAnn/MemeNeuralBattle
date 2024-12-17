import common


async def send_message(user_id, message):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message)


async def send_message_kb(user_id, message, reply_markup):
    await common.bot.send_message(chat_id=common.user_id_to_chat_id[user_id], text=message, reply_markup=reply_markup)
